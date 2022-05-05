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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration, self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message
        pass


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self):
        super().get_spent_calories()
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2) *
                self.weight / self.M_IN_KM * self.duration * self.HOU_TO_MIN)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        super().get_spent_calories()
        coeff_01 = 0.035
        coeff_02 = 2
        coeff_03 = 0.029
        return (coeff_01 * self.weight +
                (self.get_mean_speed() ** coeff_02 // self.height) *
                coeff_03 * self.weight) * self.duration * self.HOU_TO_MIN


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float
    LEN_STEP: float = field(default=1.38, init=False)

    def get_mean_speed(self) -> float:
        super().get_mean_speed()
        return (self.length_pool * self.count_pool /
                self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        super().get_spent_calories()
        spent_calories_coeff01 = 1.1
        spent_calories_coeff02 = 2
        return ((self.get_mean_speed() + spent_calories_coeff01)
                * spent_calories_coeff02 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        training = Swimming(*data)
        return training
    elif workout_type == 'RUN':
        training = Running(*data)
        return training
    elif workout_type == 'WLK':
        training = SportsWalking(*data)
        return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
