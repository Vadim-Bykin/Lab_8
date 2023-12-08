
from itertools import combinations
from random import randint
from tkinter import *


# профессионалы
class Prof:
    def __init__(self, name, score):
        self.name = name
        self.score = score

# любители
class Jun:
    def __init__(self, name, score):
        self.name = name
        self.score = score


class Team:
    def __init__(self, people):
        self.COUNT = 4
        self.juns = []
        self.profs = []
        self.JUN_MAX_SCORE = 1000
        self.PROF_MIN_SCORE = 2400
        self.commands = []
        self.selected_commands = []
        self.distribution(people)
        self.form()

    def distribution(self, a):  # распределение любителей и профессионалов
        for i in a:
            if i[1] <= self.JUN_MAX_SCORE:
                self.juns.append(Jun(i[0], i[1]))
            elif i[1] >= self.PROF_MIN_SCORE:
                self.profs.append(Prof(i[0], i[1]))

    def form(self):  # формирование команды
        for i in range(self.COUNT + 1):
            for prof in combinations(self.profs, i):
                for jun in combinations(self.juns, self.COUNT - i):
                    cur_command = prof + jun
                    cur_score = 0
                    for item in cur_command:
                        cur_score += int(item.score)
                    self.commands.append([cur_command, cur_score, i, self.COUNT - i])

    def select_commands(self, count_juns, count_profs):  # вывод команды согласно условию
        for command in self.commands:
            if command[2] < count_profs:
                continue
            elif command[3] < count_juns:
                continue

            self.selected_commands.append(command)

        return self.selected_commands

    def select_best_commands(self):  # целевая функция
        max_score = 0
        best_commands = []
        for cur_command in self.selected_commands:
            if cur_command[1] > max_score:
                max_score = cur_command[1]

        for cur_command in self.selected_commands:
            if cur_command[1] == max_score:
                best_commands.append(cur_command)

        return best_commands


def start():  # реализация графического интерфейса
    text.delete('1.0', END)

    # список профессионалов (имена для удобства начинаются на П) и любителей (имена для удобства начинаются на Л)
    team = Team([['Петр', randint(2400, 2900)], ['Павел', randint(2400, 2900)], ['Полина', randint(2400, 2900)],
                 ['Пелагея', randint(2400, 2900)], ['Прохор', randint(2400, 2900)], ['Лёня', randint(0, 1000)],
                 ['Люба', randint(0, 1000)], ['Людмила', randint(0, 1000)], ['Лев', randint(0, 1000)],
                 ['Лаврентий', randint(0, 1000)]])

    try:  # обработка исключений, если пользователь введёт некоректные данные
        p = int(profs.get())
        j = int(juns.get())
    except ValueError:
        text.insert(END, 'Введены не числа')
        return
    if p < 0 or j < 0:
        text.insert(END, 'Введено(-ы) отрицательное(-ые) число(-а)')
        return
    else:  # если данные корректны - вывод результатов работы программы
        select_teams = team.select_commands(j, p)
        text.insert('1.0', f"Все команды, удовлетворяющие условиям (не менее {profs.get()} профессионалов и не менее {juns.get()} любителя):\n")
        if len(select_teams) == 0:
            text.insert(END, "Команд, удовлетворяющих условиям не найдено")
        else:
            for i in select_teams:
                answ = ''
                for j in i[0]:
                    answ += j.name + ' '
                answ += ' - ' + str(i[1])
                text.insert(END, answ + '\n')
            text.insert(END, '-----------------\n')
            text.insert(END, 'Самые лучшие команды:\n')
            text.insert(END, 'Состав игроков, общий рейтинг команды\n')
            for i in team.select_best_commands():
                answ = ''
                for j in i[0]:
                    answ += j.name + ' '
                answ += ' -' + str(i[1])
                text.insert(END, answ + '\n')



windowEntry = Tk()
windowEntry.title('Lab 8')


info = Label(windowEntry, text=' Команда для игры в гольф должна состоять из 4 членов.\n'
                               ' Имеется 5 профессионалов и 5 любителей.\n'
                               ' В поле Juns напишите кол-во любителей, а в поле Profs кол-во профес.\n'
                               ' Нажмите на кнопку "Вывести" чтобы вывести все подходящие под условие команды\n'
                               ' Для повторного запуска нажмите кнопку "Вывести" еще раз')
label_juns = Label(windowEntry, text='Juns: ')
juns = Entry(windowEntry)
label_profs = Label(windowEntry, text='Profs: ')
profs = Entry(windowEntry)
start = Button(windowEntry, text='Вывести', command=start)
text = Text(windowEntry, width=70)
scrollbar = Scrollbar(orient="vertical", command=text.yview)


info.pack()
label_juns.pack()
juns.pack()
label_profs.pack()
profs.pack()
start.pack(pady=10)
text.pack()
scrollbar.place(x=682, y=205, height=390)
text["yscrollcommand"] = scrollbar.set
windowEntry.geometry('800x700')
windowEntry.mainloop()
