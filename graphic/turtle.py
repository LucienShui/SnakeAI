import turtle


def square_spot(x, y, width, color):
    turtle.up()
    turtle.goto(x, y)
    turtle.color(color)
    turtle.begin_fill()  # 开始填充

    # 开始画图
    for i in range(4):
        turtle.forward(width)
        turtle.right(90)

    turtle.end_fill()  # 填充结束
    turtle.up()
