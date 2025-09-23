import turtle
import math

def hearta(k):
    return 12 * math.sin(k)**3

def heartb(k):
    return 13 * math.cos(k) - 5 * math.cos(2*k) - 2 * math.cos(3*k) - math.cos(4*k)

turtle.speed("fastest")
turtle.bgcolor("black")
turtle.goto(0, 0)
turtle.penup()

for i in range(1000):
    turtle.goto(hearta(i) * 20, heartb(i) * 20)
    turtle.pendown()
    turtle.color("red")
    turtle.goto(0, 0)