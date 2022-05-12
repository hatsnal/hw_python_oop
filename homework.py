from dataclasses import dataclass, field, asdict, fields
from typing import ClassVar


class Bcolors:
    """Класс, окрашивающий строку"""

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Метод возврата результата тренировки."""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = field(default=0.65, init=False)
    M_IN_KM: ClassVar[int] = field(default=1000, init=False)
    HOU_TO_MIN: ClassVar[int] = field(default=60, init=False)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Определите метод get_spent_calories в'
                                  f'{self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration, self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    RUN_COEF_FIRST: ClassVar[float] = 18
    RUN_COEF_SEC: ClassVar[float] = 20

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return ((self.RUN_COEF_FIRST * self.get_mean_speed()
                 - self.RUN_COEF_SEC)
                * self.weight / self.M_IN_KM * self.duration * self.HOU_TO_MIN)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    SWLK_COEF_FIRST: ClassVar[float] = 0.035
    SWLK_COEF_SEC: ClassVar[float] = 2
    SWLK_COEF_THIRD: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.SWLK_COEF_FIRST * self.weight
                 + (self.get_mean_speed() ** self.SWLK_COEF_SEC // self.height)
                 * self.SWLK_COEF_THIRD * self.weight) * self.duration
                * self.HOU_TO_MIN)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: float
    LEN_STEP: ClassVar[float] = field(default=1.38, init=False)
    SWM_COEF_FIRST: ClassVar[float] = 1.1
    SWM_COEF_SEC: ClassVar[float] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.SWM_COEF_FIRST)
                * self.SWM_COEF_SEC * self.weight)


TRAINING_DICT = {
    'SWM': (Swimming, len(fields(Swimming))),
    'RUN': (Running, len(fields(Running))),
    'WLK': (SportsWalking, len(fields(SportsWalking))),
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_class, class_atrr_len = TRAINING_DICT.get(workout_type)
    if workout_type not in TRAINING_DICT:
        raise 'Код тренировки не найден в словаре'

    if class_atrr_len != len(data):
        raise 'Неправильное количество аргументов в data'

    return training_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
