import copy
import json

from PyQt6 import QtSql

import Settings


class Database:
    def __init__(self, database_path: str):
        """
        数据库

        :param database_path: 数据库路径
        """
        self.__database = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.__database.setDatabaseName(database_path)
        self.__database.open()

    def create_table(self, table_name: str, columns: list):
        """
        在数据库中创建一个新的表

        :param table_name: 表名称
        :param columns: 列属性
        """
        column_string = ", ".join(columns)
        self.__database.exec(f"CREATE TABLE {table_name} ({column_string})")
        self.__database.lastError().text()

    def delete_table(self, table_name: str):
        """
        从数据库中删除一个表

        :param table_name: 表名称
        """
        self.__database.exec(f"DROP TABLE {table_name}")

    def add_data(self, table_name: str, data: list):
        """
        在指定表中添加一行数据

        :param table_name: 表名称
        :param data: 插入的数据
        """
        values_string = ("?," * len(data))[:-1]
        query = QtSql.QSqlQuery(self.__database)
        query.prepare(f"REPLACE INTO {table_name} VALUES({values_string})")
        for i in data:
            query.addBindValue(i)
        query.exec()

    def delete_data(self, table_name: str, where: dict):
        """
        在指定表种删除一行数据

        :param table_name: 表名称
        :param where: 删除条件
        """
        query = QtSql.QSqlQuery(self.__database)
        where_string_list = []
        for k, v in where.items():
            where_string_list.append(f"{k}{v[0]}'{v[1]}'")
        where_string = " AND ".join(where_string_list)
        query.prepare(f"DELETE FROM {table_name} WHERE {where_string}")
        query.exec()

    def modify_data(self, table_name: str, modified_data: dict, where: dict):
        """
        编辑指定表中的数据

        :param table_name: 表名称
        :param modified_data: 新的数据
        :param where: 修改位置
        """
        query = QtSql.QSqlQuery(self.__database)
        modify_data_list = []
        for k, v in modified_data.items():
            modify_data_list.append(f"{k}='{v}'")
        modify_data = ", ".join(modify_data_list)
        where_string = ""
        for k, v in where.items():
            where_string += f"{k}{v[0]}{v[1]} AND "
        where_string = where_string[:-5]
        query.prepare(f"UPDATE {table_name} SET {modify_data} WHERE {where_string}")
        query.exec()

    def get_data(self, table_name: str, where: dict = None) -> list:
        """
        获取指定表的数据

        :param table_name: 表名称
        :param where: 查询条件
        :return: 表数据
        """
        query = QtSql.QSqlQuery(self.__database)
        if where is None:
            query.prepare(f"SELECT * FROM {table_name}")
        else:
            where_string_list = []
            for k, v in where.items():
                where_string_list.append(f"{k}{v[0]}'{v[1]}'")
            where_string = " AND ".join(where_string_list)
            query.prepare(f"SELECT * FROM {table_name} WHERE {where_string}")
        query.exec()
        out = []
        while query.next():
            temp = []
            for i in range(len(query.record())):
                temp.append(query.value(i))
            out.append(temp)
        return out

    def exist_data(self, table_name: str, where: dict) -> bool:
        """
        判断指定表中是否存在指定条件的数据

        :param table_name: 表名称
        :param where: 查询条件
        :return: 数据是否存在
        """
        query = QtSql.QSqlQuery(self.__database)
        where_string_list = []
        for k, v in where.items():
            where_string_list.append(f"{k}{v[0]}'{v[1]}'")
        where_string = " AND ".join(where_string_list)
        query.prepare(f"SELECT * FROM {table_name} WHERE {where_string}")
        query.exec()
        return query.next()

    def close(self):
        """
        整理数据库并保存
        """
        self.__database.exec("VACUUM")
        self.__database.commit()
        self.__database.close()


class Blacklist:
    def __init__(self, database: Database):
        """
        黑名单

        :param database: 将要操作的数据库
        """
        self.__database = database
        self.__database.create_table("Blacklist", ["Name TEXT UNIQUE NOT NULL"])
        self.blacklist = []
        self.__read_database()

    def __read_database(self) -> None:
        """
        从数据库中读取黑名单
        """
        temp = self.__database.get_data("Blacklist")
        for i in temp:
            self.blacklist.append(i[0])

    def add(self, player_name) -> None:
        """
        向黑名单中添加一个玩家

        :param player_name: 玩家名
        """
        player_name = str(player_name)
        self.blacklist.append(player_name)
        self.__database.add_data("Blacklist", [player_name])

    def remove(self, player_name) -> None:
        """
        从黑名单中删除一个玩家

        :param player_name: 玩家名
        """
        player_name = str(player_name)
        if player_name not in self.blacklist:
            return
        self.blacklist.remove(player_name)
        self.__database.delete_data("Blacklist", {"Name": player_name})


