class Skill:
    def __init__(self, name: str, cost: int, effect: dict[str, int]) -> None:
        self.name = name
        self.cost = cost
        self.effect = effect