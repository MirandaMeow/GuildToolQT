from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import QGroupBox

import Charts

_MISS_TABLE_COLUMN = {
    "名称": 140,
    "出刀数": 83,
    "缺刀数": 83,
    "伤害": 140,
    "伤害占比 %": 81
}
_TEAM_TABLE_COLUMN = {
    "第一刀": 100,
    "第二刀": 100,
    "第三刀": 100
}
_STAT_TABLE_COLUMN = {
    "名称": 100,
    "出刀数": 100,
    "缺刀数": 100,
    "总伤害": 100,
    "日均伤害": 100,
    "平均伤害": 100,
    "总伤占比 %": 100
}

_BATTLE_REPORT_TABLE_COLUMN = {
    "队伍": 100,
    "玩家": 100,
    "时间": 100,
    "伤害": 100,
    "Boss": 100,
    "等级": 100,
    "属性": 100,
    "剩余生命": 100
}


class Miss(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("缺刀统计")

        self.__horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.__layout = QtWidgets.QGridLayout()
        self.__layout.setSpacing(11)
        self.__horizontal_layout.addLayout(self.__layout)

        self.__label_date = QtWidgets.QLabel(self)
        self.__label_date.setText("日期选择：")
        self.__layout.addWidget(self.__label_date, 0, 0, 1, 1)

        self.__date = QtWidgets.QDateEdit(self)
        self.__date.setCalendarPopup(True)
        self.__date.calendarWidget().setFirstDayOfWeek(Qt.DayOfWeek.Sunday)
        self.__date.setDisplayFormat("yyyy-MM-dd")
        self.__layout.addWidget(self.__date, 0, 1, 1, 1)

        self.__check_miss = QtWidgets.QCheckBox(self)
        self.__check_miss.setText("只显示缺刀")
        self.__layout.addWidget(self.__check_miss, 0, 2, 1, 1)

        self.__label_total_damage = QtWidgets.QLabel(self)
        self.__label_total_damage.setText("总伤害：")
        self.__layout.addWidget(self.__label_total_damage, 0, 3, 1, 1)

        self.__lcd = QtWidgets.QLCDNumber(self)
        self.__lcd.setMinimumSize(0, 52)
        self.__lcd.setDigitCount(10)
        self.__layout.addWidget(self.__lcd, 0, 4, 1, 1)

        self.__table_miss = QtWidgets.QTableWidget(self)
        self.__table_miss.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.__table_miss.setRowCount(30)
        self.__table_miss.setColumnCount(5)
        _index = 0
        for column_name, width in _MISS_TABLE_COLUMN.items():
            column = QtWidgets.QTableWidgetItem()
            column.setText(column_name)
            self.__table_miss.setHorizontalHeaderItem(_index, column)
            self.__table_miss.setColumnWidth(_index, width)
            _index += 1
        self.__layout.addWidget(self.__table_miss, 1, 0, 1, 5)

        self.__layout.setColumnStretch(0, 10)
        self.__layout.setColumnStretch(1, 15)
        self.__layout.setColumnStretch(2, 10)
        self.__layout.setColumnStretch(3, 10)
        self.__layout.setColumnStretch(4, 50)

    def clear(self):
        """
        清除表中数据
        """
        self.__table_miss.clearContents()

    def set_date_range(self, date_range: list):
        """
        设置日期控件中可选日期的范围

        :param date_range: 日期范围
        """
        min_date = date_range[0].split("-")
        max_date = date_range[-1].split("-")
        self.__date.setMinimumDate(QDate(int(min_date[0]), int(min_date[1]), int(min_date[2])))
        self.__date.setMaximumDate(QDate(int(max_date[0]), int(max_date[1]), int(max_date[2])))

    # TODO: 添加更新控件的方法
    def update_data(self, data):
        """
        更新控件中的数据

        :param data: 新的数据
        """
        self.clear()
        ...

    def get_date(self):
        """
        获取当前日期控件的日期
        """
        self.__date.date().toString("yyyy-MM-dd")


class Team(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("刀型数据")
        self.__horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.__table_team = QtWidgets.QTableWidget(self)
        self.__horizontalLayout.addWidget(self.__table_team)
        self.__table_team.setColumnCount(3)
        self.__table_team.setRowCount(14)
        self.__table_team.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        _index = 0
        for i in ["名称", "时间", "队伍", "队伍伤害", "队伍韧性", "队伍属性", "Boss 属性", "Boss 名称",
                  "Boss 等级", "Boss 轮次", "Boss 均伤", "伤害", "剩余生命", "是否尾刀"]:
            row = QtWidgets.QTableWidgetItem()
            row.setText(i)
            self.__table_team.setVerticalHeaderItem(_index, row)
            _index += 1

        _index = 0
        for column_name, width in _TEAM_TABLE_COLUMN.items():
            column = QtWidgets.QTableWidgetItem()
            column.setText(column_name)
            self.__table_team.setHorizontalHeaderItem(_index, column)
            self.__table_team.setColumnWidth(_index, width)
            _index += 1

    def clear(self):
        """
        清除表中数据
        """
        self.__table_team.clearContents()

    # TODO: 添加更新控件的方法
    def update_data(self, data):
        """
        更新控件中的数据

        :param data: 新的数据
        """
        self.clear()
        ...


class Stats(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("伤害统计")
        self.__horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.__table_stats = QtWidgets.QTableWidget(self)
        self.__horizontal_layout.addWidget(self.__table_stats)
        self.__table_stats.setRowCount(30)
        self.__table_stats.setColumnCount(7)
        self.__table_stats.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        _index = 0
        for column_name, width in _STAT_TABLE_COLUMN.items():
            column = QtWidgets.QTableWidgetItem()
            column.setText(column_name)
            self.__table_stats.setHorizontalHeaderItem(_index, column)
            self.__table_stats.setColumnWidth(_index, width)
            _index += 1

    def clear(self):
        """
        清除表中数据
        """
        self.__table_stats.clearContents()

    # TODO: 添加更新控件的方法
    def update_data(self, data):
        """
        更新控件中的数据

        :param data: 新的数据
        """
        self.clear()
        ...


class Boss(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Boss 伤害统计")
        self.__horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.__table_boss = QtWidgets.QTableWidget(self)
        self.__horizontal_layout.addWidget(self.__table_boss)
        self.__table_boss.setRowCount(30)
        self.__table_boss.setColumnCount(9)
        self.__table_boss.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        _index = 0
        column = QtWidgets.QTableWidgetItem()
        column.setText("名称")
        self.__table_boss.setHorizontalHeaderItem(0, column)
        self.__table_boss.setColumnWidth(0, 100)
        for i in range(1, 9, 2):
            column = QtWidgets.QTableWidgetItem()
            column.setText("boss")
            self.__table_boss.setHorizontalHeaderItem(i, column)
            self.__table_boss.setColumnWidth(i, 100)
            column = QtWidgets.QTableWidgetItem()
            column.setText("出刀数")
            self.__table_boss.setHorizontalHeaderItem(i + 1, column)
            self.__table_boss.setColumnWidth(i + 1, 60)

    def clear(self):
        """
        清除表中数据
        """
        self.__table_boss.clearContents()

    # TODO: 添加更新控件的方法
    def update_data(self, data):
        """
        更新控件中的数据

        :param data: 新的数据
        """
        self.clear()
        ...


class Summary(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("汇总统计")
        self.__horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.__tree = QtWidgets.QTreeWidget(self)
        self.__horizontal_layout.addWidget(self.__tree)
        self.__tree.setHeaderHidden(True)
        self.__tree.setSortingEnabled(False)
        self.__item_total_damage = QtWidgets.QTreeWidgetItem(self.__tree)
        self.__item_total_damage.setText(0, "总伤害")
        self.__item_attendance = QtWidgets.QTreeWidgetItem(self.__tree)
        self.__item_attendance.setText(0, "总出勤")
        self.__item_boss_damage = QtWidgets.QTreeWidgetItem(self.__tree)
        self.__item_boss_damage.setText(0, "Boss 伤害")
        self.__item_top_damage = QtWidgets.QTreeWidgetItem(self.__tree)
        self.__item_top_damage.setText(0, "最高伤害榜")
        self.__item_low_damage = QtWidgets.QTreeWidgetItem(self.__tree)
        self.__item_low_damage.setText(0, "最低伤害榜")
        self.__item_low_last_damage = QtWidgets.QTreeWidgetItem(self.__tree)
        self.__item_low_last_damage.setText(0, "最低尾刀榜")
        self.__item_leave_last_count = QtWidgets.QTreeWidgetItem(self.__tree)
        self.__item_leave_last_count.setText(0, "留尾榜")
        self.__item_last_count = QtWidgets.QTreeWidgetItem(self.__tree)
        self.__item_last_count.setText(0, "收尾榜")
        self.__item_total_miss = QtWidgets.QTreeWidgetItem(self.__tree)
        self.__item_total_miss.setText(0, "缺刀榜")


class QueryBattleReport(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("查询设置")

        self.__horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.__layout = QtWidgets.QGridLayout()
        self.__horizontal_layout.addLayout(self.__layout)

        self.__label_date = QtWidgets.QLabel(self)
        self.__label_date.setText("日期范围：")
        self.__label_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__layout.addWidget(self.__label_date, 0, 0, 1, 1)

        self.__label_damage = QtWidgets.QLabel(self)
        self.__label_damage.setText("伤害范围：")
        self.__label_damage.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__layout.addWidget(self.__label_damage, 1, 0, 1, 1)

        self.__label_remain = QtWidgets.QLabel(self)
        self.__label_remain.setText("剩余生命范围：")
        self.__label_remain.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__layout.addWidget(self.__label_remain, 2, 0, 1, 1)

        self.__label_boss_level = QtWidgets.QLabel(self)
        self.__label_boss_level.setText("Boss 等级：")
        self.__label_boss_level.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__layout.addWidget(self.__label_boss_level, 3, 0, 1, 1)

        self.__label_boss_name = QtWidgets.QLabel(self)
        self.__label_boss_name.setText("Boss 名称：")
        self.__label_boss_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__layout.addWidget(self.__label_boss_name, 4, 0, 1, 1)

        self.__label_player = QtWidgets.QLabel(self)
        self.__label_player.setText("玩家：")
        self.__label_player.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__layout.addWidget(self.__label_player, 5, 0, 1, 1)

        self.__label_team = QtWidgets.QLabel(self)
        self.__label_team.setText("队伍筛选：")
        self.__label_team.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__layout.addWidget(self.__label_team, 6, 0, 1, 1)

        self.__label_result_0 = QtWidgets.QLabel(self)
        self.__label_result_0.setText("查询结果：")
        self.__label_result_0.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__layout.addWidget(self.__label_result_0, 7, 0, 1, 1)

        self.__label_result = QtWidgets.QLabel(self)
        self.__label_result.setText("0/0")
        self.__layout.addWidget(self.__label_result, 7, 1, 1, 1)

        self.__date_start = QtWidgets.QDateEdit(self)
        self.__date_start.setCalendarPopup(True)
        self.__layout.addWidget(self.__date_start, 0, 1, 1, 1)

        self.__date_end = QtWidgets.QDateEdit(self)
        self.__date_end.setCalendarPopup(True)
        self.__layout.addWidget(self.__date_end, 0, 2, 1, 1)

        self.__line_damage_min = QtWidgets.QLineEdit(self)
        self.__line_damage_min.setMaxLength(9)
        self.__line_damage_min.setPlaceholderText("0")
        self.__layout.addWidget(self.__line_damage_min, 1, 1, 1, 1)

        self.__line_damage_max = QtWidgets.QLineEdit(self)
        self.__line_damage_max.setMaxLength(9)
        self.__line_damage_max.setPlaceholderText("99999999")
        self.__layout.addWidget(self.__line_damage_max, 1, 2, 1, 1)

        self.__line_remain_min = QtWidgets.QLineEdit(self)
        self.__line_remain_min.setMaxLength(9)
        self.__line_remain_min.setPlaceholderText("0")
        self.__layout.addWidget(self.__line_remain_min, 2, 1, 1, 1)

        self.__line_remain_max = QtWidgets.QLineEdit(self)
        self.__line_remain_max.setMaxLength(9)
        self.__line_remain_max.setPlaceholderText("999999999")
        self.__layout.addWidget(self.__line_remain_max, 2, 2, 1, 1)

        self.__line_level_min = QtWidgets.QLineEdit(self)
        self.__line_level_min.setMaxLength(9)
        self.__line_level_min.setPlaceholderText("0")
        self.__layout.addWidget(self.__line_level_min, 3, 1, 1, 1)

        self.__line_level_max = QtWidgets.QLineEdit(self)
        self.__line_level_max.setMaxLength(9)
        self.__line_level_max.setPlaceholderText("99")
        self.__layout.addWidget(self.__line_level_max, 3, 2, 1, 1)

        self.__combobox_boss = QtWidgets.QComboBox(self)
        self.__layout.addWidget(self.__combobox_boss, 4, 1, 1, 1)

        self.__combobox_player = QtWidgets.QComboBox(self)
        self.__layout.addWidget(self.__combobox_player, 5, 1, 1, 1)

        self.__button_team = QtWidgets.QPushButton(self)
        self.__button_team.setText("队伍")
        self.__layout.addWidget(self.__button_team, 6, 1, 1, 1)

        self.__button_query = QtWidgets.QPushButton(self)
        self.__button_query.setText("查询")
        self.__layout.addWidget(self.__button_query, 6, 3, 1, 1)

        self.__button_reset = QtWidgets.QPushButton(self)
        self.__button_reset.setText("重置")
        self.__layout.addWidget(self.__button_reset, 7, 3, 1, 1)


class BattleReports(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("战斗记录")

        self.__horizontal_layout = QtWidgets.QHBoxLayout(self)

        self.__table_battle_reports = QtWidgets.QTableWidget(self)
        self.__table_battle_reports.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.__table_battle_reports.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.__table_battle_reports.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.__table_battle_reports.setRowCount(1350)
        self.__table_battle_reports.setColumnCount(8)
        self.__horizontal_layout.addWidget(self.__table_battle_reports)
        _index = 0
        for column_name, width in _BATTLE_REPORT_TABLE_COLUMN.items():
            column = QtWidgets.QTableWidgetItem()
            column.setText(column_name)
            self.__table_battle_reports.setHorizontalHeaderItem(_index, column)
            self.__table_battle_reports.setColumnWidth(_index, width)
            _index += 1


class BossRemain(QGroupBox):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.setTitle(name)
        self.setFixedSize(380, 400)
        self.__horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.__layout = QtWidgets.QVBoxLayout()
        self.__horizontal_layout.addLayout(self.__layout)

        # 第一个 Boss
        self.__frame_boss1 = QtWidgets.QFrame(self)
        self.__layout.addWidget(self.__frame_boss1)
        self.__frame_boss1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.__frame_boss1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.__horizontal_layout_boss1 = QtWidgets.QHBoxLayout(self.__frame_boss1)
        self.__layout_boss1 = QtWidgets.QGridLayout()
        self.__horizontal_layout_boss1.addLayout(self.__layout_boss1)

        self.__label_boss1_name = QtWidgets.QLabel(self.__frame_boss1)
        self.__label_boss1_name.setText("第 0 轮 Lv 99 喔喔怪")
        self.__layout_boss1.addWidget(self.__label_boss1_name, 0, 0, 1, 1)

        self.__label_boss1_elemental = QtWidgets.QLabel(self.__frame_boss1)
        self.__label_boss1_elemental.setText("光属性")
        self.__label_boss1_elemental.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__layout_boss1.addWidget(self.__label_boss1_elemental, 0, 1, 1, 1)

        self.__bar_boss1 = Charts.HPBar(self)
        self.__layout_boss1.addWidget(self.__bar_boss1, 1, 0, 1, 2)

        self.__layout_boss1.setRowStretch(0, 1)
        self.__layout_boss1.setRowStretch(1, 3)

        # 第二个 Boss
        self.__frame_boss2 = QtWidgets.QFrame(self)
        self.__layout.addWidget(self.__frame_boss2)
        self.__frame_boss2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.__frame_boss2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.__horizontal_layout_boss2 = QtWidgets.QHBoxLayout(self.__frame_boss2)
        self.__layout_boss2 = QtWidgets.QGridLayout()
        self.__horizontal_layout_boss2.addLayout(self.__layout_boss2)

        self.__label_boss2_name = QtWidgets.QLabel(self.__frame_boss2)
        self.__label_boss2_name.setText("第 0 轮 Lv 99 喔喔怪")
        self.__layout_boss2.addWidget(self.__label_boss2_name, 0, 0, 1, 1)

        self.__label_boss2_elemental = QtWidgets.QLabel(self.__frame_boss2)
        self.__label_boss2_elemental.setText("光属性")
        self.__label_boss2_elemental.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__layout_boss2.addWidget(self.__label_boss2_elemental, 0, 1, 1, 1)

        self.__bar_boss2 = Charts.HPBar(self)
        self.__layout_boss2.addWidget(self.__bar_boss2, 1, 0, 1, 2)

        self.__layout_boss2.setRowStretch(0, 1)
        self.__layout_boss2.setRowStretch(1, 3)

        # 第三个 Boss
        self.__frame_boss3 = QtWidgets.QFrame(self)
        self.__layout.addWidget(self.__frame_boss3)
        self.__frame_boss3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.__frame_boss3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.__horizontal_layout_boss3 = QtWidgets.QHBoxLayout(self.__frame_boss3)
        self.__layout_boss3 = QtWidgets.QGridLayout()
        self.__horizontal_layout_boss3.addLayout(self.__layout_boss3)

        self.__label_boss3_name = QtWidgets.QLabel(self.__frame_boss3)
        self.__label_boss3_name.setText("第 0 轮 Lv 99 喔喔怪")
        self.__layout_boss3.addWidget(self.__label_boss3_name, 0, 0, 1, 1)

        self.__label_boss3_elemental = QtWidgets.QLabel(self.__frame_boss3)
        self.__label_boss3_elemental.setText("光属性")
        self.__label_boss3_elemental.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__layout_boss3.addWidget(self.__label_boss3_elemental, 0, 1, 1, 1)

        self.__bar_boss3 = Charts.HPBar(self)
        self.__layout_boss3.addWidget(self.__bar_boss3, 1, 0, 1, 2)

        self.__layout_boss3.setRowStretch(0, 1)
        self.__layout_boss3.setRowStretch(1, 3)

        # 第四个 Boss
        self.__frame_boss4 = QtWidgets.QFrame(self)
        self.__layout.addWidget(self.__frame_boss4)
        self.__frame_boss4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.__frame_boss4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.__horizontal_layout_boss4 = QtWidgets.QHBoxLayout(self.__frame_boss4)
        self.__layout_boss4 = QtWidgets.QGridLayout()
        self.__horizontal_layout_boss4.addLayout(self.__layout_boss4)

        self.__label_boss4_name = QtWidgets.QLabel(self.__frame_boss4)
        self.__label_boss4_name.setText("第 0 轮 Lv 99 喔喔怪")
        self.__layout_boss4.addWidget(self.__label_boss4_name, 0, 0, 1, 1)

        self.__label_boss4_elemental = QtWidgets.QLabel(self.__frame_boss4)
        self.__label_boss4_elemental.setText("光属性")
        self.__label_boss4_elemental.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__layout_boss4.addWidget(self.__label_boss4_elemental, 0, 1, 1, 1)

        self.__bar_boss4 = Charts.HPBar(self)
        self.__layout_boss4.addWidget(self.__bar_boss4, 1, 0, 1, 2)

        self.__layout_boss4.setRowStretch(0, 1)
        self.__layout_boss4.setRowStretch(1, 3)