class History:
    def __init__(self, database: Database):
        """
        历史记录

        :param database: 将要操作的数据库
        """
        self.__database = database
        self.__database.create_table("GuildWarData", ["DataRange UNIQUE TEXT NOT NULL", "Data TEXT"])
        self.is_current = True
        self.__history = {}
        self.date_ranges = {}
        self.__read_database()

    def __read_database(self):
        """
        从数据库中读取历史记录
        """
        temp = self.__database.get_data("GuildWarData")
        for i in temp:
            temp_json = i[1].replace("'", '"')
            self.__history[i[0]] = json.loads(temp_json)

    def get_history(self, date_range):
        """
        获取指定日期范围的历史记录

        :param date_range: 日期范围
        :return: 指定的历史记录
        """
        self.is_current = self.date_ranges.index(date_range) == 0
        return self.__history[date_range]

    def update(self):
        """
        更新历史记录
        """
        self.__init__(self.__database)


class Rename:
    def __init__(self, database: Database):
        """
        重命名

        :param database: 将要操作的数据库
        """
        self.__database = database
        self.__database.create_table("Rename", ["OldName UNIQUE TEXT NOT NULL", "NewName TEXT NOT NULL"])
        self.rename = {}
        self.__read_database()

    def __read_database(self):
        """
        从数据库中读取重命名映射
        """
        renames = self.__database.get_data("Rename")
        for i in renames:
            self.rename[i[0]] = i[1]

    def add(self, old_name, new_name):
        """
        添加一个重命名映射

        :param old_name: 玩家的原本名称
        :param new_name: 将要被重命名的名称
        """
        self.rename[str(old_name)] = str(new_name)
        self.__database.add_data("Rename", [old_name, new_name])

    def remove(self, old_name):
        """
        移除一个重命名映射

        :param old_name: 将要被移除的重命名映射
        """
        old_name = str(old_name)
        if old_name not in self.rename:
            return
        del self.rename[old_name]
        self.__database.delete_data("Rename", {"oldName": ["=", old_name]})


class BossState:
    def __init__(self, boss: dict):
        """
        Boss 状态

        :param boss: Boss 名称和属性
        """
        self.__boss_state = {}
        _index = 0
        for boss_name, boss_elemental in boss.items():
            self.__boss_state[boss_name] = {
                "health": 1080000,
                "round": 1,
                "level": 50,
                "elemental": boss_elemental,
                "max_health": 1080000
            }

    def hit(self, boss_name, damage):
        """
        Boss 被攻击

        :param boss_name: 被攻击的 Boss
        :param damage: 造成的伤害
        """
        self.__boss_state[boss_name]["health"] -= damage
        current_health = self.__boss_state[boss_name]["health"]
        if current_health <= 0:
            update = True
            for boss_name, values in self.__boss_state.items():
                if values["health"] > 0:
                    update = False
            if update:
                self.__next()

    def __next(self):
        """
        进入下一轮
        """
        for boss_name, values in self.__boss_state.items():
            values["round"] += 1
            values["health"] = Settings.BOSS_HEALTH[self.__boss_state[boss_name]["round"]]["health"]
            values["max_health"] = values["health"]
            values["level"] = Settings.BOSS_HEALTH[self.__boss_state[boss_name]["round"]]["level"]

    def get_remain(self, boss_name):
        """
        获取 Boss 剩余生命

        :param boss_name: boss 名
        :return: Boss 剩余生命
        """
        return self.__boss_state[boss_name]["health"]

    def get_round(self, boss_name):
        """
        获取 Boss 轮数

        :param boss_name: boss 名
        :return: Boss 轮数
        """
        return self.__boss_state[boss_name]["round"]

    def get_level(self, boss_name):
        """
        获取 Boss 等级

        :param boss_name: boss 名
        :return: Boss 等级
        """
        return self.__boss_state[boss_name]["level"]

    def get_boss_max_health(self, boss_name):
        """
        获取 Boss 最大生命

        :param boss_name: boss 名
        :return: Boss 最大生命
        """
        return self.__boss_state[boss_name]["max_health"]

    def get_all(self):
        """
        获取所有 Boss 状态的深拷贝

        :return: Boss 状态
        """
        return copy.deepcopy(self.__boss_state)

    def check_missed(self, boss_name):
        """
        检查战斗记录中是否有缺失

        :param boss_name: Boss 名
        :return: [是否缺失， 缺失的伤害]
        """
        missed = False
        missed_damage = 0
        if self.__boss_state[boss_name]["health"] <= 0:
            for current_boss_name, values in self.__boss_state.items():
                if current_boss_name == boss_name:
                    continue
                if self.__boss_state[current_boss_name]["health"] > 0:
                    missed = current_boss_name
                    missed_damage = self.__boss_state[current_boss_name]["health"]
                    break
        return missed, missed_damage

# TODO：图标管理器
