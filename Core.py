import requests

import Misc
from BattleReports import BattleReports


class Core:
    def __init__(self):
        self.__database = Misc.Database("database.db")
        self.__history = Misc.History(self.__database)
        self.__rename = Misc.Rename(self.__database)
        self.__blacklist = Misc.Blacklist(self.__database)
        self.__battle_reports = BattleReports(self.__database)
        self.__session_api = "rstikt0k4sif8536phuusk0ak8"
        self.__headers = {"Cookie": "session-api=" + self.__session_api,
                          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                        "like Gecko) Chrome/91.0.4472.164 Safari/537.36"}
        self.__battle_report_url = "https://www.bigfun.cn/api/feweb?" \
                                   "target=kan-gong-guild-log%2Fa&date=&page=1&size=1350"
        self.__get_battle_reports()

    def __get_battle_reports(self):
        response = requests.get(url=self.__battle_report_url, headers=self.__headers).json()
        self.__battle_reports.set(response, self.__rename.rename)
        self.__battle_reports.get_daily_hits()

    def save_battle_reports(self):
        self.__battle_reports.save()
        self.__history.update()

    def download_icons(self):
        ...
