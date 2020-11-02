from random import randrange as rnd, choice
import tkinter as tk
import math as m
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = rnd(15, 30)
        self.vx = 10
        self.vy = 10
        self.gr = 1.5
        self.color = choice(['brown', 'pink', 'red', 'yellow'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def create_ball(self):
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move_ball(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x > 800 - self.r:
            self.vx = - self.vx / 2
            self.x = 799 - self.r
        if self.y >= 600 - self.r:
            self.vy = int(- self.vy / 2.25)
            self.vx = self.vx / 1.25
            self.y = 600 - self.r
        if self.x < self.r:
            self.vx = - self.vx / 2
            self.x = self.r + 1
        if self.y < self.r:
            self.vy = int(- self.vy / 2.25)
            self.vx = self.vx / 1.25
            self.y = self.r + 1
        if abs(self.vy) < 1.5 and self.y > 599 - self.r:
            self.vx = 0
            self.vy = 0
            self.gr = 0
        self.x += self.vx
        self.y -= self.vy
        self.vy -= self.gr

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if m.sqrt(abs(self.x - obj.xcoor()) ** 2 + abs(self.y - obj.ycoor()) ** 2) < self.r + obj.rad():
            return True
        else:
            return False

    def clear_ball(self):
        canv.delete(self.id)


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = m.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * m.cos(self.an)
        new_ball.vy = - self.f2_power * m.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = m.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * m.cos(self.an),
                    450 + max(self.f2_power, 20) * m.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def __init__(self):
        self.points = 0
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.id_points = canv.create_text(30, 30, text='', font='28')
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.vy = rnd(- 7, 7)
        self.vx = rnd(- 7, 7)
        self.r = rnd(20, 40)
        self.y = rnd(300, 500 - self.r)
        self.x = rnd(500, 800 - self.r)
        self.color = choice(('green', 'blue', 'cyan', 'violet'))
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        canv.itemconfig(self.id, fill=self.color)

    def move_target(self):
        if self.y < self.r or self.y > 499 - self.r:
            self.vy = - self.vy
        if self.x < 300 + self.r or self.x > 799 - self.r:
            self.vx = - self.vx
        self.x += self.vx
        self.y -= self.vy

    def create_target(self):
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )

    def clear_target(self):
        canv.delete(self.id)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points

    def xcoor(self):
        return self.x

    def ycoor(self):
        return self.y

    def rad(self):
        return self.r

    def score(self):
        return self.points

    def idscore(self):
        return self.id_points

t1 = target()
t2 = target()
t3 = target()
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
balls = []


def new_game(event=''):
    global gun, t1, screen1, balls, bullet
    t1.new_target()
    t2.new_target()
    t3.new_target()
    t1.clear_target()
    t2.clear_target()
    t3.clear_target()
    bullet = 0
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    t1.live = 1
    t2.live = 1
    t3.live = 1
    while t1.live or t2.live or t3.live or balls:
        clear = []
        t1.move_target()
        t2.move_target()
        t3.move_target()
        if t1.live != 0:
            t1.create_target()
        if t2.live != 0:
            t2.create_target()
        if t3.live != 0:
            t3.create_target()
        for i in range(len(balls)):
            balls[i].move_ball()
            if balls[i].hit_test(t1) and t1.live:
                t1.live -= 1
                t1.hit()
            if balls[i].hit_test(t2) and t2.live:
                t2.live -= 1
                t2.hit()
            if balls[i].hit_test(t3) and t3.live:
                t3.live -= 1
                t3.hit()
            if t1.live == 0 and t2.live == 0 and t3.live == 0:
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
                canv.itemconfig(t1.idscore(), text=str(t1.score()))
            balls[i].create_ball()
            if balls[i].vx == 0 and balls[i].vy == 0:
                if balls[i].live == 0:
                    balls[i].clear_ball()
                    clear.append(i)
                else:
                    balls[i].live -= 1
        for i in clear:
            del balls[i]

        canv.update()
        time.sleep(0.03)
        for b in balls:
            b.clear_ball()
        t1.clear_target()
        t2.clear_target()
        t3.clear_target()
        g1.targetting()
        g1.power_up()

    canv.delete(gun)
    canv.itemconfig(screen1, text='')

new_game()

while True:
    new_game()
