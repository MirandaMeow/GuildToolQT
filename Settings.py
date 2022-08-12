BOSS_HEALTH = {
    1: {"round": 1, "level": 50, "health": 1080000},
    2: {"round": 2, "level": 50, "health": 1080000},
    3: {"round": 3, "level": 55, "health": 1237500},
    4: {"round": 4, "level": 55, "health": 1237500},
    5: {"round": 5, "level": 60, "health": 1500000},
    6: {"round": 6, "level": 60, "health": 1500000},
    7: {"round": 7, "level": 65, "health": 2025000},
    8: {"round": 8, "level": 66, "health": 2640000},
    9: {"round": 9, "level": 67, "health": 3440000},
    10: {"round": 10, "level": 68, "health": 4500000},
    11: {"round": 11, "level": 69, "health": 5765625},
    12: {"round": 12, "level": 70, "health": 7500000},
    13: {"round": 13, "level": 71, "health": 9750000},
    14: {"round": 14, "level": 72, "health": 12000000},
    15: {"round": 15, "level": 73, "health": 16650000},
    16: {"round": 16, "level": 74, "health": 24000000},
    17: {"round": 17, "level": 75, "health": 35000000},
    18: {"round": 18, "level": 76, "health": 50000000},
    19: {"round": 19, "level": 77, "health": 72000000},
    20: {"round": 20, "level": 78, "health": 100000000},
    21: {"round": 21, "level": 79, "health": 140000000},
    22: {"round": 22, "level": 80, "health": 200000000},
    23: {"round": 23, "level": 81, "health": 200000000},
    24: {"round": 24, "level": 82, "health": 200000000},
}
for i in range(25, 61):
    BOSS_HEALTH[i] = {"round": i, "level": 83, "health": 200000000}

BLANK_BATTLE_REPORT = {
    'server_time': 0,
    'log_time': 0,
    'user_name': '',
    'boss': {
        'name': '',
        'level': 0,
        'elemental_type_cn': '',
        'round': 0,
        'remain': 0,
        'state': {}
    },
    'damage': 0,
    'role_list': [{
        'icon': 'https://l1-prod-patch-snake.bilibiligame.net/resources/224/bigfunAssets/9/portraits/none.png',
        'dps': 0,
        'toughness': 0,
        'recovery': 0
    }, {
        'icon': 'https://l1-prod-patch-snake.bilibiligame.net/resources/224/bigfunAssets/9/portraits/none.png',
        'dps': 0,
        'toughness': 0,
        'recovery': 0
    }, {
        'icon': 'https://l1-prod-patch-snake.bilibiligame.net/resources/224/bigfunAssets/9/portraits/none.png',
        'dps': 0,
        'toughness': 0,
        'recovery': 0
    }, {
        'icon': 'https://l1-prod-patch-snake.bilibiligame.net/resources/224/bigfunAssets/9/portraits/none.png',
        'dps': 0,
        'toughness': 0,
        'recovery': 0
    }]
}
