from tkinter import *
from math import *
from random import randrange as rnd, choice, uniform
import time

#Создание окна
root = Tk()
root.geometry('1280x720')

#Создание холста
canv = Canvas(root, bg = 'white')
canv.pack(fill = BOTH, expand = 1)

#Аргументы для ведения счёта
points = 0
mistakes = 0

#Уточнение нашей вселенной
colors = ['red','orange','yellow','green','blue']
X = 1280
Y = 720
r = 50
a = 40

'''
WARNING! Код построен на основе внешнего исходника. Предстоит доработка!
Из доработанного: модернизированы поля результатов, расширено поле, отражение шарика отполировано,
квадратная мишень - лапочка, есть шары-отвлекалки 

на холсте 2 объекта: шарик и квадратик; за попадание в шарик - 1 очко, в квадратик - 5, за промах - +2 к ошибкам
oval_1 - объект шарик
t - текст с количеством очков
nt - с количеством ошибок
square_1 - объект квадратик
move() - функция перемещения шарика
new_square() - функция перемещения квадратика
click() - функция обработки клика и проверки попадания
check_coords() - вспомогательная функция для move(), которая обеспечивает рандомное отражение шарика от стен
vx, vy - актуальнные компоненты скорости шарика

'''

x0 = rnd(r, X-r)
y0 = rnd(r, Y-r)
oval_0 = canv.create_oval(x0 - r, y0 - r, x0 + r, y0 + r, fill = choice(colors), width = 1)

x1 = rnd(r, X-r)
y1 = rnd(r, Y-r)
oval_2 = canv.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill = choice(colors), width = 1)

x2 = rnd(r, X-r)
y2 = rnd(r, Y-r)
oval_3 = canv.create_oval(x2 - r, y2 - r, x2 + r, y2 + r, fill = choice(colors), width = 1)

x = rnd(0, X-a)
y = rnd(0, Y-a)
square_1 = canv.create_rectangle(x, y, x + a, y + a, fill = choice(colors))

x = rnd(r, X-r)
y = rnd(r, Y-r)
oval_1 = canv.create_oval(x - r, y - r, x + r, y + r, fill = choice(colors), width = 1)

def new_square():
    global x, y, points, mistakes, square_1
    canv.itemconfig(t, text = str(points))
    canv.itemconfig(nt, text = str(mistakes))
    x = rnd(r, X-r)
    y = rnd(r, Y-r)
    canv.coords(square_1, x, y, x+40, y+40)     #смещение шарика
    if mistakes > 4:   #проверка; если больше 2 ошибок, то игра закончена
        exit()
    root.after(1000,new_square)

def check_coords(x, y, vy, vx, r):
    a = uniform(0, pi/2)
    v = sqrt(vx*vx + vy*vy)
    if x <= r:
        vx = v * sin(a)
        vy = vy * sqrt(v*v - vx*vx) / abs(vy)
        canv.itemconfig(oval_1, fill = choice(colors))
    if x >= X-r:
        vx = -v * sin(a)
        vy = vy * sqrt(v*v - vx*vx) / abs(vy)
        canv.itemconfig(oval_1, fill = choice(colors))
    if y <= r:
        vy = v * sin(a)
        vx = vx * sqrt(v*v - vy*vy) / abs(vx)
        canv.itemconfig(oval_1, fill = choice(colors))
    if y >= Y-r:
        vy = -v * sin(a)
        vx = vx * sqrt(v*v - vy*vy) / abs(vx)
        canv.itemconfig(oval_1, fill = choice(colors))
    return vx, vy 

vx = 2
vy = 2
t = canv.create_text(X - 100, 50, text = str(points), font = "Verdana 14")
nt = canv.create_text(X - 115, 100, text = str(mistakes), font = "Verdana 14", fill = 'red')

def move():
    global vx,vy,r
    s = canv.coords(oval_1)
    x = (s[0] + s[2]) / 2
    y = (s[1] + s[3]) / 2
    vx, vy = check_coords(x, y, vy, vx, r)
    canv.move(oval_1, vx, vy)           #смещение шарика
    canv.itemconfig(t, text = "Points: " + str(points))
    canv.itemconfig(nt, text = "Mistakes: " + str(mistakes))
    if mistakes > 4:   #проверка; если больше 2 ошибок, то игра закончена
        exit()
    root.after(10,move)

def click(event):
    global points,mistakes
    ans = 0
    s = canv.coords(oval_1)
    x = (s[0] + s[2]) / 2
    y = (s[1] + s[3]) / 2
    s1 = canv.coords(square_1)
    x1 = s1[0]
    y1 = s1[1]
    if (x-event.x)**2 + (y - event.y)**2 <= r**2:   #проверка, что курсор при нажатии находился внутри круга
        points += 1
        ans = 1      # +1 к очкам
    elif ans == 0 and not(event.x-x1 < 40 and event.y - y1 < 40 and event.x-x1 > 0 and event.y - y1 > 0):
        mistakes += 1  # +1 к ошибкам
    if event.x-x1 < 40 and event.y - y1 < 40 and event.x-x1 > 0 and event.y - y1 > 0:
        points += 5
        ans= 1      # +5 к очкам
    elif ans == 0:
        mistakes += 1  # +1 к ошибкам


move()
new_square()
canv.bind('<Button-1>', click)
mainloop()


canv.bind('<Button-1>', click)
#mainloop()