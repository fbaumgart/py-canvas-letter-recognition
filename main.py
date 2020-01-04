from tkinter import *
from PIL import Image
import io


def paint(event):
    python_green = "#476042"
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    w.create_oval(x1, y1, x2, y2, fill=python_green)


def clear_canvas():
    w.delete("all")


def convert_list_of_RGB_tuples_to_list_of_bytes(param):
    new_list_of_bytes = []
    for i in param:
        for j in i:
            if i[0] == 255:
                new_list_of_bytes.append(0)
            elif i[0] == 0:
                new_list_of_bytes.append(1)
            break

    print(len(new_list_of_bytes))
    print(new_list_of_bytes)
    return new_list_of_bytes


def recognize():
    SAVE_PATH = "C:\\Studia\\7 semestr\\SI\\cw3\\temp\\test.png"
    ps_from_canvas = w.postscript(colormode="mono")
    image = Image.open(io.BytesIO(ps_from_canvas.encode('utf-8')))
    image.save(SAVE_PATH, format='PNG')

    list_of_RGB_tuples_from_image = list(image.getdata())
    convert_list_of_RGB_tuples_to_list_of_bytes(list_of_RGB_tuples_from_image)


#learning mode window code
def learning_mode():

    def paint(event):
        python_green = "#476042"
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        w.create_oval(x1, y1, x2, y2, fill=python_green)

    def clear_canvas():
        w.delete("all")

    #def display_letter_choice():
     #   print(radio_variable.get())

    master.destroy()
    learning_window = Tk()
    learning_window.title("Letter recognition - learning mode")
    learning_window.geometry("300x300")
    w = Canvas(learning_window,
               width=canvas_width,
               height=canvas_height,
               borderwidth=2,
               relief="groove",
               bg="white")
    w.pack(expand="True")
    w.bind("<B1-Motion>", paint)

    clear_button = Button(learning_window, text="Clear", command=clear_canvas)
    clear_button.pack(side=BOTTOM, pady=5, ipady=5, ipadx=22)

    learn_button = Button(learning_window, text="Learn", command=clear_canvas)
    learn_button.pack(side=BOTTOM, pady=5, ipady=5, ipadx=22)

    radio_variable = IntVar()
    radio_variable.set(0)
    Radiobutton(learning_window, text="A", variable=radio_variable, value=0).pack()
    Radiobutton(learning_window, text="B", variable=radio_variable, value=1).pack()
    Radiobutton(learning_window, text="C", variable=radio_variable, value=2).pack()
    letter_choice = radio_variable.get()

    message = Label(learning_window, text="Choose the character, draw and click Learn")
    message.pack(side=BOTTOM, pady=10)

    #display_letter_button = Button(learning_window, text="Display", command=display_letter_choice).pack()

    mainloop()


master = Tk()
master.title("Letter recognition")
master.geometry("300x300")

canvas_width = 28
canvas_height = 28

w = Canvas(master,
           width=canvas_width,
           height=canvas_height,
           borderwidth=2,
           relief="groove",
           bg="white")
w.pack(expand="True")
w.bind("<B1-Motion>", paint)

clear_button = Button(master, text="Clear", command=clear_canvas)
clear_button.pack(side=BOTTOM, pady=5, ipady=5, ipadx=22)

recognize_button = Button(master, text="Recognize", command=recognize)
recognize_button.pack(side=BOTTOM, pady=5, ipady=5, ipadx=10)

message = Label(master, text="Draw A, B or C in the canvas and click Recognize")
message.pack(side=BOTTOM, pady=10)

menu_bar = Menu(master)
menu_bar.add_command(label="Learning mode", command=learning_mode)

master.config(menu=menu_bar)

mainloop()
