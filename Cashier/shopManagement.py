from tkinter import *
from tkinter import font
import mysql.connector
from tkinter import ttk
import session
from datetime import datetime
import tkinter
from tkinter import Frame, Label, Entry, Button, messagebox
import random
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# الاتصال بقاعدة البيانات

db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", port=3306)
cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Shop")

db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database="Shop")
cursor = db.cursor()


query = """
CREATE TABLE IF NOT EXISTS Admins (
    adminId      INT PRIMARY KEY, 
    adminName    VARCHAR(50), 
    adminEmail   VARCHAR(100), 
    adminNumber  VARCHAR(50)
)
"""
cursor.execute(query)
db.commit()

query = """
CREATE TABLE IF NOT EXISTS Login_Activity(
    adminId            INT,
    Login_Datetime     DATETIME,
    Logout_Datetime    DATETIME,
    PRIMARY KEY (adminId, Login_Datetime, Logout_Datetime),
    FOREIGN KEY (adminId) REFERENCES Admins(adminId)
)
"""
cursor.execute(query)
db.commit()

query = """
CREATE TABLE IF NOT EXISTS Stock (
    prodId          INT PRIMARY KEY,
    prodName        VARCHAR(100),
    prodPrice       VARCHAR(50), 
    datetime_added  DATETIME,
    quantity        INT ,
    Tax_id          VARCHAR(100)
)
"""
cursor.execute(query)
db.commit()

query = """
CREATE TABLE IF NOT EXISTS Bills (
    billNumber      VARCHAR(10) PRIMARY KEY,
    billDatetime    DATETIME, 
    totalPrice      VARCHAR(100),
    method          VARCHAR(100)
)
"""
cursor.execute(query)
db.commit()
query = """
CREATE TABLE IF NOT EXISTS products (
    prodId      INT PRIMARY KEY,
    prodName    VARCHAR(100),
    prodPrice   VARCHAR(50),
    FOREIGN KEY (prodId) REFERENCES stock(prodId)
)
"""
cursor.execute(query)
db.commit()

query = """
CREATE TABLE IF NOT EXISTS Contains(
    prodId        INT,
    billNumber    VARCHAR(10),
    Quantity      INT,
    PRIMARY KEY (prodId, billNumber),
    FOREIGN KEY (prodId) REFERENCES Stock(prodId),
    FOREIGN KEY (billNumber) REFERENCES Bills(billNumber)
)
"""
cursor.execute(query)
db.commit()

query = """
CREATE TABLE IF NOT EXISTS Processes(
    billNumber        VARCHAR(10) PRIMARY KEY,
    CustNumber        VARCHAR(20),
    adminId           INT,
    FOREIGN KEY (billNumber) REFERENCES Bills(billNumber),
    FOREIGN KEY (adminId) REFERENCES Admins(adminId)
)
"""
cursor.execute(query)
db.commit()

query = """
CREATE TABLE IF NOT EXISTS Returns(
    Return_IdNumber    INT PRIMARY KEY AUTO_INCREMENT,
    billNumber         VARCHAR(10),
    Return_Datetime    DATETIME,
    Reason             VARCHAR(255),
    FOREIGN KEY (billNumber) REFERENCES Bills(billNumber)
)
"""
cursor.execute(query)
db.commit()

db.close()

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def prodtoTable():
    try:
        pid = prodId.get().strip()

        db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database='Shop')
        cursor = db.cursor()

        cursor.execute("SELECT * FROM Stock WHERE prodId = %s", (pid,))
        stock_data = cursor.fetchone()

        if not stock_data:
            messagebox.showwarning("Warning", "This Product ID does not exist in stock.")
            return

        stock_name = stock_data[1]
        stock_price = stock_data[2]
        stock_quantity = stock_data[4]

        if stock_quantity == 0:
            messagebox.showwarning("Out of Stock", "This product is out of stock.")
            return

        cursor.execute("SELECT * FROM products WHERE prodId = %s", (pid,))
        if cursor.fetchone():
            messagebox.showwarning("Warning", "This Product ID already exists in products.")
            return

        query = "INSERT INTO products(prodId, prodName, prodPrice) VALUES(%s, %s, %s)"
        details = (pid, stock_name, stock_price)
        cursor.execute(query, details)
        db.commit()
        refresh_products()

    except Exception as e:
        print("The exception is:", e)
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    finally:
        prodId.delete(0, END)



