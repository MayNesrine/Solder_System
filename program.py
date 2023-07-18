import sys
import os
import time
from tkinter import *
import tkinter.simpledialog as sd
from tkinter import messagebox
import RPi.GPIO as GPIO
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(_file_)))))
from DFRobot_MAX31855 import *
I2C_1       = 0x01
I2C_ADDRESS = 0x10
#Create MAX31855 object
max31855 = DFRobot_MAX31855(I2C_1 ,I2C_ADDRESS)
# Configuration du GPIO
M= 17
verinS1= 20
verinS2= 21
chauf_bobine = 16
ref=26
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(M, GPIO.OUT)
GPIO.setup(verinS1, GPIO.OUT)
GPIO.setup(verinS2, GPIO.OUT)
GPIO.setup(chauf_bobine, GPIO.OUT)
GPIO.setup(ref, GPIO.OUT)
x1, y1 = 10, 10
x2, y2,y3,y4,y5 = 10, 50,90,130,170
enable='light grey'
font=("Times New Roman", 15, "italic","bold")
font1=("Times New Roman", 10, "italic","bold")
def tkinter_frame(fenetre,taille,titre,couleur):
    fenetre.geometry((taille))
    fenetre.title(titre)
    fenetre.geometry(taille)
    fenetre.title(titre)
    fenetre.configure(bg=couleur)
    fenetre.resizable(height=False,width=False)
    fenetre.eval('tk::PlaceWindow . center')
    fenetre.update()
    return fenetre
def temp():
    value = sd.askinteger("Title", "entrez le Temps de échauffement bobine", initialvalue=0)
    if value is not None: # check if user pressed OK or Cancel button
        print(f"You entered {value}")
        global t
        t=value
    else:
        print("Dialog cancelled")
def temp1():
    _value = sd.askinteger("Title", "entrez le Temps de réfroidissement bobine", initialvalue=1)
    if _value is not None : # check if user pressed OK or Cancel button
        print(f"You entered {_value}")
        global k
        k=_value
    else:
        print("Dialog cancelled")
taille='450x320'
titre="Machine de sodure"
couleur="light blue"
fenetre= Tk()
fenetre=tkinter_frame(fenetre,taille,titre,couleur)
frame = Frame(fenetre, bg='light blue')
frame.grid(row=0, column=0)
temp()
temp1()
l1 = Label(frame, text =" Temps d'echaufemment\n {} seconde".format(t))
l3 = Label(frame,  text =" Temps de réfroidissmemnt\n {} seconde".format(k))
temp_label = Label(frame, text = "",font=font1,width=10, background='light blue')
#button = Button(frame, text=f"Button")
l1.grid(row=0, column=0, padx=5, pady=5)
temp_label.grid(row=0, column=2, padx=5, pady=5)
l3.grid(row=0, column=1, padx=5, pady=5)
frame2 = Frame(fenetre,  bg='light blue')
frame2.grid(row=1, column=0,sticky = W)
can1 = Canvas(frame2,bg='dark grey',height=200,width=300)
can2 = Canvas(frame2,bg='dark grey',height=200,width=50)
can1.grid(row=0, column=0, padx=5, pady=5)
can2.grid(row=0, column=1, padx=5, pady=5)
oval1 = can2.create_oval(x1,y1,x1+30,y1+30,width=2,fill=enable)
oval2 = can2.create_oval(x2,y2,x2+30,y2+30,width=2,fill=enable)
oval3 = can2.create_oval(x2,y3,x2+30,y3+30,width=2,fill=enable)
oval4 = can2.create_oval(x2,y4,x2+30,y4+30,width=2,fill=enable)
oval5 = can2.create_oval(x2,y5,x2+30,y5+30,width=2,fill=enable)
text1 = can1.create_text(120, 25, text="", font=font,fill='red')
text2 = can1.create_text(120, 65, text="", font=font,fill='blue')
text3 = can1.create_text(120, 105, text="", font=font,fill='yellow')
text4 = can1.create_text(120, 145, text="", font=font,fill='green')
text5 = can1.create_text(120, 185, text="", font=font,fill='cyan')
frame3 = Frame(fenetre, bg='white')
frame3.grid(row=2, column=0)
b1 = Button(frame3, text = "Start    ",width=20,command=lambda:[loop()])
b2 = Button(frame3, text = "Quitter",width=20,command=lambda:[stop(),fenetre.quit()])
b1.grid(row = 0, column = 0, sticky = N)
b2.grid(row = 1, column = 0,)
def moteur():
    can2.itemconfig(oval2, fill='blue')
    can2.itemconfig(oval1, fill='light grey')
    can1.itemconfig(text1, text="   Dosage Términé         ",)
    can1.itemconfig(text2, text="   Monté de l'enduit      ",)
    GPIO.output(M, GPIO.LOW)
    GPIO.output(verinS1, GPIO.HIGH)
    fenetre.after(5000, chaufemmeent)
