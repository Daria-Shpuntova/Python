import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class Main:
    def __init__(self, root):
        self.root=root
        self.main()
        self.bd()
        self.tabl()
        self.izmeneniay()


    def main(self):
        self.okno=tk.Frame(self.root, background='green')
        self.okno.grid(row=0, column=0, columnspan=3)
        self.new=ttk.Label(self.okno, text='Список растений для выращивания', font=('Comic Sans MS', 15), background='green')
        self.new.pack()
        self.new1=ttk.Button(self.okno, text='Добавить новое растение', command=self.new_rost)
        self.new1.pack(pady=7)

    def tabl(self):
        self.tab=tk.Frame(self.root)
        self.tab.grid(row=1, column=0, rowspan=7)
        self.tree=ttk.Treeview(self.tab, columns=('id','name','vid', 'rod', 'family', 'tipe', 'klimat', 'yhod'), height=15,
                                 show='headings')
        self.tree.column('id', width=25, anchor=tk.CENTER)
        self.tree.column('name', width=150, anchor=tk.CENTER)
        self.tree.column('vid', width=150, anchor=tk.CENTER)
        self.tree.column('rod', width=80, anchor=tk.CENTER)
        self.tree.column('family', width=150, anchor=tk.CENTER)
        self.tree.column('tipe', width=130, anchor=tk.CENTER)
        self.tree.column('klimat', width=180, anchor=tk.CENTER)
        self.tree.column('yhod', width=150, anchor=tk.CENTER)

        self.tree.heading('id', text='№')
        self.tree.heading('name', text='Название')
        self.tree.heading('vid', text='Внешность')
        self.tree.heading('rod', text='Род')
        self.tree.heading('family', text='Семейство')
        self.tree.heading('tipe', text='Тип растения')
        self.tree.heading('klimat', text='Климат')
        self.tree.heading('yhod', text='Особенности ухода')
        self.tree.grid(row=0, column=0, pady=15)


        self.cin = sqlite3.connect('rasteniay.db')
        self.c = self.cin.cursor()

        self.c.execute('''SELECT * FROM rasteniays''')
        [self.tree.insert('', 'end', values=row) for row in self.c.fetchall()]

    def izmeneniay(self):
        self.izm_uhod=ttk.Button(self.root, text='Изменить уход', command=self.select_uhod) # Изменить способ ухода за растением
        self.izm_uhod.grid(row=1, column=3, padx=10)
        self.izm_vid = ttk.Button(self.root, text='Изменить внешность',command=self.select_vid)  # Изменить внешность растением
        self.izm_vid.grid(row=2, column=3, padx=10)
        self.izm_klimat = ttk.Button(self.root, text='Изменить климат', command=self.select_klimat)  # Изменить климат растения
        self.izm_klimat.grid(row=3, column=3, padx=10)
        self.izm_tip = ttk.Button(self.root, text='Изменить тип', command=self.select_tipe)  # Изменить тип растения
        self.izm_tip.grid(row=4, column=3, padx=10)
        self.izm_family = ttk.Button(self.root, text='Изменить семейство', command=self.select_family)  # Изменить семейство растениея
        self.izm_family.grid(row=5, column=3, padx=10)
        self.izm_rod = ttk.Button(self.root, text='Изменить род', command=self.select_rod)  # Изменить род растениея
        self.izm_rod.grid(row=6, column=3, padx=10)
        self.izm_name = ttk.Button(self.root, text='Изменить название', command=self.select_name)  # Изменить название растениея
        self.izm_name.grid(row=7, column=3, padx=10)

        self.filter=ttk.Button(self.root, text='Удалить', command=self.select_del)
        self.filter.grid(row=8, column=0, pady=10)

    def bd(self):
        self.tree = Main.tabl
        self.cin = sqlite3.connect('rasteniay.db')
        self.c = self.cin.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS rasteniays(id integer primary key, name text, vid text, rod text, family text, tipe text, klimat text, yhod text )''')
        self.cin.commit()


    def new_rost(self):
        self.child = tk.Tk()
        self.child.title('Добавление нового растения')
        self.child.geometry('330x400+400+300')
        self.child.resizable(False, False)

        self.name = tk.Label(self.child, text='Название')
        self.name.grid(column=0, row=0, padx=15, pady=15)
        self.e1 = ttk.Entry(self.child)
        self.e1.grid(column=1, row=0,padx=15, pady=15)

        self.vid = tk.Label(self.child, text='Внешность')
        self.vid.grid(column=0, row=1, padx=15, pady=15)
        self.e7 = ttk.Entry(self.child)
        self.e7.grid(column=1, row=1, padx=15, pady=15)

        self.rod = tk.Label(self.child, text='Род')
        self.rod.grid(column=0, row=2, padx=15, pady=15)
        self.e2 = ttk.Entry(self.child)
        self.e2.grid( column=1, row=2,padx=15, pady=15)

        self.family = tk.Label(self.child, text='Семейство')
        self.family.grid(column=0, row=3, padx=15, pady=15)
        self.e3 = ttk.Entry(self.child)
        self.e3.grid(column=1, row=3, padx=15, pady=15)

        self.tip = tk.Label(self.child, text='Тип растения')
        self.tip.grid(column=0, row=4, padx=15, pady=15)
        self.e4 = ttk.Entry(self.child)
        self.e4.grid(column=1, row=4, padx=15, pady=15)

        self.klimat = tk.Label(self.child, text='Климат')
        self.klimat.grid(column=0, row=5, padx=15, pady=15)
        self.e5 = ttk.Entry(self.child)
        self.e5.grid(column=1, row=5, padx=15, pady=15)

        self.uhod = tk.Label(self.child, text='Уход за растением')
        self.uhod.grid(column=0, row=6, padx=15, pady=15)
        self.e6 = ttk.Entry(self.child)
        self.e6.grid(column=1, row=6, padx=15, pady=15)

        btn = ttk.Button(self.child, text='Сохранить', command=self.dobavlenie)
        btn.grid(column=0, row=7, columnspan=2)

    def dobavlenie(self):
        namme=self.e1.get()
        vidd=self.e7.get()
        rodd=self.e2.get()
        familly=self.e3.get()
        tipee=self.e4.get()
        klimatt=self.e5.get()
        uhodd=self.e6.get()
        self.c.execute('''INSERT INTO rasteniays(name, vid, rod, family, tipe, klimat, yhod) VALUES(?,?,?,?,?,?,?)''',
                       (namme, vidd, rodd, familly, tipee, klimatt, uhodd))
        self.cin.commit()
        self.tabl()

    def select(self):
        self.b = (self.tree.set(self.tree.selection()[0], '#1'),)
        self.c.execute('''SELECT name FROM rasteniays WHERE id=?''', self.b)
        self.imay = self.c.fetchall()[0][0]

    def select_uhod(self):
        self.select()
        self.izmen_uhod()

    def izmen_uhod(self):
        self.child1 = tk.Tk()
        self.child1.title('Изменить способ ухода за растением')
        self.child1.geometry('300x160+400+300')
        self.child1.resizable(False, False)

        nname = tk.Label(self.child1, text='Название')
        nname.grid(column=0, row=0, padx=15, pady=5)
        name = self.imay
        e1 = ttk.Label(self.child1, text=name)
        e1.grid(row=0, column=1, padx=15, pady=5)

        self.new_uhod=tk.Label(self.child1, text='Способ ухода')
        self.new_uhod.grid(column=0, row=1, padx=15, pady=5)
        self.new_uhod1=tk.Entry(self.child1)
        self.new_uhod1.grid(row=1, column=1, padx=15, pady=5)

        btn = ttk.Button(self.child1, text='Сохранить изменения', command=self.sohr_uhod)
        btn.grid(column=0, row=2, columnspan=2)

    def sohr_uhod(self):
        try:
            self.uhhod=self.new_uhod1.get()
            zamena = (self.uhhod, self.b[0])
            self.c.execute('''UPDATE rasteniays SET yhod=? WHERE id=?''', (zamena))
            self.cin.commit()
            self.tabl()
            messagebox.showinfo('Все отлично', 'Обновление прошло успешно')
            self.child1.destroy()
        except:
            messagebox.showerror('Ошибочка','Что-то пошло не так')


    def select_vid(self):
        self.select()
        self.izmen_vid()

    def izmen_vid(self):
        self.child1 = tk.Tk()
        self.child1.title('Изменить внешность растения')
        self.child1.geometry('300x160+400+300')
        self.child1.resizable(False, False)

        nname = tk.Label(self.child1, text='Название')
        nname.grid(column=0, row=0, padx=15, pady=5)
        name = self.imay
        e1 = ttk.Label(self.child1, text=name)
        e1.grid(row=0, column=1, padx=15, pady=5)

        self.new_vid=tk.Label(self.child1, text='Внешность')
        self.new_vid.grid(column=0, row=1, padx=15, pady=5)
        self.new_vid1=tk.Entry(self.child1)
        self.new_vid1.grid(row=1, column=1, padx=15, pady=5)

        btn = ttk.Button(self.child1, text='Сохранить изменения', command=self.sohr_vid)
        btn.grid(column=0, row=2, columnspan=2)

    def sohr_vid(self):
        try:
            self.vidd=self.new_vid1.get()
            zamena = (self.vidd, self.b[0])
            self.c.execute('''UPDATE rasteniays SET vid=? WHERE id=?''', (zamena))
            self.cin.commit()
            self.tabl()
            messagebox.showinfo('Все отлично', 'Обновление прошло успешно')
            self.child1.destroy()
        except:
            messagebox.showerror('Ошибочка','Что-то пошло не так')

    def select_klimat(self):
        self.select()
        self.izmen_klimat()

    def izmen_klimat(self):
        self.child1 = tk.Tk()
        self.child1.title('Изменить климат растения')
        self.child1.geometry('300x160+400+300')
        self.child1.resizable(False, False)

        nname = tk.Label(self.child1, text='Название')
        nname.grid(column=0, row=0, padx=15, pady=5)
        name = self.imay
        e1 = ttk.Label(self.child1, text=name)
        e1.grid(row=0, column=1, padx=15, pady=5)

        self.new_klimat=tk.Label(self.child1, text='Климат')
        self.new_klimat.grid(column=0, row=1, padx=15, pady=5)
        self.new_klimat1=tk.Entry(self.child1)
        self.new_klimat1.grid(row=1, column=1, padx=15, pady=5)

        btn = ttk.Button(self.child1, text='Сохранить изменения', command=self.sohr_klimat)
        btn.grid(column=0, row=2, columnspan=2)

    def sohr_klimat(self):
        try:
            self.klimmat=self.new_klimat1.get()
            zamena = (self.klimmat, self.b[0])
            self.c.execute('''UPDATE rasteniays SET klimat=? WHERE id=?''', (zamena))
            self.cin.commit()
            self.tabl()
            messagebox.showinfo('Все отлично', 'Обновление прошло успешно')
            self.child1.destroy()
        except:
            messagebox.showerror('Ошибочка','Что-то пошло не так')


    def select_tipe(self):
        self.select()
        self.izmen_tipe()

    def izmen_tipe(self):
        self.child1 = tk.Tk()
        self.child1.title('Изменить тип растения')
        self.child1.geometry('300x160+400+300')
        self.child1.resizable(False, False)

        nname = tk.Label(self.child1, text='Название')
        nname.grid(column=0, row=0, padx=15, pady=5)
        name = self.imay
        e1 = ttk.Label(self.child1, text=name)
        e1.grid(row=0, column=1, padx=15, pady=5)

        self.new_tipe=tk.Label(self.child1, text='Тип')
        self.new_tipe.grid(column=0, row=1, padx=15, pady=5)
        self.new_tipe1=tk.Entry(self.child1)
        self.new_tipe1.grid(row=1, column=1, padx=15, pady=5)

        btn = ttk.Button(self.child1, text='Сохранить изменения', command=self.sohr_tipe)
        btn.grid(column=0, row=2, columnspan=2)

    def sohr_tipe(self):
        try:
            self.tipee=self.new_tipe1.get()
            zamena = (self.tipee, self.b[0])
            self.c.execute('''UPDATE rasteniays SET tipe=? WHERE id=?''', (zamena))
            self.cin.commit()
            self.tabl()
            messagebox.showinfo('Все отлично', 'Обновление прошло успешно')
            self.child1.destroy()
        except:
            messagebox.showerror('Ошибочка','Что-то пошло не так')



    def select_family(self):
        self.select()
        self.izmen_family()

    def izmen_family(self):
        self.child1 = tk.Tk()
        self.child1.title('Изменить семейство растения')
        self.child1.geometry('300x160+400+300')
        self.child1.resizable(False, False)

        nname = tk.Label(self.child1, text='Название')
        nname.grid(column=0, row=0, padx=15, pady=5)
        name = self.imay
        e1 = ttk.Label(self.child1, text=name)
        e1.grid(row=0, column=1, padx=15, pady=5)

        self.new_family=tk.Label(self.child1, text='Семейство')
        self.new_family.grid(column=0, row=1, padx=15, pady=5)
        self.new_family1=tk.Entry(self.child1)
        self.new_family1.grid(row=1, column=1, padx=15, pady=5)

        btn = ttk.Button(self.child1, text='Сохранить изменения', command=self.sohr_family)
        btn.grid(column=0, row=2, columnspan=2)

    def sohr_family(self):
        try:
            self.familyy=self.new_family1.get()
            zamena = (self.familyy, self.b[0])
            self.c.execute('''UPDATE rasteniays SET family=? WHERE id=?''', (zamena))
            self.cin.commit()
            self.tabl()
            messagebox.showinfo('Все отлично', 'Обновление прошло успешно')
            self.child1.destroy()
        except:
            messagebox.showerror('Ошибочка','Что-то пошло не так')


    def select_rod(self):
        self.select()
        self.izmen_rod()

    def izmen_rod(self):
        self.child1 = tk.Tk()
        self.child1.title('Изменить род растения')
        self.child1.geometry('300x160+400+300')
        self.child1.resizable(False, False)

        nname = tk.Label(self.child1, text='Название')
        nname.grid(column=0, row=0, padx=15, pady=5)
        name = self.imay
        e1 = ttk.Label(self.child1, text=name)
        e1.grid(row=0, column=1, padx=15, pady=5)

        self.new_rod=tk.Label(self.child1, text='Род')
        self.new_rod.grid(column=0, row=1, padx=15, pady=5)
        self.new_rod1=tk.Entry(self.child1)
        self.new_rod1.grid(row=1, column=1, padx=15, pady=5)

        btn = ttk.Button(self.child1, text='Сохранить изменения', command=self.sohr_rod)
        btn.grid(column=0, row=2, columnspan=2)

    def sohr_rod(self):
        try:
            self.rodd=self.new_rod1.get()
            zamena = (self.rodd, self.b[0])
            self.c.execute('''UPDATE rasteniays SET rod=? WHERE id=?''', (zamena))
            self.cin.commit()
            self.tabl()
            messagebox.showinfo('Все отлично', 'Обновление прошло успешно')
            self.child1.destroy()
        except:
            messagebox.showerror('Ошибочка','Что-то пошло не так')

    def select_name(self):
        self.select()
        self.izmen_name()

    def izmen_name(self):
        self.child1 = tk.Tk()
        self.child1.title('Изменить название растения')
        self.child1.geometry('300x160+400+300')
        self.child1.resizable(False, False)

        nname = tk.Label(self.child1, text='Название')
        nname.grid(column=0, row=0, padx=15, pady=5)
        name = self.imay
        e1 = ttk.Label(self.child1, text=name)
        e1.grid(row=0, column=1, padx=15, pady=5)

        self.new_name=tk.Label(self.child1, text='Новое название ')
        self.new_name.grid(column=0, row=1, padx=15, pady=5)
        self.new_name1=tk.Entry(self.child1)
        self.new_name1.grid(row=1, column=1, padx=15, pady=5)

        btn = ttk.Button(self.child1, text='Сохранить изменения', command=self.sohr_name)
        btn.grid(column=0, row=2, columnspan=2)

    def sohr_name(self):
        try:
            self.namee=self.new_name1.get()
            zamena = (self.namee, self.b[0])
            self.c.execute('''UPDATE rasteniays SET name=? WHERE id=?''', (zamena))
            self.cin.commit()
            self.tabl()
            messagebox.showinfo('Все отлично', 'Обновление прошло успешно')
            self.child1.destroy()
        except:
            messagebox.showerror('Ошибочка','Что-то пошло не так')

    def select_del(self):
        self.select()
        self.del_child()

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

    def delet(self):
        try:
            self.c.execute('''DELETE FROM rasteniays WHERE id=?''', self.b)
            self.cin.commit()
            self.tabl()
            messagebox.showinfo('Все отлично', 'Удаление прошло успешно')
            self.child.destroy()
        except:
            messagebox.showerror("Ошибка", "Что-то пошло не так....")




if __name__ == '__main__':
    root = tk.Tk()
    root.title('Растения')
    root.geometry('1200x500+400+200')
    root['background'] = 'green'
    Main(root)
    root.mainloop()