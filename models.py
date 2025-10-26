class Card:
    def __init__(self, id: int, name: str, type: int, description: str, image_file: str, effect_tag: str, betting_value: int, card_count: int):
        self.id = id
        self.name = name
        self.type = type #메리트=1, 리스크=2, 패널티=3
        self.description = description
        self.effect_tag = effect_tag #player.effectlist에 추가할 내용
        self.image_file = image_file
        self.betting_value = betting_value
        self.card_count = card_count

class RoundSong:
    """
    전반/후반에 등록한 곡과 페널티의 정보입니다.
    """
    def __init__(self, song_name: str, song_level: str, round_penalty: str):
        self.song_name: str = song_name
        self.song_level: str = song_level
        self.round_penalty: str = round_penalty
    
    def __repr__(self) -> str:
        return f"{self.song_name}/{self.song_level}/{self.round_penalty}"

class Player:
    """
    게임에 참여하는 플레이어의 상태를 저장하는 클래스입니다.
    """
    def __init__(self, name: str, initial_coin: int):
        self.name: str = name
        self.coin: int = initial_coin
        self.score: int = 0
        self.round_score: int = 0
        self.round_multiplier: int = 0
        self.effect_list: list[str] = []
        self.first_half: RoundSong = RoundSong(song_name = "", song_level = "", round_penalty = "")
        self.second_half: RoundSong = RoundSong(song_name = "", song_level = "", round_penalty = "")
        self.betting: int = 0

    def __repr__(self) -> str:
        """
        print() 함수 등으로 객체를 출력할 때 표시될 형식을 지정합니다.
        """
        return (
            f"{self.name}\n"
            f"  coin={self.coin}, betting={self.betting}, score={self.score}\n"
            f"  round_score={self.round_score}, round_multiplier={self.round_multiplier}\n"
            f"  effect_list={self.effect_list}\n"
            f"  first_half={self.first_half}\n"
            f"  second_half={self.second_half}\n"
        )
