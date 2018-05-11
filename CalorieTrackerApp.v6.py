#Import required libraries
from datetime import datetime
from tkinter import *

import sqlite3
import tkinter.ttk as ttk
sqlite_file='CalorieTracker.db'

#Set up GUI Canvas
root = Tk()
root.title('Daily Calorie Tracker')
root['bg'] = 'lightblue'
root.geometry("500x350+0+0")
root.resizable(False, False)

conn=sqlite3.connect(sqlite_file)
c=conn.cursor()

#Create exit button
class quitButton(Button):
    def __init__(self, parent):
        Button.__init__(self, parent)
        self['text'] = 'Quit'
        self['command'] = parent.destroy
        self.pack(side=BOTTOM, anchor=E)

#Create label for current date display
class dateLabel(Label):
    def __init__(self, parent):
        Label.__init__(self, parent)
        self['text'] = 'DATE:', datetime.now().date()
        self.pack(side=TOP, anchor=E)

#Create label for drop down menu
class foodLabel(Label):
    def __init__(self, parent):
        Label.__init__(self, parent)
        self['text'] = 'Enter Food Above'
        self.pack(side=TOP, anchor=W)

#Create dropdown menu
def chooseOption(value):
    tmp=c.execute("SELECT Calories FROM Calorie_Values WHERE FoodName=?", (value))
    out = tmp.fetchone()
    printfoodListlabel['text']=out
    printfoodListlabel.pack()
#save each value as it is chosen
    savedata(int(out[0]))

choice=[]

for row in c.execute('SELECT FoodName FROM Calorie_Values'):
    choice.append(row)

value = StringVar()

choose=OptionMenu(root, value, *choice, command = chooseOption)
choose['text']='List of foods'
choose.pack(anchor=SW)

#Save data from any entries chosen in Db/User_Repository
def savedata(amount):
    print("saving {}".format((datetime.now().date(),amount)))
    tmp1=c.execute("INSERT INTO Calorie_Intake(Date,CaloriesConsumed) VALUES (?,?)", (str(datetime.now().date()),amount))
    out = tmp1.fetchone()
    #Add dummy label to execute with total calorie count (following)
    printDummyLabel['text']=out
    printDummyLabel.pack(side=BOTTOM)
    conn.commit()
    #Add total calorie count to this function so that it executes constantly
    tmp2=c.execute("SELECT SUM(CaloriesConsumed) FROM Calorie_Intake WHERE Date=(?) GROUP BY Date", [(str(datetime.now().date(),))])
    out = tmp2.fetchone()
    printTotCalLabel['text']=out
    printTotCalLabel.pack(side=BOTTOM)
    conn.commit()

#Create label for calorie value associated with food chosen
class calorieIntake(Label):
    def __init__(self, parent):
        Label.__init__(self, parent)
        self['text'] = 'Calorie Value: '
        self.pack(anchor=W, pady=30)

#Display calorie value associated with food chosen
printfoodListlabel=Label(root, bg="white", fg="blue", font='times 25', height=2, width=10)

#Display total calorie count for user
printTotCalLabel=Label(root, bg="white", fg="purple", font="times 25", height=2, width=10)
#Display total calories consumed
printDummyLabel=Label(root, bg="lightblue")

#Create label for total calories consumed
class totCalorieCount(Label):
    def __init__(self, parent):
        Label.__init__(self, parent)
        self['text'] = 'Total Calories Consumed: '
        self.pack(side=LEFT, pady=20)

#Execute all [packed] commands of GUI
status = Frame(root)

quitButton(root)
dateLabel(root)
foodLabel(root)
calorieIntake(root)
totCalorieCount(root)

action = Frame(root)
action['bg']= 'lightblue'

status.pack()
action.pack()

mainloop()
