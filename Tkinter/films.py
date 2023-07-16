import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Main:
    def __init__(self, wind):
        self.wind = wind
        self.wind.title('Фильмы и сериалы')
        self.wind.geometry('800x500+500+200')
        self.wind.resizable(False, False)
        self.wind['background'] = '#4C0E6E'
        self.osnov()
        self.bd()
        self.tabl()
        self.imay = ' '

    def osnov(self):
        self.frame = ttk.Labelframe(self.wind)
        self.frame.grid(row=0, column=0, pady=5, padx=15)
        self.name = ttk.Label(self.frame, text='Название', foreground='blue', background='#E066FF')
        self.name.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)
        self.name.columnconfigure(index=0, weight=1)
        self.year = ttk.Label(self.frame, text='Год выпуска', foreground='blue', background='#E066FF')
        self.year.grid(row=0, column=1, sticky='nswe', padx=5, pady=5)
        self.year.columnconfigure(index=1, weight=1)
        self.tip = ttk.Label(self.frame, text='Тип', foreground='blue', background='#E066FF')
        self.tip.grid(row=0, column=2, sticky='nswe', padx=5, pady=5)
        self.tip.columnconfigure(index=2, weight=1)
        self.janr = ttk.Label(self.frame, text='Жанр', foreground='blue', background='#E066FF')
        self.janr.grid(row=0, column=3, sticky='nswe', padx=5, pady=5)
        self.janr.columnconfigure(index=3, weight=1)
        self.koment = ttk.Label(self.frame, text='Коментарий', foreground='blue', background='#E066FF')
        self.koment.grid(row=0, column=4, sticky='nswe', padx=5, pady=5)
        self.koment.columnconfigure(index=4, weight=1)
        self.e1 = ttk.Entry(self.frame)
        self.e1.grid(row=1, column=0, padx=5, pady=5)
        self.e2 = ttk.Entry(self.frame)
        self.e2.grid(row=1, column=1, padx=5, pady=5)
        self.tipp = tk.StringVar()
        self.tippp = ttk.Combobox(self.frame, textvariable=self.tipp)
        self.tippp['values'] = ('Фильм', 'Сериал')
        self.tippp.grid(row=1, column=2, padx=5, pady=5)
        self.janrr = tk.StringVar()
        self.janrrr = ttk.Combobox(self.frame, textvariable=self.janrr)
        self.janrrr['values'] = ('Боевик', 'Ужастик', 'Остальное')
        self.janrrr.grid(row=1, column=3, padx=5, pady=5)
        self.e5 = ttk.Entry(self.frame)
        self.e5.grid(row=1, column=4, padx=5, pady=5)

        self.button = ttk.Button(self.frame, text='Добавить', command=self.insert)
        self.button.grid(column=4, row=2)

    def tabl(self):
        self.frame2 = ttk.Labelframe(self.wind, height=100)
        self.frame2.grid(row=1, column=0, pady=5, padx=10)

        self.tree = ttk.Treeview(self.frame2, columns=('id', 'name', 'year', 'tyyp', 'janr', 'koment', 'otmetka'),
                                 height=15,
                                 show='headings')
        self.tree.column('id', width=25, anchor=tk.CENTER)
        self.tree.column('name', width=230, anchor=tk.CENTER)
        self.tree.column('year', width=95, anchor=tk.CENTER)
        self.tree.column('tyyp', width=95, anchor=tk.CENTER)
        self.tree.column('janr', width=95, anchor=tk.CENTER)
        self.tree.column('koment', width=190, anchor=tk.CENTER)
        self.tree.column('otmetka', width=45, anchor=tk.CENTER)
        self.tree.heading('id', text='№')
        self.tree.heading('name', text='Название')
        self.tree.heading('year', text='Год выпуска')
        self.tree.heading('tyyp', text='Тип')
        self.tree.heading('janr', text='Жанр')
        self.tree.heading('koment', text='Коментарий')
        self.tree.heading('otmetka', text='Метка')
        self.tree.grid(columnspan=2)

        self.cin = sqlite3.connect('films.db')
        self.c = self.cin.cursor()

        self.c.execute('''SELECT * FROM films''')
        [self.tree.insert('', 'end', values=row) for row in self.c.fetchall()]
        #       self.cin.commit()

        self.button2 = ttk.Button(self.frame2, text='Удалить', command=self.select_del)
        self.button2.grid(column=0, row=2)

        self.button3 = ttk.Button(self.frame2, text='Редактировать', command=self.select)
        self.button3.grid(column=1, row=2)

    def bd(self):
        self.tree = Main.tabl
        self.cin = sqlite3.connect('films.db')
        self.c = self.cin.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS films(id integer primary key, name text, year integer, tyyp text, janr text, koment text, otmetka text )''')
        self.cin.commit()

    def insert(self):
        namme = self.e1.get()
        yearr = self.e2.get()
        tyypp = self.tippp.get()
        janrr = self.janrr.get()
        komentt = self.e5.get()
        otmetkka = '  '
        self.c.execute('''INSERT INTO films(name, year, tyyp, janr, koment, otmetka) VALUES(?,?,?,?,?,?)''',
                       (namme, yearr, tyypp, janrr, komentt, otmetkka))
        self.cin.commit()
        self.osnov()
        self.tabl()

    def select(self):
        self.b = (self.tree.set(self.tree.selection()[0], '#1'),)
        self.c.execute('''SELECT name FROM films WHERE id=?''', self.b)
        self.imay = self.c.fetchall()[0][0]
        self.init_child()

    def red_met(self):
        try:
            self.otmet = self.mmet.get()
            zamena = (self.otmet, self.b[0])
            self.c.execute('''UPDATE films SET otmetka=? WHERE id=?''', (zamena))
            self.cin.commit()
            self.tabl()
            messagebox.showinfo('Все отлично', 'Обновление прошло успешно')
            self.child.destroy()
        except:
            messagebox.showerror("Ошибка", "Что-то пошло не так....")

    def select_del(self):
        self.b = (self.tree.set(self.tree.selection()[0], '#1'),)
        self.c.execute('''SELECT name FROM films WHERE id=?''', self.b)
        self.imay = self.c.fetchall()[0][0]
        self.del_child()

    def delet(self):
        try:
            self.c.execute('''DELETE FROM films WHERE id=?''', self.b)
            self.cin.commit()
            self.tabl()
            messagebox.showinfo('Все отлично', 'Удаление прошло успешно')
            self.child.destroy()
        except:
            messagebox.showerror("Ошибка", "Что-то пошло не так....")

    def init_child(self):
        self.child = tk.Tk()
        self.child.title('Редоктирование')
        self.child.geometry('300x160+400+300')
        self.child.resizable(False, False)

        nname = tk.Label(self.child, text='Название')
        nname.grid(column=0, row=0, padx=15, pady=5)
        name = self.imay
        e1 = ttk.Label(self.child, text=name)
        e1.grid(row=0, column=1, padx=15, pady=5)

        met = ttk.Label(self.child, text='Метка')
        met.grid(row=5, column=0, padx=15, pady=5)
        self.otmetka = tk.StringVar()

        self.mmet = ttk.Combobox(self.child, textvariable=self.otmetka)
        self.mmet['values'] = ('🆇', '♡', '✓')

        self.mmet.grid(row=5, column=1, padx=15, pady=5)

        btn = ttk.Button(self.child, text='Сохранить изменения', command=self.red_met)
        btn.grid(column=0, row=6, columnspan=2)

    def del_child(self):
        self.child = tk.Tk()
        self.child.title('Удаление')
        self.child.geometry('200x150+400+300')
        self.child.resizable(False, False)

        nname = tk.Label(self.child, text='Название')
        nname.grid(column=0, row=0, padx=25, pady=5)
        name = self.imay
        e1 = ttk.Label(self.child, text=name)
        e1.grid(row=0, column=1, padx=25, pady=5)

        btn = ttk.Button(self.child, text='Удалить', command=self.delet)
        btn.grid(column=0, row=6, columnspan=2)


if __name__ == '__main__':
    wind = tk.Tk()
    Main(wind)
    wind.mainloop()
