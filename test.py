import Tkinter as tk


def donothing():
    print ('IT WORKED')


root = tk.Tk()
root.title(string='LOGIN PAGE')

frame1 = tk.Frame(root)
frame1.pack(side='top', fill='x')

m = tk.Menu(frame1)
root.config(menu=m)

submenu = tk.Menu(m)
m.add_cascade(label='File', menu=submenu)
submenu.add_command(label='New File', command=donothing)
submenu.add_command(label='Open', command=donothing)
submenu.add_separator()
submenu.add_command(label='Exit', command=frame1.quit)


editmenu = tk.Menu(m)
m.add_cascade(label='Edit', menu=editmenu)
editmenu.add_command(label='Cut', command=donothing)
editmenu.add_command(label='Copy', command=donothing)
editmenu.add_command(label='Paste', command=donothing)
editmenu.add_separator()
editmenu.add_command(label='Exit', command=frame1.quit)

toolbar = tk.Frame(frame1, bg='grey')
toolbar.pack(side='top', fill='x')
btn1 = tk.Button(toolbar, text='Print', command=donothing)
btn2 = tk.Button(toolbar, text='Paste', command=donothing)
btn3 = tk.Button(toolbar, text='Cut', command=donothing)
btn4 = tk.Button(toolbar, text='Copy', command=donothing)
btn1.pack(side='left')
btn2.pack(side='left')
btn3.pack(side='left')
btn4.pack(side='left')


root.mainloop()
