from tkinter import *
from tkinter.font import *
import random

"""pyinstaller boom.py  -F -w -i 源码.ico"""

gamerow = 20
gamecol = 20
gameboom = 40
# from tkinter.ttk import *
first = True
win_or_no = None
window = Tk()
window.resizable(0, 0)
window.geometry("+0+0")
# photo = PhotoImage(file="boom.png")
# TODO:图片丫
flags = []
colors = []
window.title(f"扫雷{gamerow}x{gamecol}版（{gameboom}雷）")
window.iconbitmap("error")


# 获取屏幕宽度和高度
# font = Font(family='DroidSansMono NF')
def build_game(user_touch, row, col, boom):
    canchose = []
    res = []
    for x in range(row):
        for y in range(col):
            canchose.append((x, y))
    canchose.remove(user_touch)
    choses = random.sample(canchose, boom)
    for x in range(row):
        temp = []
        for y in range(col):
            temp.append("boom" if (x, y) in choses else "air")
        res.append(temp)
    print("\n".join([" ".join(x) for x in res]))
    return (res, choses)


def make_a_flag(self, row, col):
    if win_or_no is None:
        if (row, col) in flags:
            self["bg"] = colors[flags.index((row, col))]
            del colors[flags.index((row, col))]
            flags.remove((row, col))
        else:
            flags.append((row, col))
            colors.append(self["bg"])
            self["bg"] = "red"


def fan(self, row, col, path=None):
    global win_or_no
    if win_or_no is None:
        if (row, col) not in flags:
            if path is None:
                path = []
            global game_board
            path += [(row, col)]
            global first
            if first:
                game_board = build_game((row, col), gamerow, gamecol, gameboom)
                first = False
            self["bg"] = "gray"
            if game_board[0][row][col] == "boom":
                # self["image"] = photo
                # TODO:图片！！！
                self["text"] = "雷"
                win_or_no = False
                tips["text"] = "你输了"
                show()
            else:
                count_boom = 0
                for boom_x in range(-1, 2):
                    for boom_y in range(-1, 2):
                        if -1 < row + boom_x < gamerow and -1 < col + boom_y < gamecol:
                            if game_board[0][row + boom_x][col + boom_y] == "boom":
                                count_boom += 1
                if count_boom > 0:
                    self["text"] = str(count_boom)
                # else:
                #     for boom_x in range(-1, 2):
                #         for boom_y in range(-1, 2):
                #             if -1 < row + boom_x < gamerow and -1 < col + boom_y < gamecol:
                #                 if (row + boom_x, col + boom_y) not in path:
                #                     if game_board[0][row + boom_x][col + boom_y] != "boom":
                #                         fan(eval(f"btn{str(row + boom_x)}_{str(col + boom_y)}"), row + boom_x,
                #                             col + boom_y,
                #                             path)
                # else:
                for boom_x in range(-1, 2):
                    for boom_y in range(-1, 2):
                        if -1 < row + boom_x < gamerow and -1 < col + boom_y < gamecol:
                            if (row + boom_x, col + boom_y) not in path:
                                if game_board[0][row + boom_x][col + boom_y] != "boom":
                                    fan(eval(f"btn{str(row + boom_x)}_{str(col + boom_y)}"), row + boom_x,
                                        col + boom_y,
                                        path)


game = Frame(
    master=window,
    relief=RAISED,
    borderwidth=1
)
for i in range(gamerow):
    for j in range(gamecol):
        frame = Frame(
            master=game,
            relief=SUNKEN,
            borderwidth=1
        )
        frame.grid(row=i, column=j, padx=0, pady=0)

        exec(f"""
btn{i}_{j} = Button(master=frame, height=1, width=3)
btn{i}_{j}.bind("<Button-1>",lambda event:fan(btn{i}_{j},{i},{j}))
btn{i}_{j}.bind("<Button-2>",lambda event:make_a_flag(btn{i}_{j},{i},{j}))
btn{i}_{j}.bind("<Button-3>",lambda event:make_a_flag(btn{i}_{j},{i},{j}))
btn{i}_{j}.pack()""")
game.pack()


def winornot():
    global win_or_no, game_board, first
    if first:
        game_board = build_game((random.randrange(gamerow), random.randrange(gamecol)), gamerow, gamecol, gameboom)
        first = False
    if win_or_no is None:
        f = flags.copy()
        g = game_board[1].copy()
        f.sort()
        g.sort()
        if f == g:
            win_or_no = True
            tips["text"] = "你赢了"
            show()
    else:
        win_or_no = False
        tips["text"] = "你输了"
        show()


def show():
    global game_board, first
    if first:
        game_board = build_game((random.randrange(gamerow), random.randrange(gamecol)), gamerow, gamecol, gameboom)
        first = False
    for row in range(gamerow):
        for col in range(gamecol):
            self = eval(f"btn{str(row)}_{str(col)}")
            if game_board[0][row][col] == "boom":
                # self["image"] = photo
                # TODO:图片！！！
                self["text"] = "雷"
            else:
                count_boom = 0
                for boom_x in range(-1, 2):
                    for boom_y in range(-1, 2):
                        if -1 < row + boom_x < gamerow and -1 < col + boom_y < gamecol:
                            if game_board[0][row + boom_x][col + boom_y] == "boom":
                                count_boom += 1
                if count_boom > 0:
                    self["text"] = str(count_boom)


def clear():
    global game_board, first
    if first:
        game_board = build_game((random.randrange(gamerow), random.randrange(gamecol)), gamerow, gamecol, gameboom)
        first = False
    for row in range(gamerow):
        for col in range(gamecol):
            self = eval(f"btn{str(row)}_{str(col)}")
            self["text"] = ""


def fuck_board():
    global game_board, first
    game_board = build_game((random.randrange(gamerow), random.randrange(gamecol)), gamerow, gamecol, gameboom)
    first = False
    clear()


Button(text="确认", command=winornot).pack()
Button(text="进入作弊模式", command=show).pack()
Button(text="重置棋盘", command=fuck_board).pack()
tips = Label(text="")
tips.pack()
Label(text="创新者老王制作").pack()
scn_w, scn_h = window.maxsize()

window.mainloop()
