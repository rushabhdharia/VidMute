from Tkinter import *
import cv2
import numpy as np
from PIL import Image
from PIL import ImageGrab
import subprocess
import threading

count=0

def change():
    global count
    i=0
    j=0
    x=0
    ImageGrab.grab().save("grab.jpg", "JPEG")
    im=Image.open("grab.jpg")
    u,v=im.size
    if count==0:
       count=1
       while(count==1):
          ImageGrab.grab().crop((0,v-100,400,v)).save("grab.jpg", "JPEG")
          image = cv2.imread("grab.jpg")
          hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
          lower_red = np.array([22,150,150])
          upper_red= np.array([25,255,255])
          mask = cv2.inRange(hsv, lower_red, upper_red)
          cv2.imwrite("process.jpg", mask)
          img = cv2.imread("process.jpg")
          gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
          edges = cv2.Canny(gray, 80, 120)
          lines = cv2.HoughLinesP(edges, 1, np.pi/2, 1, None, 20, 1)
          a=str(lines)
          if a in ['None']:
              i=0
              j+=1
              if(j==5):
                  j=0
                  if(x==0):
                      x=1
                      subprocess.call(['nircmd.exe','mutesysvolume','0'])
          else:
              j=0
              if(x==1):
                  x=0
                  subprocess.call(['nircmd.exe','mutesysvolume','1'])

    elif count==1:
        count=0
        labelText1.set("Click here to Start")

    return

t=threading.Thread(target=change)

app = Tk()
app.title("VidMute_beta_1")
app.iconbitmap(bitmap=None, default="icon1.ico")
app.geometry("550x450+200+200")

label1 = Label(app, text="Note: Works properly for Full Screen Videos",height=3,foreground="red")
label1.pack(side="top")

labelText1= StringVar()
labelText1.set("Click here to Start")
button1 = Button(app, textvariable=labelText1,width=20,command=lambda:t.start())
button1.pack(padx=15,pady=15)

labelText2= StringVar()
labelText2.set("Click here to Stop")
button2 = Button(app, textvariable=labelText2,width=20,command=app.destroy)
button2.pack(padx=15,pady=15)

label2 = Label(app, text="Contact Us at \n rushabh.dharia@outlook.com\nchirag.jain1996@outlook.com",height=3)
label2.pack(side="bottom")

label1 = Label(app, text="Developed By \nChirag Jain & Rushabh Dharia",height=3)
label1.pack(side="bottom")

app.mainloop()
