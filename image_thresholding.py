import cv2
import numpy as np
import tkinter as tk # For interactive GUI window
from tkinter import filedialog, simpledialog #filedialog for opening files, and simpledialog for user input
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #for integrating matplotlib with tkinter window

img = None
image_figure = None
figure_histogram = None
def load_image(): #Loading image using opencv
    global img
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        display_image(img)
        display_histogram(img)
def display_image(image): #displaying image
    global image_figure
    image_figure.clf()
    axes = image_figure.add_subplot(111)
    axes.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axes.axis('off')
    image_figure.canvas.draw()
def display_histogram(image, threshold_values=None): #calculating and visualizing image histogram
    global figure_histogram
    figure_histogram.clf()
    color = ('b', 'g', 'r')
    axes = figure_histogram.add_subplot(111)
    for i, col in enumerate(color):
        histogram = cv2.calcHist([image], [i], None, [256], [0, 256])
        axes.plot(histogram, color=col)
        if threshold_values and threshold_values[i] is not None:
            axes.axvline(threshold_values[i], color=col, linestyle='--')
    figure_histogram.canvas.draw()
def manual_threshold(): #Manual threshold with user specified threshold value
    global img
    if img is not None:
        threshold = simpledialog.askinteger("Manual Threshold", "Enter threshold value:", minvalue=0, maxvalue=255)
        channels = cv2.split(img)
        threshold_values = [threshold] * 3
        thresholded_channels = [cv2.threshold(ch, threshold, 255, cv2.THRESH_BINARY)[1] for ch in channels]
        thresholded_image = cv2.merge(thresholded_channels)
        display_image(thresholded_image)
        display_histogram(img, threshold_values)
def automatic_threshold(): #Automatic thresholding with the mean value of the color channel
    global img
    if img is not None:
        channels = cv2.split(img)
        threshold_values = [int(np.mean(ch)) for ch in channels]
        thresholded_channels = [cv2.threshold(ch, t, 255, cv2.THRESH_BINARY)[1] for ch, t in zip(channels, threshold_values)]
        thresholded_image = cv2.merge(thresholded_channels)
        display_image(thresholded_image)
        display_histogram(img, threshold_values)
def otsu_threshold(): #Thresholding using Otsu's method
    global img
    if img is not None:
        channels = cv2.split(img)
        threshold_values = [cv2.threshold(ch, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[0] for ch in channels]
        thresholded_channels = [cv2.threshold(ch, t, 255, cv2.THRESH_BINARY)[1] for ch, t in zip(channels, threshold_values)]
        thresholded_image = cv2.merge(thresholded_channels)
        display_image(thresholded_image)
        display_histogram(img, threshold_values)
def adaptive_threshold(): #Adaptive thresholding using user specific offset value
    global img
    if img is not None:
        offset = simpledialog.askinteger("Adaptive Threshold", "Enter offset value:", minvalue=0, maxvalue=100)
        channels = cv2.split(img)
        thresholded_channels = [cv2.adaptiveThreshold(ch, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, offset) for ch in channels]
        thresholded_image = cv2.merge(thresholded_channels)
        display_image(thresholded_image)
        display_histogram(img)

root = tk.Tk()
root.title("Assignment 3: Image Thresholding")
root.geometry("1000x500")
load_button = tk.Button(root, text="Insert image", command=load_image)
load_button.pack()
frame = tk.Frame(root)
frame.pack()
manual_button = tk.Button(frame, text="Manual Threshold", command=manual_threshold)
manual_button.grid(row=0, column=0, padx=5, pady=5)
automatic_button = tk.Button(frame, text="Automatic Threshold", command=automatic_threshold)
automatic_button.grid(row=0, column=1, padx=5, pady=5)
otsu_button = tk.Button(frame, text="Otsu's Method", command=otsu_threshold)
otsu_button.grid(row=0, column=2, padx=5, pady=5)
adaptive_button = tk.Button(frame, text="Adaptive Threshold", command=adaptive_threshold)
adaptive_button.grid(row=0, column=3, padx=5, pady=5)
image_figure = Figure(figsize=(5, 4), dpi=100)
figure_histogram = Figure(figsize=(5, 4), dpi=100)
canvas_image = FigureCanvasTkAgg(image_figure, master=root)
canvas_image.get_tk_widget().pack(side=tk.LEFT)
canvas_histogram = FigureCanvasTkAgg(figure_histogram, master=root)
canvas_histogram.get_tk_widget().pack(side=tk.RIGHT)
root.mainloop()
