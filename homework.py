from dataclasses import dataclass


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration} ч.;'
                f' Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч;'
                f' Потрачено ккал: {self.calories}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        pass


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self):
        super().get_spent_calories()
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2 *
                self.weight / self.M_IN_KM * self.duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        super().get_spent_calories()
        coeff_01 = 0.035
        coeff_02 = 2
        coeff_03 = 0.029
        return (coeff_01 * self.weight + (self.get_mean_speed() ** coeff_02 //
                                          self.weight)
                * coeff_03 * self.weight)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self, action, duration, weight, length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

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

    pass


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
