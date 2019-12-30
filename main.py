from tkinter import *
from tkinter import filedialog
from PIL import Image
import io


def paint(event):
    python_green = "#476042"
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    w.create_oval(x1, y1, x2, y2, fill=python_green)


def clear_canvas():
    w.delete("all")


def recognize():
    TEMP_PATH = "C:\\Studia\\7 semestr\\SI\\cw3\\temp\\test.png"
    ps = w.postscript(colormode="mono")
    ps_im = Image.open(io.BytesIO(ps.encode('utf-8')))
    ps_im.save(TEMP_PATH)

    img = Image.open(TEMP_PATH, mode='r')
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    print(list(img.getdata()))


master = Tk()
master.title("Letter recognition")
master.geometry("300x300")

canvas_width = 100
canvas_height = 100

w = Canvas(master,
           width=canvas_width,
           height=canvas_height,
           borderwidth=2,
           relief="groove",
           bg="white")
w.pack(expand="True")
w.bind("<B1-Motion>", paint)

clearBtn = Button(master, text="Clear", command=clear_canvas)
clearBtn.pack(side=BOTTOM, pady=5, ipady=5, ipadx=22)

recognizeBtn = Button(master, text="Recognize", command=recognize)
recognizeBtn.pack(side=BOTTOM, pady=5, ipady=5, ipadx=10)

message = Label(master, text="Draw A, B or C in the canvas and click Recognize")
message.pack(side=BOTTOM, pady=10)

mainloop()
