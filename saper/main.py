import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror
import time

colorsys={0:'white', 1:'blue', 2:'green', 3:'#3fc700', 4:'#b924f0', 5:'#c76000', 6:'#ad038d', 7:'#048a94', 8:'#396104'}

class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.is_flag=False
        self.count_bomb = 0
        self.is_open=False
        self.time_start=0


    def __repr__(self):
        return f'MyButten {self.x} {self.y} {self.number} {self.is_mine} {self.not_is_mine}'


class MineSweeper:
    win = tk.Tk()
    win.title('Сапер')
    ROW = 7
    COLUMNS = 10
    MINS = 5
    IS_GAME_OVER= False
    IS_FIRST_CLICK=True
    count_flag=0

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.ROW + 2):
            temp = []
            for j in range(MineSweeper.COLUMNS + 2):
                btn = MyButton(MineSweeper.win, x=i, y=j, width=3, font='Calibri 15 bold')
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind('<Button-3>', self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

    def right_click(self, event):
        cur_btn = event.widget
        if MineSweeper.IS_GAME_OVER:
            return
        if self.IS_FIRST_CLICK:
            return
        list_mins_pos=sorted(self.index_mines)
        if not cur_btn.is_flag and not cur_btn.is_open:
            if self.count_flag == 0:
                return
            cur_btn['command']=0
            cur_btn.is_flag = True
            cur_btn['text'] = '🚩'
            self.count_flag-=1
            self.flag_position.append(cur_btn.number)
        elif cur_btn.is_flag and not cur_btn.is_open:
            cur_btn.is_flag=False
            cur_btn['text'] = 'X'
            cur_btn['command'] = lambda button = cur_btn: self.click(button)
            self.count_flag+=1
            self.flag_position.remove(cur_btn.number)

        if list_mins_pos == sorted(self.flag_position):
            showinfo("Congratulations", "Ви виграли!")

        self.lbl_mine.config(text=f'Мины: {self.count_flag}')




    def click(self, clicked_button: MyButton):

        if MineSweeper.IS_GAME_OVER:
            return
        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines()
            self.print_butn()
            self.time_start=time.time()
            self.tic()
            MineSweeper.IS_FIRST_CLICK=False
        if clicked_button.is_mine:
            clicked_button.config(text='💣', background='red', disabledforeground='black')
            clicked_button.is_open=True
            MineSweeper.IS_GAME_OVER=True
            showinfo('Игра окончена', 'The end ')
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '💥'

        else:
            color = colorsys.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.bread_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

        no_of_closed_buttons = 0
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                if not self.buttons[i][j].is_open:
                    no_of_closed_buttons += 1
        if no_of_closed_buttons == MineSweeper.MINS:
            MineSweeper.IS_GAME_OVER = True
            showinfo("Congratulations", "Ви виграли!")


    def bread_first_search(self, btn:MyButton):
        queu=[btn]
        while queu:
            cur_btn=queu.pop()
            color = colorsys.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text=' ', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)
            if cur_btn.count_bomb==0:
                x, y =cur_btn.x, cur_btn.y
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        next_btn = self.buttons[x+dx][y+dy]
                        if not next_btn.is_open and 1<=next_btn.x<=MineSweeper.ROW and \
                                1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queu:
                            queu.append(next_btn)
    def reload(self):
        [child.destroy() for child in self.win.winfo_children()]
        self.__init__()
        self.create_widght()
        MineSweeper.IS_FIRST_CLICK=True
        MineSweeper.IS_GAME_OVER=False

    def create_setting_window(self):
        win_setting=tk.Toplevel(self.win)
        win_setting.wm_title('Настройки')
        tk.Label(win_setting, text='Количество строк ').grid(row=0, column=0)
        row_entry=tk.Entry(win_setting)
        row_entry.insert(0, MineSweeper.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_setting, text='Количество колонок ').grid(row=1, column=0)
        column_entry=tk.Entry(win_setting)
        column_entry.insert(0, MineSweeper.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_setting, text='Количество мин ').grid(row=2, column=0)
        mines_entry=tk.Entry(win_setting)
        mines_entry.insert(0, MineSweeper.MINS)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        save_btn=tk.Button(win_setting, text='Приминить',
                           command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row:tk.Entry, column:tk.Entry, mines:tk.Entry):
        try:
            int(row.get()), int(column.get()),  int(mines.get())
        except ValueError:
            showerror('Ошибка', 'Не верный ввод данных ')
            return
        MineSweeper.ROW=int(row.get())
        MineSweeper.COLUMNS= int(column.get())
        MineSweeper.MINS = int(mines.get())
        self.reload()

    def create_widght(self):
        menubar=tk.Menu(self.win)
        self.flag_position=[]
        self.count_flag=self.MINS
        self.win.config(menu=menubar)
        settings_menu=tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.create_setting_window)
        settings_menu.add_command(label='Выход', command=self.win.destroy)
        menubar.add_cascade(label='Игра', menu=settings_menu)
        count=1
        for i in range(1,MineSweeper.ROW + 1):
            for j in range(1,MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='nwes')
                count+=1
        for i in range(1,MineSweeper.ROW + 1):
            tk.Grid.rowconfigure(self.win, i, weight=1)
        for i in range(1,MineSweeper.COLUMNS + 1):
            tk.Grid.columnconfigure(self.win, i, weight=1)

        self.lbl_time = tk.Label(text='Время: ')
        self.lbl_time.grid(row=0, column=1, columnspan=(self.COLUMNS//2))
        self.lbl_mine = tk.Label(text='Мины:')
        self.lbl_mine.grid(row=0, column=(self.COLUMNS // 2)+1, columnspan=(self.COLUMNS // 2))

    def tic(self):
        if self.IS_GAME_OVER:
            return
        timer=time.time()-self.time_start
        self.lbl_time.config(text=f'Время:{timer:.0f}')
        self.lbl_time.after(500, self.tic)

    def open_all_butten(self):
        for i in range(MineSweeper.ROW + 2):
            for j in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                elif btn.count_bomb in colorsys:
                    color=colorsys.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):
        self.create_widght()
        MineSweeper.win.mainloop()

    def print_butn(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end=' ')
                else:
                    print(btn.count_bomb, end=' ')
            print(' ')

    def insert_mines(self, number:int):
        self.index_mines = self.get_mines_pleaces(number)
        print(self.index_mines)
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in self.index_mines:
                    btn.is_mine = True


    def count_mines(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neight = self.buttons[i + row_dx][j + col_dx]
                            if neight.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb

    @staticmethod
    def get_mines_pleaces(exclude_number:int):
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        print(f'Исключаем кнопку номер {exclude_number}')
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:MineSweeper.MINS]


game = MineSweeper()
game.start()
