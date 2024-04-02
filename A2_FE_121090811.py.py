# import function
import turtle
import random

g_dim = 5
g_color_lis1 = ['red', 'green', 'purple', 'blue', 'yellow']  # color list to draw the color set
g_color_lis2 = ['red', 'green', 'purple', 'blue', 'yellow']  # color list for reference
g_row_lis = []  # a nested list storing the color of each tile
g_position_list = []  # store the x,y coordinates of last clicked tile in the colorboard


# construct a turtle named tt
def init_turtle():
    global tt
    tt = turtle.Turtle()


# init screen as s
def init_screen():
    global s
    s = tt.getscreen()


# draw side 60 square ( 8 operations )
def draw_square():
    for _ in range(4):
        tt.fd(60)
        tt.left(90)


# draw a square with a filling color but without frame
def goto_draw_square(x, y, color):
    tt.penup()
    tt.goto(x, y)
    tt.pendown()

    tt.color('white', color)

    # draw the square and fill in the color
    tt.begin_fill()
    draw_square()
    tt.end_fill()


# draw the black frame around the tile selected
def goto_draw_square_frame(x, y):
    s.tracer(0)

    tt.penup()
    tt.goto(x, y)
    tt.pendown()
    tt.color('black')
    draw_square()

    s.update()


# draw the tile of colorset below
def goto_draw_colorset(x, y):
    tt.penup()
    tt.goto(x, y)
    tt.pendown()
    tt.pensize(2)

    color_lis = g_color_lis1  # copy a color list
    color = color_lis.pop(0)
    tt.color('black', color)  # get random color from the color list, and color the pen

    tt.begin_fill()
    draw_square()
    tt.end_fill()


# draw the board and record the color of each tile.
def draw_the_board(g_row_lis):
    s.tracer(0)

    for i in range(g_dim):
        y = 220 - 65 * i
        column_lis = []
        for j in range(g_dim):
            x = -175 + 65 * j
            color = random.choice(g_color_lis1)
            goto_draw_square(x, y, color)
            column_lis.append(color)
        g_row_lis.append(column_lis)  # record the color of each row

    s.update()


def draw_the_colorset():
    s.tracer(0)

    for n in range(g_dim):
        x = -205 + 61 * n
        goto_draw_colorset(x, -150)

    s.update()


# check if the click is in the board
def check_board_coordinates(x, y):
    flag = False
    symbol = False
    for i in range(5):
        if -175 + 65 * i <= x <= -115 + 65 * i:
            flag = True
    for j in range(5):
        if 220 - 65 * j <= y <= 280 - 65 * j:
            symbol = True
    return flag and symbol


# check if the click is in the colorset
def check_colorset_coordinates(x, y):
    for j in range(5):
        if -205 + 61 * j <= x <= -145 + 61 * j and (-150 <= y <= -100):
            return True
    return False


# change the click position in the colorboard into the left down point of the corresponding tile
def change_coordinates(x, y):
    for n in range(5):
        if -175 + 65 * n <= x <= -115 + 65 * n:
            a = -175 + 65 * n

    for n in range(5):
        if 220 - 65 * n <= y <= 280 - 65 * n:
            b = 220 - 65 * n

    history_data = [a, b]
    return history_data


# find the according row index based on y coordinate
def get_row_index(y):
    global d
    for i in range(5):
        if 220 - 65 * i <= y <= 280 - 65 * i:
            d = i
    return d


# find the according row index based on x coordinate
def get_col_index(x):
    global c
    for i in range(5):
        if -175 + 65 * i <= x <= -115 + 65 * i:
            c = i
    return c


# find the index of g_color_list based on the x coordinate
def get_color_index(x):
    for j in range(5):
        if -205 + 61 * j <= x <= -145 + 61 * j:
            m = j
    return m


# perform 8 useless operation to offset undo operation
def operate_8_operations():
    for j in range(8):
        tt.left(45)


# offset 8 operations of tt, used to undo the black frame if we select another cell or flip color
def offset_8_operations():
    for i in range(8):
        tt.undo()


def flipcolor(x, y, color):
    if color_list[0] == color:
        return

    if x < -175 or x > 85:
        return

    if y < -40 or y > 220:
        return

    if g_row_lis[get_row_index(y)][get_col_index(x)] != color_list[0]:
        return

    goto_draw_square(x, y, color)
    g_row_lis[get_row_index(y)][get_col_index(x)] = color
    operate_8_operations()

    flipcolor(x + 65, y, color)
    flipcolor(x - 65, y, color)
    flipcolor(x, y + 65, color)
    flipcolor(x, y - 65, color)


# write the title
def write():
    s.tracer(0)
    tt.penup()
    tt.goto(-145, 300)
    tt.pendown()
    tt.write("ZHT's flipping color game", font=40)
    s.update()


# clicking in the color board
def step1(x, y):
    if check_board_coordinates(x, y):
        offset_8_operations()

        goto_draw_square_frame(change_coordinates(x, y)[0], change_coordinates(x, y)[1])  # draw black frame
        global color_list
        global g_position_list
        global g_coordinate_list
        color_list = [g_row_lis[get_row_index(change_coordinates(x, y)[1])] \
                          [get_col_index(change_coordinates(x, y)[0])]]
        g_position_list = [change_coordinates(x, y)[0], change_coordinates(x, y)[1]]
        g_coordinate_list = [get_col_index(change_coordinates(x, y)[0]), get_row_index(change_coordinates(x, y)[1])]


# clicking in the colorset
def step2(x, y):
    if check_colorset_coordinates(x, y):
        offset_8_operations()
        color = g_color_lis2[get_color_index(x)]  # get color in the colorset

        if g_position_list:
            flipcolor(g_position_list[0], g_position_list[1], color)

            operate_8_operations()
        else:
            operate_8_operations()


# the whole process
def fun(x, y):
    step1(x, y)
    step2(x, y)


if __name__ == '__main__':
    init_turtle()  # initialize turtle and screen
    init_screen()  # initialize turtle and screen

    tt.hideturtle()

    write()  # write the title

    draw_the_board(g_row_lis)  
    draw_the_colorset()
    operate_8_operations()

    s.onclick(fun)

    s.mainloop()


