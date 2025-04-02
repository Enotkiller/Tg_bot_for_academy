from datetime import timedelta, datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
import asyncio
import System
from zoneinfo import ZoneInfo

dp = Dispatcher()

class bot_aiogram(System.system):
    def __init__(self):
        super().__init__()
        API_TOKEN = None
        chat_id = None
        test_chat_id = None
        self.id_admin = []
        self.bot = Bot(token = API_TOKEN)
        self.days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]

    @dp.message(Command("para"))
    async def send_pair(self, message: Message, command: CommandObject):
        """
        Отправляет какая сейчас пара, время, перемена или нет и ссылку на пару. Можно написать в параметры к команде all - выведет всё расписание на сегодня, и next - расписание на завтра.
        :param command: Сдесь параметры для функции.
        """

        args = (command.args.split()) if command.args != None else (command.args)
        if args == None:
            print(message.from_user.username, message.from_user.id)
            if self.get_day_weekly_now() <= 5 and self.get_time_float() <= 14.50:
                await message.answer(
                    f"{self.days[self.get_day_weekly_now()]}\nТекущее время: {self.get_time_str()}\n{"Текущая" if not self.get_pair_number_type(self.get_pair_number_now()) else "Будет"} пара: {self.get_pair_now()}\nСтатус: {(("Отпустили" if self.get_cancellation() == True else "Перемена" if self.get_pair_number_type(self.get_pair_number_type()) else ("Идёт")))}\nСсылка: {self.get_url_pair()}")
            else:
                await message.answer("Какие уроки челл.")
        elif args[0].lower() == "all":
            await message.answer(
                f"{self.days[self.get_day_weekly_now()]}\n1: {self.get_pair(1, self.get_day_weekly_now())}\n2: {self.get_pair(2, self.get_day_weekly_now())}\n3: {self.get_pair(3, self.get_day_weekly_now())}\n4: {self.get_pair(4, self.get_day_weekly_now())}")
        elif args[0].lower() == "next":
            await message.answer(
                f"{self.days[self.get_day_weekly_now() + 1]}\n1: {self.get_pair(1, self.get_day_weekly_now())}\n2: {self.get_pair(2, self.get_day_weekly_now())}\n3: {self.get_pair(3, self.get_day_weekly_now())}\n4: {self.get_pair(4, self.get_day_weekly_now())}")

    @dp.message(Command("otmena"))
    async def otmena_pari(self, message: Message):
        """
        Ставит статус отмены если ID пользователя есть в списке с ID админами.
        """

        if message.from_user.id in self.id_admin:
            self.set_cancellation_on_pair()
            text = "Параметр: <b>Отмена Пары</b> успешно поставлен!"
            await message.answer(text, parse_mode=ParseMode.HTML)

    @dp.message(Command("pingme"))
    async def pingme(self, message: Message):
        """
        Добавляет в файл ping.txt, и перед парой будет пинговать. А если ещё раз использовать то удаляет.
        """

        self.load_in_file(message.from_user.id, message.from_user.username)

    @dp.message(Command("pingwho"))
    async def pingwho(self, message: Message):
        """
        Выводит всех кого будет пинговать перед парой.
        """

        self.read_file()
        if len(self.all) == 0:
            await message.answer("Нет кого пинговать.")
        else:
            text = "Вот всё кого будет пинговать: " + self.username[0]
            if len(self.username) > 1:
                for i in range(1, len(self.username)):
                    text = f"{text}, {self.username[i]}"
            await message.reply(text)

    async def send_message(self):
        """
        Сдесь происходит отправка сообщение перед парой в чат который задан в chat_id
        """

        if not self.get_day_weekly_now() in [6, 7]:
            try:
                self.read_file()
                username = self.username
                text = "@" + username[0]
                print(username, len(username))
                if len(username) > 1:
                    for i in range(1, len(username)):
                        text = f"{text} @{username[i]}"
                await self.bot.send_message(chat_id=self.chat_id,
                                       text=f"Пара некст - {self.get_pair_now()}.\nСсылка - {(self.get_url_pair()) if self.get_pair_now() != "Пары нет" else None}.")
                await self.bot.send_message(chat_id=self.chat_id, text=f"Пинг: {text}")
                print(f"Сообщение отправлено в {datetime.now().strftime('%H:%M:%S')}")
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")

    async def scheduler(self, target_times: list):
        """
        Вызывает функцию send_message если сейчас время есть в списке target_times.
        :param target_times: Список с временем когда отпралять сообщение
        """

        utc_plus_2 = ZoneInfo("Europe/Kiev")
        while True:
            now = datetime.now(utc_plus_2)
            future_targets = []
            for time_str in target_times:
                target_hour, target_minute = map(int, time_str.split(":"))
                target = now.replace(
                    hour=target_hour,
                    minute=target_minute,
                    second=0,
                    microsecond=0
                )
                if now > target:
                    target += timedelta(days=1)
                future_targets.append(target)
            next_target = min(future_targets)
            wait_seconds = (next_target - now).total_seconds()
            print(f"Ожидание до {next_target.strftime('%H:%M')} UTC+2 ({wait_seconds:.0f} секунд)")
            await asyncio.sleep(wait_seconds)
            await self.send_message()

    async def on_startup(self):
        """
        Задает список для scheduler.
        """

        asyncio.create_task(self.scheduler(["08:28", "09:58", "11:58", "13:25"]))

    async def start(self):
        """
        Стартует и бота, и авто отправку сообщений.
        """

        await self.on_startup()
        await dp.start_polling(self.bot)

if __name__ == "__main__":
    asyncio.run(bot_aiogram().start())