def removeProd():
    try:
        pid = prodId.get().strip()

        db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database='Shop')
        cursor = db.cursor()

        query = "DELETE FROM products WHERE LOWER(prodId) = %s"
        cursor.execute(query, (pid.lower(),))
        db.commit()
        refresh_products()

    except Exception as e:
        print("The exception is:", e)
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    finally:
            prodId.delete(0, END)


def refresh_products():
    for widget in labelFrame.winfo_children():
        widget.destroy()

    Label(labelFrame, text="Product", font=('calibri', 11, 'bold'), fg='black').grid(row=0, column=0, padx=60, pady=5, sticky='w')
    Label(labelFrame, text="Price", font=('calibri', 11, 'bold'), fg='black').grid(row=0, column=1, padx=60, pady=5, sticky='w')
    Label(labelFrame, text="Quantity", font=('calibri', 11, 'bold'), fg='black').grid(row=0, column=2, padx=60, pady=5, sticky='w')

    db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database='Shop')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products')
    res = cursor.fetchall()

    product_entries.clear()
    for idx, item in enumerate(res, start=1):
        Label(labelFrame, text=item[1], fg='black').grid(row=idx, column=0, padx=60, pady=3, sticky='w')
        Label(labelFrame, text=item[2], fg='black').grid(row=idx, column=1, padx=60, pady=3, sticky='w')
        entry = Entry(labelFrame)
        entry.grid(row=idx, column=2, padx=10, pady=3)
        product_entries.append((item, entry))




def generate_bill_number():
    return random.randint(1000000, 9999999)


#  PDF
def print_bill(totalBill, cName, dt, product_entries, billNumber):
    """طباعة الفاتورة كملف PDF مع رقم الفاتورة"""
    safe_name = re.sub(r'[^\w\-]', '_', cName)
    safe_date = re.sub(r'[^\w\-]', '_', dt)
    file_name = f"Bill_{billNumber}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    c.setFont("Helvetica", 10)

    c.drawString(100, 750, f"Bill Number: {billNumber}")
    c.drawString(100, 730, f"Bill for {cName}")
    c.drawString(100, 710, f"Date: {dt}")

    c.drawString(100, 690, "Product")
    c.drawString(200, 690, "Price")
    c.drawString(300, 690, "Quantity")
    c.drawString(400, 690, "Total")

    y = 670
    totalBill = 0
    for item, entry in product_entries:
        qty_text = entry.get().strip()
        if qty_text:
            try:
                qty = int(qty_text)
                product_name = item[1]  # الاسم
                price = int(item[2])  # السعر
                total = qty * price

                c.drawString(100, y, product_name)
                c.drawString(200, y, str(price))
                c.drawString(300, y, str(qty))
                c.drawString(400, y, str(total))

                totalBill += total
                y -= 20
            except ValueError:
                continue

    c.drawString(100, y - 30, f"Total Bill: {totalBill}")
    c.save()

    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_name)
        elif os.name == 'posix':  # Linux/macOS
            os.system(f'xdg-open "{file_name}"')  # أو 'open' للماك
    except Exception as e:
        print(f"Could not open the PDF file: {e}")

    return file_name

