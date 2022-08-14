import copy

from PyQt6 import QtCore

import Misc
import Settings


class BattleReports:
    def __init__(self, database: Misc.Database):
        """
        战斗记录

        :param database: 将要被操作的数据库
        """
        self.date_list = []
        self.members = []
        self.boss = {}
        self.char_icons = {}
        self.__data = None
        self.valid = False
        self.__start_end = ""
        self.__boss_state = None
        self.__battle_reports_for_save = []
        self.__battle_reports = []
        self.count_battle_report = 0
        self.daily_hits = {}
        self.__database = database

    def save(self):
        """
        保存战斗记录至数据库
        """
        self.__database.add_data("GuildWarData", [self.__start_end, str(self.__battle_reports_for_save)])

    def analyse(self, data: dict, rename: dict):
        """
        处理战斗记录并应用重命名

        :param data: 战斗记录
        :param rename: 重命名
        """
        self.__data = data
        self.valid = self.__data["code"] == 0
        self.__battle_reports = copy.deepcopy(self.__data["data"])
        self.__battle_reports.reverse()
        start_date = QtCore.QDateTime.fromSecsSinceEpoch(self.__battle_reports[0]["log_time"]).toString("yyyy-MM-dd")
        end_date = QtCore.QDate.fromString(start_date, "yyyy-MM-dd").addDays(14).toString("yyyy-MM-dd")
        self.__start_end = f"{start_date} - {end_date}"

        # 得出日期范围，成员列表，Boss 信息，角色头像
        for current in self.__battle_reports:
            current_date = QtCore.QDateTime.fromSecsSinceEpoch(current["log_time"]).toString("yyyy-MM-dd")
            current_player = str(current["user_name"])
            current_boss_name = current["boss"]["name"]
            current_boss_elemental = current["boss"]["elemental_type_cn"]
            if current_date not in self.date_list:
                self.date_list.append(current_date)
            if "数据缺失" not in current_player and current_player not in self.members:
                self.members.append(current_player)
            if current_boss_name not in self.boss:
                self.boss[current_boss_name] = current_boss_elemental
            for current_role_list in current["role_list"]:
                char_icon_name = current_role_list["icon"].split("/")[-1]
                if char_icon_name not in self.char_icons:
                    self.char_icons[char_icon_name] = current_role_list["icon"]

        # 在战斗记录中补齐轮数和 Boss 状态
        self.__boss_state = Misc.BossState(self.boss)
        missed_index = 0
        for current in self.__battle_reports:
            current_boss_name = current["boss"]["name"]
            current_damage = current["damage"]
            current_boss_remain = self.__boss_state.get_remain(current_boss_name)
            current["boss"]["remain"] = current_boss_remain - current_damage
            current["boss"]["round"] = self.__boss_state.get_round(current_boss_name)
            check_missed = self.__boss_state.check_missed(current_boss_name)
            if check_missed[0]:
                missed_index += 1
                new_battle_report = copy.deepcopy(Settings.BLANK_BATTLE_REPORT)
                missed_boss = check_missed[0]
                missed_damage = check_missed[1]
                new_battle_report["log_time"] = current["log_time"] - 1
                new_battle_report["user_name"] = f"- 数据缺失 #{missed_index} -"
                new_battle_report["boss"]["name"] = missed_boss
                new_battle_report["boss"]["elemental_type_cn"] = self.boss[missed_boss]
                new_battle_report["boss"]["round"] = self.__boss_state.get_round(missed_boss)
                new_battle_report["boss"]["level"] = self.__boss_state.get_level(missed_boss)
                new_battle_report["boss"]["remain"] = 0
                new_battle_report["damage"] = missed_damage
                self.__boss_state.hit(missed_boss, missed_damage)
                new_battle_report["boss"]["state"] = self.__boss_state.get_all()
                current["boss"]["remain"] = self.__boss_state.get_boss_max_health(current_boss_name) - current_damage
                current["boss"]["round"] = self.__boss_state.get_round(current_boss_name)
                current["boss"]["level"] = self.__boss_state.get_level(current_boss_name)
                self.__battle_reports_for_save.append(new_battle_report)
            self.__boss_state.hit(current_boss_name, current_damage)
            current["boss"]["state"] = self.__boss_state.get_all()
            self.__battle_reports_for_save.append(current)
        self.__battle_reports = self.__battle_reports_for_save
        self.count_battle_report = len(self.__battle_reports)

        # 应用重命名
        for current in self.__battle_reports:
            current_player = str(current["user_name"])
            if current_player in rename:
                current["user_name"] = rename[current_player]
        self.__get_daily_hits()

    def __get_team_and_elemental(self, role_list: list) -> tuple[str, list]:
        """
        获取队伍成员和根据队伍计算出队伍的属性

        :param role_list: 将要被计算的队伍
        :return: [队伍属性, 队伍成员]
        """
        weight_ = {"土": 0, "火": 0, "水": 0, "光": 0, "暗": 0, "虚": 0}
        weight_first = True
        team = []
        missed = False
        for i in role_list:
            team.append(i["icon"].split("/")[-1])
            current_elemental = self.__get_character_elemental(i["icon"].split("/")[-1])
            if current_elemental == "-":
                missed = True
                break
            if weight_first:
                weight_[current_elemental] += 1.5
                weight_first = False
            else:
                weight_[current_elemental] += 1
        if missed:
            elemental = "缺失"
        else:
            elemental = sorted(weight_.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0][0] + "属性"
        return elemental, team

    def __get_character_elemental(self, char):
        """
        获取角色属性

        :param char: 角色
        :return: 角色的属性
        """
        temp_result = self.__database.get_data("CharacterData", {"Character": ["=", char]})
        return temp_result[0][2]

    def __get_daily_hits(self):
        if self.daily_hits != {}:
            return self.daily_hits
        for date in self.date_list:
            self.daily_hits[date] = {}
        for current in self.__battle_reports:
            qdate = QtCore.QDateTime.fromSecsSinceEpoch(current["log_time"])
            current_date = qdate.toString("yyyy-MM-dd")
            current_datetime = qdate.toString("yyyy-MM-dd hh:mm:ss")
            current_player = current["user_name"]
            current_damage = current["damage"]
            current_boss_round = current["boss"]["round"]
            current_boss_name = current["boss"]["name"]
            current_boss_level = current["boss"]["level"]
            current_boss_elemental = current["boss"]["elemental_type_cn"]
            current_role_list = current["role_list"]
            current_boss = {"round": current_boss_round,
                            "level": current_boss_level,
                            "name": current_boss_name,
                            "elemental": current_boss_elemental}
            team_and_elemental = self.__get_team_and_elemental(current_role_list)

            temp_attack_data = {
                "time": current_datetime,
                "damage": current_damage,
                "boss": current_boss,
                "team_elemental": team_and_elemental[0],
                "team": team_and_elemental[1]
            }
            if current_player not in self.daily_hits[current_date]:
                self.daily_hits[current_date][current_player] = {"attack": []}
            self.daily_hits[current_date][current_player]["attack"].append(temp_attack_data)
        for current_date, current_data in self.daily_hits.items():
            for current_player, current_player_data in current_data.items():
                total_damage = 0
                total_hit = 0
                for current_attack in current_player_data["attack"]:
                    total_damage += current_attack["damage"]
                    total_hit += 1
                current_player_data["total_damage"] = total_damage
                current_player_data["total_count"] = total_hit
