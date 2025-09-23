import turtle
import math

def hearta(k):
    return 12 * math.sin(k)**3

def heartb(k):
    return 12 * math.cos(k) - 5 * \
          math.cos(2 * k) - 2 * \
          math.cos(3 * k) - \
          math.cos(4 * k)

turtle.speed(9)
turtle.bgcolor("black")
turtle.pensize(2)
turtle.pencolor("red")
turtle.penup()

for i in range(7000):
    turtle.goto(hearta(i) * 20, heartb(i) * 20)
    turtle.pendown()

turtle.done()