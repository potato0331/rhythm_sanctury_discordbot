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

    def __repr__(self) -> str:
        """
        print() 함수 등으로 객체를 출력할 때 표시될 형식을 지정합니다.
        """
        return (
            f"{self.name}\n"
            f"  coin={self.coin}, score={self.score}\n"
            f"  round_score={self.round_score}, round_multiplier={self.round_multiplier}\n"
            f"  effect_list={self.effect_list}\n"
        )
