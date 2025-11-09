from enum import Enum

# 게임설정값
# BOT_TOKEN을 입력해 둔 채로 commit하지 말것!!!!

INITIAL_COIN = 15
ROUND_COIN = (5,10)

MASTER_ROUND_ON_FIRST_ROUND = 0 # 0 또는 1
MASTER_ROUND_ON_LAST_ROUND = 1 # 0 또는 1

CARD_PRICE = 4

BOT_TOKEN = ""
SAVE_FILE = "game_state.pkl"

class Tag(Enum):
    TARGET = 1 #무언가 대상을 지정해야 하는 경우
    EFFECT = 2 #효과에 무언가 지정해야하는 것이 있는 경우
    SHARED = 3 #77.77등 라운드 자체에 적용돼는 효과들
    ALL = 4 #효과룰렛처럼 모든 플레이어를 대상으로 적용돼는 효과들
    

class Phase(Enum):
    READY = 0
    PREPARE = 1
    BETTING = 2
    PENALTY = 3
    CARD = 4
    RESULT = 5