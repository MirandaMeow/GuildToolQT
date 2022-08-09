from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import QGroupBox

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


class Miss(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("缺刀统计")

        self.__horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.__layout = QtWidgets.QGridLayout()
        self.__layout.setSpacing(11)

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
        self.__horizontal_layout.addLayout(self.__layout)

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
        self.__horizontal_layout.addWidget(self.__tree)