def chaufemmeent():
    print("dosage terminé")
    can2.itemconfig(oval3, fill='yellow')
    can2.itemconfig(oval2, fill='light grey')
    GPIO.output(verinS1, GPIO.LOW)
    GPIO.output(chauf_bobine, GPIO.HIGH)
    can1.itemconfig(text3, text="      Echauffement bobine  ",)
    can1.itemconfig(text2, text="      Induit en postion   ",)
    fenetre.after(t*1000, descent)
def descent():
    GPIO.output(chauf_bobine, GPIO.LOW)
    GPIO.output(verinS2, GPIO.HIGH)
    can1.itemconfig(text3, text="      Température atteint  ",)
    can2.itemconfig(oval3, fill='light grey')
    can2.itemconfig(oval4, fill='green')
    can1.itemconfig(text4, text="   Descent de l'induit     ",)
    fenetre.after(5000, referoidissement)
def referoidissement():
    GPIO.output(verinS2, GPIO.LOW)
    can2.itemconfig(oval5, fill='cyan')
    can1.itemconfig(text4, text="   Induit en position bas    ",)
    can2.itemconfig(oval4, fill='light grey')
    can1.itemconfig(text5, text="    Refroidissement bobine  ",)
    GPIO.output(ref, GPIO.HIGH)
    fenetre.after(k*1000, stop)
def stop():
    print("stop")
    GPIO.output(verinS2, GPIO.LOW)
    GPIO.output(verinS1, GPIO.LOW)
    GPIO.output(ref, GPIO.LOW)
    GPIO.output(chauf_bobine, GPIO.LOW)
    GPIO.output(M, GPIO.LOW)
    can2.itemconfig(oval1, fill='light grey')
    can2.itemconfig(oval2, fill='light grey')
    can2.itemconfig(oval3, fill='light grey')
    can2.itemconfig(oval4, fill='light grey')
    can2.itemconfig(oval5, fill='light grey')
    can1.itemconfig(text1, text=" ",)
    can1.itemconfig(text2, text=" ",)
    can1.itemconfig(text3, text=" ",)
    can1.itemconfig(text4, text=" ",)
    can1.itemconfig(text5, text=" ",)
    b1.configure(state="active")
def loop():
    GPIO.output(M, GPIO.HIGH)
    can2.itemconfig(oval1, fill='red')
    can1.itemconfig(text1, text="  Dosage d'étain            ",)
    b1.configure(state="disabled")
    fenetre.after(5000, moteur);l
def update_temperature():
    # Read the CPU temperature
    bobine_temp = max31855.read_celsius()
    temp_label.config(text="T: {:.1f} °C".format(bobine_temp))
    fenetre.after(1000, update_temperature)
    tmp_seil=34
    if(bobine_temp>=tmp_seil):
        messagebox.showwarning("Avertissement de température", "La température est au-dessus du seuil de {} degrees Celsius.".format(tmp_seil))

if __name__=="__main_":
    update_temperature()
    fenetre.mainloop()