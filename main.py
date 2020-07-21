import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time

#set the height and weight of the page
SET_WEIDTH = 1000
SET_HEIGHT = 600

stream = cv2.VideoCapture("run.mp4")
flag = True
def play(speed):
    global flag
    print(f"Speed is : {speed}")

    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WEIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134,26,fill = 'white',font ="Times 28 italic bold",text = "Decision pending")
    flag = not flag

def pending(decision):
    # 1 Display decision pending
    frame = cv2.cvtColor(cv2.imread("pending.jpeg"),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width = SET_WEIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image= frame, anchor=tkinter.NW)
    # 2 wait for 1 sec
    time.sleep(1)
    # 3 Display sponcer image
    frame = cv2.cvtColor(cv2.imread("sponcer.jpeg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WEIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    # 4 wait for 1.5 sec
    time.sleep(1.5)
    # 5 Display out/not out
    if decision == 'out':
        decisionImg = "out.jpeg"
    else:
        decisionImg = "not-out.jpeg"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WEIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("player is out")

def not_out():
    thread = threading.Thread(target=pending, args=("Not out",))
    thread.daemon = 1
    thread.start()
    print("player is NOT out")


# Tkinter gui starts here
window = tkinter.Tk()
window.title("Decision review kit")
cv_img = cv2.cvtColor(cv2.imread("DRS.jpeg"),cv2.COLOR_BGR2BGRA)
canvas = tkinter.Canvas(window,width = SET_WEIDTH,height = SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0,0, ancho =tkinter.NW,image = photo)
canvas.pack()

#button to control playback
btn = tkinter.Button(window, text = "<< Previous (fast)",width =50,command = partial(play,-25))
btn.pack()

btn = tkinter.Button(window, text = "<< Previous (slow)",width =50,command = partial(play,-2))
btn.pack()

btn = tkinter.Button(window, text = "<< Next (fast)",width =50,command = partial(play,2))
btn.pack()

btn = tkinter.Button(window, text = "<< Next (slow)",width =50,command = partial(play,25))
btn.pack()

btn = tkinter.Button(window, text = " Give OUT",width =50 ,command = out)
btn.pack()

btn = tkinter.Button(window, text = "Give NOT OUT",width =50,command = not_out)
btn.pack()

window.mainloop()