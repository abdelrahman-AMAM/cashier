import tkinter
import mysql.connector
from tkinter import *
from tkinter import font
from tkinter import messagebox
from shopManagement import newCust
from datetime import datetime
import session


def prodtoStock():
    # Getting the user inputs of product details from the user
    pid = prodId.get()
    pname = prodName.get()
    price = prodPrice.get()
    dt = date_added.get()
    qt = quantity.get()
    tx = tax_id.get()
    # Connecting to the database
    db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database='Shop')
    cursor = db.cursor()

    # query to add the product details to the table
    query = "INSERT INTO Stock(prodId,prodName,prodPrice,datetime_added,quantity,Tax_id) VALUES(%s,%s,%s,%s,%s,%s)"
    details = (pid, pname, price,dt,qt,tx)

    # Executing the query and showing the pop up message
    try:
        cursor.execute(query, details)
        db.commit()
        messagebox.showinfo('Success', "Product added successfully")
    except Exception as e:
        print("The exception is:", e)
        messagebox.showinfo("Error", "Trouble adding data into Database")

    wn.destroy()



def add_to_stock():
    global prodId,prodName, prodPrice, date_added,quantity,tax_id, Canvas1, wn

    # Creating the window
    wn = tkinter.Tk()
    wn.title("Complex Management System")
    wn.configure(bg='mint cream')
    wn.minsize(width=500, height=500)
    wn.geometry("700x600")
    wn.geometry("700x600+{}+{}".format(
        int(wn.winfo_screenwidth() / 2 - 730 / 2),
        int(wn.winfo_screenheight() / 2 - 620 / 2)))

    Canvas1 = Canvas(wn)
    Canvas1.config(bg='#1f2020')
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(wn, bg='snow3', bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    headingLabel = Label(headingFrame1, text="Add a Product to stock", fg='grey19', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(wn)
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)



    # Getting Date
    lable1 = Label(labelFrame, text="Date Added : ", fg='black')
    lable1.place(relx=0.05, rely=0.09, relheight=0.08)

    date_added = Entry(labelFrame)
    date_added.place(relx=0.3, rely=0.09, relwidth=0.62, relheight=0.08)
    date_added.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Getting Tax_id
    lable7 = Label(labelFrame, text="Supplier Tax_id : ", fg='black')
    lable7.place(relx=0.05, rely=0.24, relheight=0.08)

    tax_id = Entry(labelFrame)
    tax_id.place(relx=0.3, rely=0.24, relwidth=0.62, relheight=0.08)


    # Product Id
    lable4 = Label(labelFrame, text="Product Id : ", fg='black')
    lable4.place(relx=0.05, rely=0.39, relheight=0.08)

    prodId = Entry(labelFrame)
    prodId.place(relx=0.3, rely=0.39, relwidth=0.62, relheight=0.08)


    # Product Name
    lable2 = Label(labelFrame, text="Product Name : ", fg='black')
    lable2.place(relx=0.05, rely=0.54, relheight=0.08)

    prodName = Entry(labelFrame)
    prodName.place(relx=0.3, rely=0.54, relwidth=0.62, relheight=0.08)

    # Product Price
    lable3 = Label(labelFrame, text="Product Unit Price : ", fg='black')
    lable3.place(relx=0.05, rely=0.69, relheight=0.08)

    prodPrice = Entry(labelFrame)
    prodPrice.place(relx=0.3, rely=0.69, relwidth=0.62, relheight=0.08)

    # Product Quantity
    lable6 = Label(labelFrame, text="Product Quantity : ", fg='black')
    lable6.place(relx=0.05, rely=0.84, relheight=0.08)

    quantity = Entry(labelFrame)
    quantity.place(relx=0.3, rely=0.84, relwidth=0.62, relheight=0.08)

    # Add Button
    Btn = Button(wn, text="ADD", bg='snow3', fg='black', command=prodtoStock)
    Btn.place(relx=0.28, rely=0.85, relwidth=0.18, relheight=0.08)

    Quit = Button(wn, text="Quit", bg='snow3', fg='black', command=wn.destroy)
    Quit.place(relx=0.53, rely=0.85, relwidth=0.18, relheight=0.08)

    wn.mainloop()


def add_new_prod():
    def verify_passwordd():
        entered_password = entry_password.get()
        if entered_password == "0912":
            password_window.destroy()
            open_stock_window()
        else:
            messagebox.showerror("Error", "Incorrect Password")
            password_window.destroy()

    password_window = Tk()
    password_window.title("Verify Password")
    password_window.iconbitmap("complex.ico")
    password_window.geometry("300x150")
    password_window.geometry("300x150+{}+{}".format(
        int(password_window.winfo_screenwidth() / 2 - 310 / 2),
        int(password_window.winfo_screenheight() / 2 - 410 / 2)))
    password_window.configure(bg='#1f2020')

    form_frame = Frame(password_window, bg='#1f2020')
    form_frame.pack(pady=20)

    Label(form_frame, text="Enter Admin Creation Password:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10,
                                                                                   sticky=E)
    entry_password = Entry(form_frame, show="*")
    entry_password.grid(row=1, column=0, pady=5)

    Btn_verify = Button(form_frame, text="Verify", bg='snow3', command=verify_passwordd)
    Btn_verify.grid(row=1, column=1, padx=7)

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Done*

def open_stock_window():
    wn = Tk()
    wn.title("Complex Management System")
    wn.iconbitmap("complex.ico")
    wn.configure(bg='#1f2020')
    wn.geometry("700x600")
    wn.geometry("700x600+{}+{}".format(
        int(wn.winfo_screenwidth() / 2 - 730 / 2),
        int(wn.winfo_screenheight() / 2 - 620 / 2)))

    headingFrame1 = Frame(wn, bg="snow3", bd=5)
    headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.16)
    headingLabel = Label(headingFrame1, text=" Complex \nManagement System", fg='grey19', font=('Courier', 17, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    btn1_font = font.Font(family="Arial",size=10, weight='normal')
    btn1 = Button(wn, text="Add To Stock", bg='snow3', fg='black', width=20, height=2, command=add_to_stock)
    btn1['font'] = font.Font(size=12)
    btn1.place(x=260, y=175)

    btn2 = Button(wn, text="Delete a Product", bg='snow3', fg='black', width=20, height=2, command=delProdd)
    btn2['font'] = font.Font(size=12)
    btn2.place(x=260, y=255)

    Btn3 = Button(wn, text="Add New Admin", bg='snow3', fg='black', width=20, height=2, command=open_add_admin_window)
    Btn3['font'] = font.Font(size=12)
    Btn3.place(x=260, y=335)

    wn.mainloop()


def removeProdd():
    name = prodId.get()  # Now using correct variable

    db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database='Shop')
    cursor = db.cursor()

    query = "DELETE from Stock where LOWER(prodId) = %s"
    try:
        cursor.execute(query, (name.lower(),))
        db.commit()
        messagebox.showinfo('Success', "Product Record Deleted Successfully")
    except Exception as e:
        print("The exception is:", e)
        messagebox.showinfo("Error", "Please check Product ID")

    wn.destroy()


def delProdd():
    global prodId, Canvas1, wn

    wn = tkinter.Tk()
    wn.title("Complex Management System")
    wn.iconbitmap("complex.ico")
    wn.configure(bg='#1f2020')
    wn.minsize(width=500, height=500)
    wn.geometry("700x600")
    wn.geometry("700x600+{}+{}".format(
        int(wn.winfo_screenwidth() / 2 - 730 / 2),
        int(wn.winfo_screenheight() / 2 - 620 / 2)))

    Canvas1 = Canvas(wn)
    Canvas1.config(bg="#1f2020")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(wn, bg="snow3", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    headingLabel = Label(headingFrame1, text="Delete Product", fg='grey19', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(wn)
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    lable = Label(labelFrame, text="Product Id : ", fg='black')
    lable.place(relx=0.05, rely=0.5)

    prodId = Entry(labelFrame)
    prodId.place(relx=0.3, rely=0.5, relwidth=0.62)

    Btn = Button(wn, text="DELETE", bg='snow3', fg='black', command=removeProdd)
    Btn.place(relx=0.28, rely=0.85, relwidth=0.18, relheight=0.08)

    Quit = Button(wn, text="Quit", bg='snow3', fg='black', command=wn.destroy)
    Quit.place(relx=0.53, rely=0.85, relwidth=0.18, relheight=0.08)

    wn.mainloop()

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////done*


def validate_login():
    admin_id = entry_admin_id.get()

    db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database="Shop")
    cursor = db.cursor()
    query = "SELECT * FROM Admins WHERE adminId = %s"
    cursor.execute(query, (admin_id,))
    result = cursor.fetchone()

    if result:
        session.current_admin_id = admin_id
        session.login_time = datetime.now()

        messagebox.showinfo("Login Success",
                            f"You are logged in successfully!\nLogin time: {session.login_time.strftime('%Y-%m-%d %H:%M:%S')}")

        wn_sign_in.destroy()
        newCust()

    else:
        messagebox.showerror("Login Failed", "Invalid Id")

    cursor.close()
    db.close()


# نافذة إضافة إدمن جديد
def open_add_admin_window():
    def save_new_admin():
        admin_id = entry_admin_id_new.get()
        admin_name = entry_admin_name_new.get()
        admin_email = entry_admin_email_new.get()
        admin_number = entry_admin_number_new.get()

        db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database="Shop")
        cursor = db.cursor()
        query = "INSERT INTO Admins (adminId, adminName, adminEmail,adminNumber) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (admin_id, admin_name, admin_email,admin_number))
        db.commit()

        messagebox.showinfo("Success", "New Admin added successfully!")
        new_admin_window.destroy()  # اغلق نافذة الإضافة

        cursor.close()
        db.close()

    global new_admin_window
    new_admin_window = Tk()
    new_admin_window.title("Add New Admin")
    new_admin_window.iconbitmap("complex.ico")
    new_admin_window.geometry("350x300")
    new_admin_window.geometry("450x400+{}+{}".format(
        int(new_admin_window.winfo_screenwidth() / 2 - 430 / 2),
        int(new_admin_window.winfo_screenheight() / 2 - 420 / 2)))
    new_admin_window.configure(bg='#1f2020')
    # إطار لتنسيق الإدخالات
    form_frame = Frame(new_admin_window, bg='#1f2020')
    form_frame.pack(pady=20)

    # Admin ID
    Label(form_frame, text="Admin ID:", bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=15, sticky=E)
    entry_admin_id_new = Entry(form_frame)
    entry_admin_id_new.grid(row=0, column=1, pady=5)

    # Admin Name
    Label(form_frame, text="Admin Name:", bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=10, sticky=E)
    entry_admin_name_new = Entry(form_frame)
    entry_admin_name_new.grid(row=1, column=1, pady=5, padx=10)

    # Email
    Label(form_frame, text="Email:", bg='#f0f0f0').grid(row=2, column=0, padx=10, pady=10, sticky=E)
    entry_admin_email_new = Entry(form_frame)
    entry_admin_email_new.grid(row=2, column=1, pady=5, padx=10)


    # number
    Label(form_frame, text="Phone Number:", bg='#f0f0f0').grid(row=3, column=0, padx=10, pady=10, sticky=E)
    entry_admin_number_new = Entry(form_frame)
    entry_admin_number_new.grid(row=3, column=1, pady=5, padx=10)

    Btn_save = Button(new_admin_window, text="Save New Admin", bg='snow3', fg='black', command=save_new_admin)
    Btn_save.place(relx=0.28, rely=0.75, relwidth=0.45, relheight=0.1)



def addAdmin():
    global wn_sign_in, entry_admin_id

    wn_sign_in = Tk()
    wn_sign_in.title("Admin Sign-In")
    wn_sign_in.geometry("350x300")
    wn_sign_in.iconbitmap("complex.ico")
    wn_sign_in.geometry("400x350+{}+{}".format(
        int(wn_sign_in.winfo_screenwidth() / 2 - 380 / 2),
        int(wn_sign_in.winfo_screenheight() / 2 - 380 / 2)))
    wn_sign_in.configure(bg='#1f2020')

    form_frame = Frame(wn_sign_in, bg='#1f2020')
    form_frame.pack(pady=90)

    Label(form_frame, text="Admin ID:", bg='#f0f0f0').grid(row=2, column=0, padx=20, pady=12, sticky=E)
    entry_admin_id = Entry(form_frame)
    entry_admin_id.grid(row=2, column=1, pady=5)

    Btn1 = Button(wn_sign_in, text="Sign In", bg='snow3', fg='black', command=validate_login)
    Btn1.place(relx=0.42, rely=0.48, relwidth=0.18, relheight=0.08)


    wn_sign_in.mainloop()

