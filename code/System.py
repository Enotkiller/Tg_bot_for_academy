import datetime
import calendar
from .DataBase import base
from zoneinfo import ZoneInfo

class system(base):
    def __init__(self):
        super().__init__()
        self.cancellation = [0, 0, 0]

    def get_pair(self, number = 0, day_week = 0):
        """
        Получение пары за заданым номером в заданый день.
        :param number: Номер пары.
        :param day_week: День недели.
        :return: В текстовом виде, какая сейчас пара за задаными параметрами.
        """

        if number != 0 and day_week != 0 and day_week <= 5 and number <= 4 and number >= -4:
            if number < 0:
                number = number * -1
            return self.schedule[day_week][number]
        return None

    def get_pair_now(self):
        """
        Получение нынешней пары в данный момент времени.
        :return: В текстовом виде. Но если сейчас пары нет то вернет None.
        """

        return self.get_pair(self.reverse_pair_number_for_type_week(), self.get_day_weekly_now())

    def get_day_weekly_now(self):
        """
        Получение дня недели.
        :return: Возвращает какой по счету день недели, если понедельник то 1, если вторник то 2 и так далее.
        """

        return datetime.datetime.now().isoweekday()

    def get_day_weekly(self, mounth = 0, day = 0):
        """
        Получение дня недели за заданым нем и месяцом.
        :param mounth: Месяц.
        :param day: Число месяца, типо 02 10 месяца.
        :return: Возвращает какой по счету день недели, если понедельник то 1, если вторник то 2 и так далее.
        """

        if mounth != 0 and day != 0:
            year = int(datetime.datetime.now().strftime("20%y"))
            date = datetime.date(year, mounth, day)
            return date.isoweekday()

    def get_pair_number_now(self):
        """
        Возвращает какая сейчас пара по укр времени.
        :return: Вернет номер пары, а если число минусовое то это означает что перемена перед парой.
        """

        time = self.get_time_float()
        if time >= 8.0 and time <= 9.49:
            if time >= 8.0 and time <= 8.30:
                return -1
            else:
                return 1
        elif time >= 9.50 and time <= 11.20:
            if time >= 9.50 and time <= 9.59:
                return -2
            else:
                return 2
        elif time >= 11.20 and time <= 13.20:
            if time >= 11.20 and time <= 11.59:
                return -3
            else:
                return 3
        elif time >= 13.20 and time <= 14.50:
            if time >= 13.20 and time <= 13.29:
                return -4
            else:
                return 4
        return 0

    def get_pair_number_now_without_type(self):
        """
        :return: Возвращает какая сейчас или будет пара без её типа.
        """

        return self.get_pair_number_now() if not self.get_pair_number_type(self.get_pair_number_now()) else self.get_pair_number_now() * -1

    def reverse_pair_number_for_type_week(self):
        """
        :return: Вернет номер пары с сразу правельным вариантом, если get_week_type скажит что сейчас тип недели 1 то вернет целое число и не минусовое, а если тип недели 0 то вернет не целое число а с .5 на конце.
        """

        pair_number = self.get_pair_number_now()
        week_type = self.get_week_type()
        if week_type == 0:
            return float(pair_number + 0.5) if not self.get_pair_number_type(self.get_pair_number_now()) else float(pair_number * -1 + 0.5)
        else:
            return pair_number if not self.get_pair_number_type(self.get_pair_number_now()) else pair_number * -1

    def get_week_type(self, now = 0, day = 10, mounth = 2):
        """
        Вычисляет тип недели за счет того что считает от заданой даты до нынешней понедельники, и если попадётся понедельник то поменяет now на обратное значение.
        :param now: Тип недели заданого числа.
        :param day: Ставить понедельник данной недели.
        :param mounth: Месяц.
        :return: Вернет now после всех вычислений.
        """

        when_mounth, when_day = mounth, day
        mounth = int(datetime.datetime.now().strftime("%m"))
        day = int(datetime.datetime.now().strftime("%d"))
        year = int(datetime.datetime.now().strftime("20%y"))
        now = int(1) if now == 0 else int(0)
        for i in range(mounth - when_mounth + 1):
            for j in range(1, calendar.monthrange(year, i + when_mounth)[1] + 1):
                if i == 0 and j <= when_day - 1:
                    pass
                else:
                    if self.get_day_weekly(when_mounth + i, j) == 1:
                        if now == 0:
                            now = 1
                        else:
                            now = 0
                    if i + when_mounth == mounth and j >= day:
                        break
        return now

    def get_pair_number_type(self, number = 0):
        """
        :param number: сюда результат от функции get_pair_number_now, или самому.
        :return: Если перемена то вернет True, если нет то False.
        """

        if number != 0:
            if number < 0:
                return True
            else:
                return False

    def get_time_now(self):
        """
        :return: Время в datetime по Украине.
        """

        time_zone = ZoneInfo("Europe/Kiev")
        time_now = datetime.datetime.now(time_zone)
        return time_now

    def get_time_str(self):
        """
        :return: Возвращает время в str, пример - "20:31"
        """

        time = self.get_time_now()
        return f"{str(time.hour):{str(time.minute)}}"

    def get_time_float(self):
        """
        :return: Возвращает время в float, пример - 20.31
        """

        time = self.get_time_now()
        return float(float(time.hour) + (float(time.minute) / 100))

    def get_url_pair(self):
        """
        :return: Возвращает ссылку на пару котороя сейчас.
        """

        pair = self.get_pair_now()
        return self.url[pair]

    def set_cancellation_on_pair(self):
        """
        Ставит значение "отмены пары" на 1
        """

        self.cancellation = [1, self.get_pair_number_now_without_type(), self.get_day_weekly_now()]

    def get_cancellation(self):
        """
        Проверяет если пара поменялась то сбрасывает все значение у "отмены пары"
        :return: Вернет True если ещё действует отмена пары, а если пара поменялась то False
        """

        if self.cancellation[1] == self.get_pair_number_now_without_type() and self.cancellation[2] == self.get_day_weekly_now():
            return True
        else:
            self.cancellation = [0, 0, 0]
            return False