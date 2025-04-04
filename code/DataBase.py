class base:
    def __init__(self):
        self.read_file()
        self.read_schedule()
        self.read_url()

    def read_file(self):
        """
        Читает .txt файл.
        :return: Словарь с списками всех: id, username.
        """

        self.all = []
        self.id = []
        self.username = []
        with open("code/ping.txt", "r") as file:
            for i in file.read().split("\n"):
                if i != '':
                    print(i)
                    self.all.append(i.split(" "))
                    self.id.append(i.split(" ")[0])
                    self.username.append(i.split(" ")[1])
        return {"all" : self.all, "id" : self.id, "username" : self.username}

    def load_in_file(self, id = None, username = None):
        """
        Сохраняет в файл: id, username. А если он уже записан то стирает его из памяти.
        :param id: ID пользователя которого надо сохранить или удалить.
        :param username: USERNAME пользователя которого надо сохранить или удалить.
        :return: Если он смог записать или удалить то вернет True, если нет то False.
        """

        self.read_file()
        if id != None and username != None:
            if not str(id) in self.id:
                with open("code/ping.txt", "a") as file:
                    if len(self.all) > 0:
                        file.write(f"\n{id} {username}")
                    else:
                        file.write(f"{id} {username}")
            else:
                with open("code/ping.txt", "w"):
                    pass
                mass = self.all
                self.all = []
                self.id = []
                self.username = []
                for i in mass:
                    q = []
                    for j in i:
                        if j == str(id) or j == str(id):
                            break
                        else:
                            q.append(j)
                    if q != []:
                        with open("ping.txt", "a") as f:
                            f.write(f"{"\n"if len(self.all) != 0 else ""}{q[0]} {q[1]}")
                        self.username.append(q[1])
                        self.id.append(q[0])
                        self.all.append(q)
            return True
        else:
            return False

    def check_user_in_file(self, id = None, username = None):
        """
        Проверка есть ли пользователь в файле.
        :param id: ID пользователя которого проверить есть ли он в файле.
        :param username: USERNAME пользователя которого проверить есть ли он в файле.
        :return: True если есть, False если нету.
        """

        self.read_file()

        if id != None:
            if id in self.id:
                return True
            else:
                False
        elif username != None:
            if username in self.username:
                return True
            else:
                return False

    def read_schedule(self):
        """
        Читает Schedule.txt
        :return: Рассписание которое написано в файле.
        """

        with open("code/Schedule.txt", "r", encoding="utf-8") as file:
            self.schedule = eval(file.read())
        return self.schedule

    def replace_schedule(self):
        """
        Поменять расписание в Schedule.txt на то которое сейчас в self.shedule
        """

        with open("code/Schedule.txt", "w") as file:
            file.write(self.schedule)

    def read_url(self):
        """
        Читает Url.txt
        :return: Вернет словарь с ссылками на уроки.
        """

        with open("code/Url.txt", "r", encoding="utf-8") as file:
            self.url = eval(file.read())
            return self.url

    def replace_url(self):
        """
        Поменять расписание в Url.txt на то которое сейчас в self.url
        """

        with open("code/Url.txt", "w") as file:
            file.write(self.url)


