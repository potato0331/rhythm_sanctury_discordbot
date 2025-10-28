from enum import Enum

# 게임설정값
#BOT_TOKEN을 입력해 둔 채로 commit하지 말것!!!!

INITIAL_COIN = 15
ROUND_COIN = (5,10)

MASTER_ROUND_ON_FIRST_ROUND = 0 # 0 또는 1
MASTER_ROUND_ON_LAST_ROUND = 1 # 0 또는 1

CARD_PRICE = 4

BOT_TOKEN = ""

class Phase(Enum):
    PERPARE = 1
    BETTING = 2
    PENALTY = 3
    CARD = 4