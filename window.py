import sys

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QMainWindow

import Parts

# TODO: 微调窗口大小
_WINDOW_SIZE = {
    0: [800, 500],
    1: [1200, 900],
    2: [1200, 800]
}


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("会战统计工具")
        self.setGeometry(100, 100, 100, 100)

        self.__central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.__central_widget)
        self.__horizontal_layout = QtWidgets.QHBoxLayout(self.__central_widget)

        self.__tab = QtWidgets.QTabWidget(self.__central_widget)
        self.__tab.currentChanged.connect(self.__signal_tab_changed)
        self.__horizontal_layout.addWidget(self.__tab)

        # 选项卡 - 出刀概览
        self.__tab_overview = QtWidgets.QWidget()
        self.__tab.addTab(self.__tab_overview, "出刀概览")

        self.__horizontal_layout_overview = QtWidgets.QHBoxLayout(self.__tab_overview)
        self.__layout_overview = QtWidgets.QVBoxLayout()
        self.__horizontal_layout_overview.addLayout(self.__layout_overview)

        self.__part_miss = Parts.Miss(self.__tab_overview)
        self.__layout_overview.addWidget(self.__part_miss)

        self.__part_team = Parts.Team(self.__tab_overview)
        self.__layout_overview.addWidget(self.__part_team)

        # 选项卡 - 统计数据
        self.__tab_stats = QtWidgets.QWidget()
        self.__tab.addTab(self.__tab_stats, "统计数据")

        self.__horizontal_layout_stats = QtWidgets.QHBoxLayout(self.__tab_stats)
        self.__layout_stats = QtWidgets.QGridLayout()
        self.__horizontal_layout_stats.addLayout(self.__layout_stats)

        self.__part_stats = Parts.Stats(self.__tab_stats)
        self.__layout_stats.addWidget(self.__part_stats, 0, 0, 1, 1)

        self.__part_summary = Parts.Summary(self.__tab_stats)
        self.__layout_stats.addWidget(self.__part_summary, 0, 1, 1, 1)

        self.__part_boss = Parts.Boss(self.__tab_stats)
        self.__layout_stats.addWidget(self.__part_boss, 1, 0, 1, 2)
        self.__layout_stats.setColumnStretch(0, 2)

        # 选项卡 - 战斗记录
        self.__tab_battle_reports = QtWidgets.QWidget()
        self.__tab.addTab(self.__tab_battle_reports, "战斗记录")

        self.__horizontal_layout_battle_reports = QtWidgets.QHBoxLayout(self.__tab_battle_reports)
        self.__layout_battle_reports = QtWidgets.QGridLayout()
        self.__horizontal_layout_battle_reports.addLayout(self.__layout_battle_reports)

        # 菜单栏
        self.__menubar = QtWidgets.QMenuBar(self)
        self.__menu_functions = QtWidgets.QMenu(self.__menubar)
        self.__menu_functions.setTitle("功能")
        self.__menu_change_session_api = QtGui.QAction(self)
        self.__menu_change_session_api.setText("更改公会识别码")
        self.__menu_flush = QtGui.QAction(self)
        self.__menu_flush.setText("刷新数据库")
        self.__menu_export = QtGui.QAction(self)
        self.__menu_export.setText("导出数据到表格")
        self.__menu_clear_icons = QtGui.QAction(self)
        self.__menu_clear_icons.setText("清空头像缓存")
        self.__menu_history = QtGui.QAction(self)
        self.__menu_history.setText("历史记录")

        self.__menu_functions.addAction(self.__menu_change_session_api)
        self.__menu_functions.addSeparator()
        self.__menu_functions.addAction(self.__menu_flush)
        self.__menu_functions.addAction(self.__menu_export)
        self.__menu_functions.addAction(self.__menu_clear_icons)
        self.__menu_functions.addSeparator()
        self.__menu_functions.addAction(self.__menu_history)

        self.__menu_infos = QtWidgets.QMenu(self.__menubar)
        self.__menu_infos.setTitle("信息")

        self.__menu_news = QtGui.QAction(self)
        self.__menu_news.setText("更新记录")
        self.__menu_log = QtGui.QAction(self)
        self.__menu_log.setText("运行日志")
        self.__menu_version = QtGui.QAction(self)
        self.__menu_version.setText("关于")

        self.__menu_infos.addAction(self.__menu_news)
        self.__menu_infos.addAction(self.__menu_log)
        self.__menu_infos.addAction(self.__menu_version)
        self.__menubar.addAction(self.__menu_functions.menuAction())
        self.__menubar.addAction(self.__menu_infos.menuAction())
        self.setMenuBar(self.__menubar)

        # 状态栏
        self.__statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.__statusbar)
        self.__statusbar.showMessage("就绪")

    # 切换选项卡信号
    def __signal_tab_changed(self):
        self.setFixedSize(*_WINDOW_SIZE[self.__tab.currentIndex()])

    # 程序运行
    def run(self):
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Window()
    ui.run()
    sys.exit(app.exec())
