import tkinter as tk
import time
from MySQLdb import connect

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root['background'] = "#004ba0"
        self.root.title("Post-It")
        #CHANGE BACK TO 10 MINUTES
        self.minutes = 1
        self.seconds = 0
        self.greeting = tk.Label(text="Welcome to Post-It!", bg="#63a4ff")
        self.greeting.config(font=("Arial", 22))
        self.greeting.pack()
        self.inputField = tk.Text(bg="#bbdefb")
        self.inputField.pack()
        self.buttonRow = tk.Frame()
        self.viewBoard = tk.Button(
            self.buttonRow,
            text="View board",
            width = 15,
            height=2,
            bg="#1976d2",
            fg="#ffffff",
            command=self.viewMessage
        )

        self.viewBoard.config(font=("Arial 10 bold"))
        self.viewBoard.pack(side = "left")

        self.submit = tk.Button(self.buttonRow,
            text="Submit message",
            width=15,
            height=2,
            bg="#1976d2",
            fg="#ffffff",
            command=self.submitMessage
        )

        self.submit.config(font=("Arial 10 bold"))
        self.submit.pack(side = "left")

        self.timerDisplay = tk.Label(self.buttonRow, text = str(self.minutes) + ":" + str(self.seconds) + "0")
        self.timerDisplay.config(font=("Arial 10 bold"))
        self.timerDisplay.pack(side = "left")

        self.buttonRow.pack()
        self.timerDisplayUpdate()
        self.view = None
        self.root.mainloop()

    def timerDisplayUpdate(self):
        #if timer runs out
        if (self.minutes == 0 and self.seconds == 0):
            self.deleteMessages()
            self.minutes = 10
            if (self.view): 
                self.view.destroy()
            #call delete function
        #if we reach the end of any minute other than 0
        elif (self.seconds == 0):
            self.minutes = self.minutes - 1
            self.seconds = 59
        #any other case
        else:
            self.seconds = self.seconds-1
        time = str(self.minutes) + ":" + str(self.seconds)
        if (self.seconds < 10):
            if (self.seconds == 0):
                time = str(self.minutes) + ":" + str(self.seconds) + "0"
            else:
                time = str(self.minutes) + ":" + "0" + str(self.seconds) 
        self.timerDisplay.config(text=time)
        self.root.after(1000, self.timerDisplayUpdate)
    
    def deleteMessages(self):
        #delete from database
        cnx = connect(user='DbTyXibSpj', password='qBhvLikFaL', host='remotemysql.com', database='DbTyXibSpj')
        cursor = cnx.cursor()
        specs = "DELETE FROM Messages;"
        cursor.execute(specs)
        cnx.commit()
        cnx.close()
    
    def submitMessage(self):
        #insert message into database
        #when submitting, refresh the bulletin window to display latest message
        cnx = connect(user='DbTyXibSpj', password='qBhvLikFaL', host='remotemysql.com', database='DbTyXibSpj')
        cursor = cnx.cursor()
        val = self.inputField.get("1.0", "end")
        specs = "INSERT INTO Messages VALUES ('%s');" %val
        cursor.execute(specs)
        cnx.commit()
        cnx.close()
        self.inputField.delete("1.0", "end")
    
    def viewMessage(self):
        #open new window, load in existing messages
        #read from database
        window = tk.Toplevel(self.root)
        self.view = window
        window['background'] = "#63cdd7"
        cnx = connect(user='DbTyXibSpj', password='qBhvLikFaL', host='remotemysql.com', database='DbTyXibSpj')
        cursor = cnx.cursor()
        specs = "SELECT * FROM Messages;"
        cursor.execute(specs)
        for message in cursor:
            msg = tk.Label(window, text=message[0], fg="#1976d2", bg="#bbdefb", borderwidth=2, relief = "groove")
            msg.config(font=("Arial 10 bold"))
            msg.pack()

app = App()
""" window = tk.Tk()
window['background'] = "#004ba0"
minutes = 10
seconds = 0
greeting = tk.Label(text="Welcome to Post-It!", bg="#63a4ff")
greeting.config(font=("Arial", 22))
greeting.pack()

inputField = tk.Text(bg="#bbdefb")
inputField.pack()

buttonRow = tk.Frame()

viewBoard = tk.Button(
    buttonRow,
    text="View board",
    width = 15,
    height=2,
    bg="#1976d2",
    fg="#ffffff"
)

viewBoard.config(font=("Arial 10 bold"))
viewBoard.pack(side = "left")

submit = tk.Button(
    buttonRow,
    text="Submit message",
    width=15,
    height=2,
    bg="#1976d2",
    fg="#ffffff"
)

submit.config(font=("Arial 10 bold"))
submit.pack(side = "left")

timerDisplay = tk.Label(buttonRow, text = str(minutes) + ":" + str(seconds) + "0")
timerDisplay.config(font=("Arial 10 bold"))
timerDisplay.pack(side = "right")

buttonRow.pack()
timerDisplayUpdate()

window.mainloop()


def timerDisplayUpdate():
    #if timer runs out
    if (minutes == 0 and seconds == 0):
        print("hello")
        #call delete function
    #if we reach the end of any minute other than 0
    elif (seconds == 0):
        minutes = minutes - 1
        seconds = 59
    #any other case
    else:
        seconds = seconds-1
    time = minutes + ":" + seconds
    if (seconds == 0):
        time = minutes + ":" + seconds + "0"
    timerDisplay.config(text=time)
    window.after(1000, timerDisplayUpdate)
    
 """