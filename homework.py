from dataclasses import dataclass, field


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Метод возврата результата тренировки.

        Keywords arguments:
        training_type -- тип тренировки
        duration -- продолжительность тренировки в часах
        distance -- пройденая дистанция в КМ
        speed -- скорость в км/ч
        calories -- количество затреченных ккал за тренировку
        """
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: float = field(default=0.65, init=False)
    M_IN_KM: int = field(default=1000, init=False)
    HOU_TO_MIN: int = field(default=60, init=False)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Определите метод get_spent_calories в'
                                  f' {self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration, self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUN_COEF_FIRST: float = 18
    RUN_COEF_SEC: float = 20

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return (
                (self.RUN_COEF_FIRST * self.get_mean_speed()
                 - self.RUN_COEF_SEC)
                * self.weight / self.M_IN_KM * self.duration * self.HOU_TO_MIN
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    SWLK_COEF_FIRST: float = 0.035
    SWLK_COEF_SEC: float = 2
    SWLK_COEF_THIRD: float = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
                (self.SWLK_COEF_FIRST * self.weight
                 + (self.get_mean_speed() ** self.SWLK_COEF_SEC // self.height)
                 * self.SWLK_COEF_THIRD * self.weight) * self.duration
                * self.HOU_TO_MIN
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float
    LEN_STEP: float = field(default=1.38, init=False)
    SWM_COEF_FIRST: float = 1.1
    SWM_COEF_SEC: float = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        super().get_mean_speed()
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.SWM_COEF_FIRST)
                * self.SWM_COEF_SEC * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        training_dict = {
            'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking,
        }
        return training_dict.get(workout_type)(*data)
    except TypeError:
        print('[-] В словаре нету указаного вами кода тренировки.')


def main(training: Training) -> None:
    """Главная функция."""
    try:
        print(training.show_training_info().get_message())
    except AttributeError:
        print('[-] Передано неправильное количество атрибутов.')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
