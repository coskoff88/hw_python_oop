class InfoMessage:
    """Информационное сообщение о тренировке."""
    message = ('Тип тренировки: {training_type}; Длительность: {duration} ч.;'
               ' Дистанция: {distance} км; Ср. скорость: {speed} км/ч;'
               ' Потрачено ккал: {calories}.')

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.distance = str('%.3f' % distance)
        self.speed = str('%.3f' % speed)
        self.calories = str('%.3f' % calories)
        self.duration = str('%.3f' % duration)

    def get_message(self):
        """Форматированной строки."""
        return self.message.format(training_type=self.training_type,
                                   duration=self.duration,
                                   distance=self.distance,
                                   speed=self.speed,
                                   calories=self.calories)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: int = 0.65
    M_IN_KM: float = 1000
    M_IN_HOUR: int = 60

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
        value_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return value_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        value_mean_speed = self.get_distance() / self.duration
        return value_mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вывод сообщения о тенировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        value_spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                 * self.get_mean_speed()
                                + self.CALORIES_MEAN_SPEED_SHIFT)
                                * self.weight / self.M_IN_KM
                                * (self.duration * self.M_IN_HOUR))
        return value_spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_MEAN_WEIGHT_SHIFT: float = 0.029
    КМH_IN_MSEC: float = 0.278
    SM_IN_M: int = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        value_spent_calories = ((self.CALORIES_MEAN_WEIGHT_MULTIPLIER
                                 * self.weight + (((self.get_mean_speed()
                                                  * self.КМH_IN_MSEC)**2)
                                                  / (self.height
                                                  / self.SM_IN_M))
                                 * self.CALORIES_MEAN_WEIGHT_SHIFT
                                 * self.weight) * (self.duration
                                                   * self.M_IN_HOUR))
        return value_spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_MEAN_SPEED_SW_MULTIPLIER: float = 1.1
    CALORIES_MEAN_WEIGHT_SW_SHIFT: int = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        value_mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                            / self.duration)
        return value_mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        value_spent_calories = ((self.get_mean_speed()
                                + self.CALORIES_MEAN_SPEED_SW_MULTIPLIER)
                                * self.CALORIES_MEAN_WEIGHT_SW_SHIFT
                                * self.weight * self.duration)
        return value_spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in training_dict:
        training_object = training_dict[workout_type](*data)
        return training_object
    else:
        raise ('Тренировка не найдена')


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
