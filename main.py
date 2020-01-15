from tkinter import *
from PIL import Image
import io
import numpy as np
import csv


class NeuralNetwork:

    # intialize variables in class
    def __init__(self, inputs, outputs):
        self.inputs  = inputs
        self.outputs = outputs
        # initialize weights as .50 for simplicity
        self.weights = np.array([[.50], [.50], [.50]])
        self.error_history = []
        self.epoch_list = []

    #activation function ==> S(x) = 1/1+e^(-x)
    def sigmoid(self, x, deriv=False):
        if deriv == True:
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))

    # data will flow through the neural network.
    def feed_forward(self):
        self.hidden = self.sigmoid(np.dot(self.inputs, self.weights))

    # going backwards through the network to update weights
    def backpropagation(self):
        self.error  = self.outputs - self.hidden
        delta = self.error * self.sigmoid(self.hidden, deriv=True)
        self.weights += np.dot(self.inputs.T, delta)

    # train the neural net for 25,000 iterations
    def train(self, epochs=1500):
        for epoch in range(epochs):
            # flow forward and produce an output
            self.feed_forward()
            # go back though the network to make corrections based on the output
            self.backpropagation()
            # keep track of the error history over each epoch
            self.error_history.append(np.average(np.abs(self.error)))
            self.epoch_list.append(epoch)

    # function to predict output on new and unseen input data
    def predict(self, new_input):
        prediction = self.sigmoid(np.dot(new_input, self.weights))
        return prediction


def paint(event):
    python_green = "#476042"
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    w.create_oval(x1, y1, x2, y2, fill=python_green)


def clear_canvas():
    w.delete("all")


#converts list of RGB tuples from canvas image to the list of 0s and 1s
def convert_list_of_RGB_tuples_to_list_of_bits(param):
    new_list_of_bits = []
    for i in param:
        for j in i:
            if i[0] == 255:
                new_list_of_bits.append(0)
            elif i[0] == 0:
                new_list_of_bits.append(1)
            break
    return new_list_of_bits


#action triggered by the 'Recognize' button in main window
def recognize():
    ps_from_canvas = w.postscript(colormode="mono")
    image = Image.open(io.BytesIO(ps_from_canvas.encode('utf-8')))
    list_of_RGB_tuples_from_image = list(image.getdata()) #each tuple represents one pixel
    image_to_predict = convert_list_of_RGB_tuples_to_list_of_bits(list_of_RGB_tuples_from_image)
    inputs = inputs_from_dataset()
    outputs = outputs_from_dataset()
    # create neural network
    NN = NeuralNetwork(inputs, outputs)
    # train neural network
    NN.train()
    print(NN.predict(image_to_predict), ' - Correct: ', image_to_predict[0][0])


def inputs_from_dataset():
    with open("dataset.csv", "r", newline='\n') as f:
        dataset = list(csv.reader(f))
        dataset = np.array(dataset)
        inputs = dataset[:, :-1]
        return inputs


def outputs_from_dataset():
    with open("dataset.csv", "r", newline='\n') as f:
        dataset = list(csv.reader(f))
        dataset = np.array(dataset)
        outputs = dataset[:, -1]
        return outputs


#learning mode window
def learning_mode():
    def canvas_to_list_of_RGB_tuples(canvas):
        ps_from_canvas = canvas.postscript(colormode="mono")
        image = Image.open(io.BytesIO(ps_from_canvas.encode('utf-8')))
        list_of_RGB_tuples_from_image = list(image.getdata())  # each tuple represents one pixel
        return list_of_RGB_tuples_from_image

    def paint(event):
        python_green = "#476042"
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        w.create_oval(x1, y1, x2, y2, fill=python_green)

    def clear_canvas():
        w.delete("all")

    #action triggered by the 'Learn' button in the learning window
    def learn():
        list_of_RGB_tuples = canvas_to_list_of_RGB_tuples(w)
        list_of_bits = convert_list_of_RGB_tuples_to_list_of_bits(list_of_RGB_tuples)
        list_with_character = add_character_to_list_of_bits(list_of_bits, radio_variable)
        save_pattern(list_with_character)
        clear_canvas()

    #appends the list of 0s and 1s with the chosen character
    def add_character_to_list_of_bits(list_of_bits, character):
        character = radio_variable.get()
        if character == 0: #A
            list_of_bits.append(2)
        elif character == 1: #B
            list_of_bits.append(3)
        elif character == 2: #C
            list_of_bits.append(4)
        return list_of_bits

    #appends the dataset.csv file with the list of 0s and 1s with the appended character
    def save_pattern(list_of_bits):
        try:
            with open("dataset.csv", "a+") as f:
                wr = csv.writer(f)
                wr.writerow(list_of_bits)
        except FileNotFoundError:
            print("File not accessible")

    #test method for reading from the csv file and displaying in the console
    def read_from_csv():
        with open("dataset.csv", "r", newline='\n') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)

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

    #test
    read_button = Button(learning_window, text="Read", command=read_from_csv)
    read_button.pack(side=BOTTOM, pady=5, ipady=5, ipadx=22)

    learn_button = Button(learning_window, text="Learn", command=learn)
    learn_button.pack(side=BOTTOM, pady=5, ipady=5, ipadx=22)

    radio_variable = IntVar()
    radio_variable.set(0)
    Radiobutton(learning_window, text="A", variable=radio_variable, value=0).pack()
    Radiobutton(learning_window, text="B", variable=radio_variable, value=1).pack()
    Radiobutton(learning_window, text="C", variable=radio_variable, value=2).pack()

    message = Label(learning_window, text="Choose the character, draw and click Learn")
    message.pack(side=BOTTOM, pady=10)

    mainloop()


#recognition mode windows
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