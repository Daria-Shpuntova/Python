import tkinter as tk
from tkinter import messagebox

win = tk.Tk()
win.title('Калькулятор')
win.geometry('240x270+650+200')
win.resizable(False, False)
photo = tk.PhotoImage(file='calculator.png')
win.iconphoto(False, photo)
win.config(bg='#4C0E8E')

def add_dig(digit):
    valu = calk.get()
    if valu[0]=='0' and len(valu)==1:
        valu=valu[1:]
    calk.delete(0, 'end')
    calk.insert(0, valu+digit)

def add_operr(oper):
    vall=calk.get()
    if vall[-1] in '-+/*':
        vall=vall[:-1]
    elif '+' in vall or '-' in vall or '/' in vall or '*' in vall:
        calculate()
        vall=calk.get()
    calk.delete(0, 'end')
    calk.insert(0, vall+oper)

def calculate():
    valllu=calk.get()
    if valllu[-1] in '/*-+':
        valllu=valllu+valllu[:-1]
    calk.delete(0, 'end')
    try:
        calk.insert(0, eval(valllu))
    except (NameError, SyntaxError):
        messagebox.showinfo('Внимание', 'Нужно вводить только цифры, Вы ввели другие символы')
        calk.insert(0,0)
    except ZeroDivisionError:
        messagebox.showinfo('Внимание', 'На ноль делить нельзя!!!!')
        calk.insert(0, 0)



def clear():
    calk.delete(0, 'end')
    calk.insert(0,0)

def make_dig(digit):
    return tk.Button(text=digit, bd=5, font=('Arial', 13), command=lambda: add_dig(digit))

def make_oper(oper):
    return tk.Button(text=oper, bd=5, font=('Arial', 13), fg='red', command=lambda: add_operr(oper))

def make_calk(oper):
    return tk.Button(text=oper, bd=5, font=('Arial', 13), fg='red', command=calculate)

def make_clear(oper):
    return tk.Button(text=oper, bd=5, font=('Arial', 13), fg='red', command=clear)


def press_key(event):
    print(repr(event.char))
    if event.char.isdigit():
        add_dig(event.char)
    elif  event.char in '/*-+':
        add_operr(event.char)
    elif event.char == '\r':
        calculate()
        


win.bind('<Key>', press_key)

calk = tk.Entry(win, justify=tk.RIGHT, font=('Arial', 15), width=15)
calk.insert(0, '0')
calk.grid(row=0, column=0, columnspan=4, stick='wens', padx=5)

make_dig('1').grid(row=1, column=0, stick='wens', padx=5, pady=5)
make_dig('2').grid(row=1, column=1, stick='wens', padx=5, pady=5)
make_dig('3').grid(row=1, column=2, stick='wens', padx=5, pady=5)
make_dig('4').grid(row=2, column=0, stick='wens', padx=5, pady=5)
make_dig('5').grid(row=2, column=1, stick='wens', padx=5, pady=5)
make_dig('6').grid(row=2, column=2, stick='wens', padx=5, pady=5)
make_dig('7').grid(row=3, column=0, stick='wens', padx=5, pady=5)
make_dig('8').grid(row=3, column=1, stick='wens', padx=5, pady=5)
make_dig('9').grid(row=3, column=2, stick='wens', padx=5, pady=5)
make_dig('0').grid(row=4, column=0, stick='wens', padx=5, pady=5)

make_oper('+').grid(row=1, column=3, stick='wens', padx=5, pady=5)
make_oper('-').grid(row=2, column=3, stick='wens', padx=5, pady=5)
make_oper('/').grid(row=3, column=3, stick='wens', padx=5, pady=5)
make_oper('*').grid(row=4, column=3, stick='wens', padx=5, pady=5)

make_calk('=').grid(row=4, column=2, stick='wens', padx=5, pady=5)

make_clear('C').grid(row=4, column=1, stick='wens', padx=5, pady=5)

win.grid_columnconfigure(0, minsize=60)
win.grid_columnconfigure(1, minsize=60)
win.grid_columnconfigure(2, minsize=60)
win.grid_columnconfigure(3, minsize=60)

win.grid_rowconfigure(1, minsize=60)
win.grid_rowconfigure(2, minsize=60)
win.grid_rowconfigure(3, minsize=60)
win.grid_rowconfigure(4, minsize=60)
win.mainloop()