def store_bill_in_database(billNumber, totalBill, dt,meth):
    try:
        db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database="Shop")
        cursor = db.cursor()

        query = """
        INSERT INTO Bills (billNumber,billDatetime,totalPrice,method)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (billNumber,dt,totalBill,meth))  # تخزين اسم الإدمن في adminName

        db.commit()

        cursor.close()
        db.close()


    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")



def bill():
    global product_entries
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date.delete(0, END)
    date.insert(0, dt)
    cName = custName.get()
    meth = method.get()
    num = custNumb.get()
    totalBill = 0

    db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database='Shop')
    cursor = db.cursor()

    try:
        db.start_transaction()

        all_quantities_entered = True
        for item, entry in product_entries:
            if not entry.get().strip():
                all_quantities_entered = False
                break

        if not all_quantities_entered:
            messagebox.showwarning("Warning", "You must enter a quantity for every product.")
            return

        totalBill = 0
        billNumber = generate_bill_number()

        for item, entry in product_entries:
            qty_text = entry.get().strip()
            if qty_text:
                try:
                    qty = int(qty_text)
                    product_name = item[1]
                    prod_id = item[0]
                    price = int(item[2])
                    total = qty * price
                    totalBill += total

                    cursor.execute("SELECT quantity FROM stock WHERE prodId = %s", (prod_id,))
                    stock_data = cursor.fetchone()

                    if stock_data:
                        stock_quantity = stock_data[0]
                        if qty > stock_quantity:
                            messagebox.showwarning("Warning", f"The entered quantity for {product_name} exceeds the available stock. Only {stock_quantity} items available.")
                            db.rollback()
                            return

                        new_stock_quantity = stock_quantity - qty
                        cursor.execute("UPDATE stock SET quantity = %s WHERE prodId = %s", (new_stock_quantity, prod_id))
                    else:
                        messagebox.showwarning("Warning", f"Product ID {prod_id} not found in stock.")
                        db.rollback()
                        return

                except ValueError:
                    continue

        print_bill(totalBill, cName, dt, product_entries, billNumber)

        store_bill_in_database(billNumber, totalBill, dt, meth)

        admin_id = session.current_admin_id
        print(session.current_admin_id)

        for item, entry in product_entries:
            qty_text = entry.get().strip()
            if qty_text:
                try:
                    qty = int(qty_text)
                    prod_id = item[0]
                    cursor.execute("INSERT INTO Contains(prodId, billNumber, Quantity) VALUES (%s, %s, %s)", (prod_id, billNumber, qty))
                except:
                    continue

        cursor.execute("INSERT INTO Processes(billNumber, CustNumber, adminId) VALUES (%s, %s, %s)", (billNumber, num, admin_id))

        try:
            cursor.execute("DELETE FROM products")
        except:
            pass

        db.commit()
        messagebox.showinfo("Success", f"Bill generated successfully! Bill Number: {billNumber}")
        refresh_products()
        date.delete(0, END)
        date.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        custName.delete(0, END)
        custNumb.delete(0, END)
        method.set('')

    except Exception as e:
        db.rollback()
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        db.close()





def return_products_to_stock(billNumber, reason):
    if not billNumber:
        messagebox.showwarning("Warning", "Please enter a Bill Number before returning.")
        return
    if not reason:
        messagebox.showwarning("Warning", "Please enter a reason for the return.")
        return

    try:
        db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database='Shop')
        cursor = db.cursor()

        now = datetime.now()
        cursor.execute("""
            INSERT INTO Returns (billNumber, Return_Datetime, Reason)
            VALUES (%s, %s, %s)
        """, (billNumber, now, reason))

        cursor.execute("SELECT prodId, Quantity FROM Contains WHERE billNumber = %s", (billNumber,))
        products = cursor.fetchall()

        if not products:
            messagebox.showinfo("Info", "No products found for this bill number.")
            return

        for prodId, qty in products:
            cursor.execute("SELECT quantity FROM Stock WHERE prodId = %s", (prodId,))
            result = cursor.fetchone()
            if result:
                current_qty = result[0]
                new_qty = current_qty + qty
                cursor.execute("UPDATE Stock SET quantity = %s WHERE prodId = %s", (new_qty, prodId))
            else:
                messagebox.showwarning("Warning", f"Product ID {prodId} not found in stock.")
                continue

        db.commit()
        cursor.close()
        db.close()
        messagebox.showinfo("Success", f"Stock updated and return recorded successfully for bill {billNumber}")


    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")



def search_for_bill():
    global wn_search, billId_entry, labelFrame, reason_entry

    wn_search = tkinter.Tk()
    wn_search.title("Search for Bill")
    wn_search.iconbitmap("complex.ico")
    wn_search.configure(bg='#1f2020')
    wn_search.minsize(width=600, height=600)
    wn_search.geometry("750x650+{}+{}".format(
        int(wn_search.winfo_screenwidth() / 2 - 780 / 2),
        int(wn_search.winfo_screenheight() / 2 - 670 / 2)))

    headingFrame = Frame(wn_search, bg="snow3")
    headingFrame.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.2)

    Label(headingFrame, text="Bill Number : ", fg='black').place(relx=0.05, rely=0.25, relheight=0.15)
    billId_entry = Entry(headingFrame)
    billId_entry.place(relx=0.3, rely=0.25, relwidth=0.4, relheight=0.15)

    Label(headingFrame, text="Return Reason : ", fg='black').place(relx=0.05, rely=0.55, relheight=0.15)
    reason_entry = Entry(headingFrame)
    reason_entry.place(relx=0.3, rely=0.55, relwidth=0.4, relheight=0.15)

    Button(headingFrame, text="Search", bg='snow3', fg='black', command=display_bill_contents).place(relx=0.75, rely=0.25, relwidth=0.2, relheight=0.18)

    labelFrame = Frame(wn_search)
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    Button(wn_search, text="Return", bg='snow3', fg='black',
           command=lambda: (
           return_products_to_stock(billId_entry.get().strip(), reason_entry.get().strip()), wn_search.destroy())
           ).place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.08)

    wn_search.mainloop()


def display_bill_contents():
    billNumber = billId_entry.get().strip()
    if not billNumber:
        messagebox.showwarning("Warning", "Please enter a Bill Number.")
        return

    for widget in labelFrame.winfo_children():
        widget.destroy()

    Label(labelFrame, text="Product", font=('calibri', 11, 'bold'), fg='black').grid(row=0, column=0, padx=60, pady=5, sticky='w')
    Label(labelFrame, text="Price", font=('calibri', 11, 'bold'), fg='black').grid(row=0, column=1, padx=60, pady=5, sticky='w')
    Label(labelFrame, text="Quantity", font=('calibri', 11, 'bold'), fg='black').grid(row=0, column=2, padx=60, pady=5, sticky='w')

    try:
        db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database='Shop')
        cursor = db.cursor()

        # تحقق إذا كانت الفاتورة مرتجعة مسبقًا
        cursor.execute("SELECT 1 FROM Returns WHERE billNumber = %s", (billNumber,))
        already_returned = cursor.fetchone()
        if already_returned:
            messagebox.showwarning("Warning", f"Bill number {billNumber} has already been returned.")
            cursor.close()
            db.close()
            return

        cursor.execute("""
            SELECT s.prodName, s.prodPrice, c.Quantity 
            FROM Contains c 
            JOIN Stock s ON c.prodId = s.prodId 
            WHERE c.billNumber = %s
        """, (billNumber,))
        items = cursor.fetchall()
        cursor.close()
        db.close()

        if not items:
            messagebox.showinfo("Info", "No products found for this bill number.")
            return

        for idx, (prodName, prodPrice, qty) in enumerate(items, start=1):
            Label(labelFrame, text=prodName, fg='black').grid(row=idx, column=0, padx=60, pady=3, sticky='w')
            Label(labelFrame, text=prodPrice, fg='black').grid(row=idx, column=1, padx=60, pady=3, sticky='w')
            Label(labelFrame, text=qty, fg='black').grid(row=idx, column=2, padx=60, pady=3, sticky='w')

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")





def newCust():
    global wn, name1, name2, name3, date, custName, product_entries, method, custNumb, prodId, labelFrame

    wn = tkinter.Tk()
    wn.title("Complex Cashier System")
    wn.iconbitmap("complex.ico")
    wn.configure(bg='#1f2020')
    width = int(wn.winfo_screenwidth() * 0.6)
    height = int(wn.winfo_screenheight() * 0.85)
    x = int((wn.winfo_screenwidth() - width) / 2)
    y = int((wn.winfo_screenheight() - height) / 2)

    wn.geometry(f"{width}x{height}+{x}+{y}")

    headingFrame1 = Frame(wn, bg="snow3")
    headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.16)

    Label(headingFrame1, text="Product Id : ", fg='black').place(relx=0.05, rely=0.45, relheight=0.18)
    prodId = Entry(headingFrame1)
    prodId.place(relx=0.21, rely=0.45, relwidth=0.35, relheight=0.18)

    Button(headingFrame1, text="ADD", bg='snow3', fg='black', command=prodtoTable).place(relx=0.6, rely=0.45, relwidth=0.15, relheight=0.2)
    Button(headingFrame1, text="DELETE", bg='snow3', fg='black', command=removeProd).place(relx=0.8, rely=0.45, relwidth=0.15, relheight=0.2)

    Label(wn, text="Datetime:", fg='black').place(relx=0.1, rely=0.3)
    date = Entry(wn)
    date.place(relx=0.235, rely=0.3, relwidth=0.22)
    date.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    Label(wn, text="Method:", fg='black').place(relx=0.53, rely=0.3)
    method = ttk.Combobox(wn, values=["Cash", "Visa"])
    method.place(relx=0.67, rely=0.3, relwidth=0.22)

    Label(wn, text="Customer Name:", fg='black').place(relx=0.1, rely=0.35)
    custName = Entry(wn)
    custName.place(relx=0.235, rely=0.35, relwidth=0.22)

    Label(wn, text="Customer Number:", fg='black').place(relx=0.53, rely=0.35)
    custNumb = Entry(wn)
    custNumb.place(relx=0.67, rely=0.35, relwidth=0.22)

    labelFrame = Frame(wn)
    labelFrame.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.4)

    product_entries.clear()
    refresh_products()

    Button(wn, text="Generate Bill", bg='snow3', fg='black', command=bill).place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)
    Button(wn, text="Quit", bg='snow3', fg='black', command=on_close).place(relx=0.55, rely=0.9, relwidth=0.18, relheight=0.08)

    image_3 = PhotoImage(file="return (1).png")

    Btn3 = Button(wn, bg='white', image=image_3, bd=0, borderwidth=1, highlightthickness=1,
                  command=search_for_bill)
    Btn3.place(relx=0.85, rely=0.2, width=40, height=40)

    wn.protocol("WM_DELETE_WINDOW", on_close)

    wn.mainloop()

def on_close():
    global wn
    if session.current_admin_id is not None and session.login_time is not None:
        logout_time = datetime.now()
        try:
            db = mysql.connector.connect(user="root", passwd="Test@1234", host="localhost", database="Shop")
            cursor = db.cursor()
            insert_query = """
            INSERT INTO Login_Activity (adminId, Login_Datetime, Logout_Datetime)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (session.current_admin_id, session.login_time, logout_time))
            db.commit()
            cursor.close()
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to log login activity: {e}")

    wn.destroy()



product_entries = []



    #///////////////////////////////////////////////////////////////////////////////////////////////////

                                #اللهم لك الحمد حمدا كثيرا طيبا مباركا فيه


    #///////////////////////////////////////////////////////////////////////////////////////////////////


