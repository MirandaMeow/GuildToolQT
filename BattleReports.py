import copy

from PyQt6 import QtCore

import Misc
import Settings


class BattleReports:
    def __init__(self, data: dict, rename: dict):
        self.date_list = []
        self.members = []
        self.boss = {}
        self.char_icons = {}
        self.__data = data
        self.valid = self.__data["code"] == 0
        self.__battle_reports: list = copy.deepcopy(self.__data["data"])
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
            for current_role in current["role_list"]:
                char_icon_name = current_role["icon"].split("/")[-1]
                if char_icon_name not in self.char_icons:
                    self.char_icons[char_icon_name] = current_role["icon"]

        # 在战斗记录中补齐轮数和 Boss 状态
        self.__boss_state = Misc.BossState(self.boss)
        missed_index = 0
        self.__battle_reports_for_save = []
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
                new_battle_report["boss"]["round"] = self.__boss_state.get_round(missed_damage)
                new_battle_report["boss"]["level"] = self.__boss_state.get_level(missed_damage)
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

    def save(self, database: Misc.Database):
        database.add_data("GuildWarData", [self.__start_end, str(self.__battle_reports_for_save)])

    # TODO: 生成各个报表数据的方法
