import tkinter
from tkinter import *
from signin_screen import addAdmin
from signin_screen import add_new_prod

def close_and_open_new_window(func):
    wwn.destroy()
    func()

def start_window():
    global wwn
    wwn = Tk()
    wwn.title("Complex")
    wwn.iconbitmap("complex.ico")
    wwn.geometry("500x400+{}+{}".format(
        int(wwn.winfo_screenwidth() / 2 - 480 / 2),
        int(wwn.winfo_screenheight() / 2 - 420 / 2)))
    wwn.configure(bg='#1f2020')

    form_frame = Frame(wwn, bg='#1f2020')
    form_frame.pack(pady=70)

    image_1 = PhotoImage(file="clerk.png")
    image_2 = PhotoImage(file="warehouse (2).png")

    Btn3 = Button(wwn, bg='white', image=image_1,bd=0, borderwidth=1, highlightthickness=1,command=lambda: close_and_open_new_window(addAdmin))
    Btn3.place(relx=0.08, rely=0.25, width=200, height=200)

    Btn4 = Button(wwn, bg='white', image=image_2, bd=0, borderwidth=1, highlightthickness=1,command=lambda: close_and_open_new_window(add_new_prod))
    Btn4.place(relx=0.52, rely=0.25, width=200, height=200)

    wwn.mainloop()

start_window()

