import sqlite3, hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial

#db code
with sqlite3.connect("vault.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
    id INTEGER PRIMARY KEY,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
    id INTEGER PRIMARY KEY,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

#Create PopUp
def popUp(text):
    answer = simpledialog.askstring("input string", text)
    return answer

  

#initial code
window = Tk()
window.title("Password Vault")

def fScreen():
    window.geometry("350x150")

    lbl = Label(window, text="Create New Master Pass")
    lbl.pack(ipadx=10, ipady=5)

    txt = Entry(window, text="Enter New Pass", show="*")
    txt.pack()
    txt.focus()

    lbl2 = Label(window, text="Re-enter Pass")
    lbl2.pack(ipadx=10, ipady=5)

    txt2 = Entry(window, show="*")
    txt2.pack()

    wrong = Label(window)
    wrong.pack(ipadx=10, ipady=5)

    def savePass():
        if txt.get() == txt2.get():
            hashedPass = txt.get()
            
            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?) """
            cursor.execute(insert_password, [(hashedPass)])
            db.commit()

            bigV()
        else:
            wrong.config(text="Pass don't match dumbfuck")

    btn = Button(window, text="Enter", command=savePass)
    btn.pack()

def loginScreen():
    window.geometry("350x150")

    lbl = Label(window, text="Enter Master Password")
    lbl.pack(ipadx=10, ipady=10)

    txt = Entry(window, text="Enter Password", show="*")
    txt.pack()
    txt.focus()

    wrong = Label(window)
    wrong.pack(pady=5)

    def getMasterPass():
        checkHashedPass = txt.get()
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkHashedPass)])
        return cursor.fetchall()

    def checkPass():
        match = getMasterPass()

        if match:
            bigV()
        else:
            wrong.config(text="fuck off")


    btn = Button(window, text="Submit", command=checkPass)
    btn.pack(pady=10)

def bigV():
        for widget in window.winfo_children():
            widget.destroy()


        def addEntry():
            text1="Websites"
            text2="Username"
            text3="Password"


            website = popUp(text1)
            username = popUp(text2)
            password = popUp(text3)

            insert_fields = """INSERT INTO vault(website,username,password)
            VALUES(?, ?, ?)"""

            cursor.execute(insert_fields, (website, username, password))
            db.commit()

            bigV()

        def removeEntry(input):
            cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
            db.commit()

            bigV()

        window.geometry("700x350")

        lbl = Label(window, text="BigVault")
        lbl.grid(column=1)

        btn = Button(window, text="+", command=addEntry)
        btn.grid(column=1, pady = 10)

        lbl = Label(window, text="Website")
        lbl.grid(row=2, column=0, padx=80)
        lbl = Label(window, text="Username")
        lbl.grid(row=2, column=1, padx=80)
        lbl = Label(window, text="Password")
        lbl.grid(row=2, column=2, padx=80)

        cursor.execute("SELECT * FROM vault")
        if(cursor.fetchall() != None):
            i=0
            while True:
                cursor.execute("SELECT * FROM vault")
                array = cursor.fetchall()

                lbl1 = Label(window, text=(array[i][1]), font=("Helvetica", 12))
                lbl1.grid(column = 0, row = i + 3)
                lbl1 = Label(window, text=(array[i][2]), font=("Helvetica", 12))
                lbl1.grid(column = 1, row = i + 3)
                lbl1 = Label(window, text=(array[i][3]), font=("Helvetica", 12))
                lbl1.grid(column = 2, row = i + 3)

                btn = Button(window, text="Delete", command= partial(removeEntry, array[i][0]))
                btn.grid(column = 3, row = i + 3, pady= 10)

                i=i+1

                cursor.execute("SELECT * FROM vault")
                if (len(array) == 0):
                    break

cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginScreen()
else:
    fScreen()

window.mainloop()
