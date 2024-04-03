"""Модуль с утилитами - вспомогательными скриптами для работы бота."""


class StatsCalculator:
    __base_stats = {
        'Сила': 8,
        'Ловкость': 8,
        'Телосложение': 8,
        'Интелект': 8,
        'Мудрость': 8,
        'Харизма': 8
    }
    __modifiers = {
        8: 0,
        9: 1,
        10: 2,
        11: 3,
        12: 4,
        13: 5,
        14: 7,
        15: 9
    }
    __base_count = 27

    def __init__(self):
        self.stats = self.__base_stats
        self.count_stats = self.__base_count

    async def change_stat(self, new_value: int, old_value: int, count_stats: int) -> (str, str):
        if old_value != new_value:
            count_stats -= self.__modifiers[new_value]
            old_value = new_value
        return str(old_value), str(count_stats)

    async def get_possible_stats(self, count) -> list[str]:
        return [str(k) for k, v in self.__modifiers.items() if count - v >= 0]


class StatsRandomizer:
    pass


stats_calculator = StatsCalculator()
