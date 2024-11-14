# Image Processing Application

An image processing and thresholding application written in both Java and Python. I have implemented various features such as noise addition, multiple filtering techniques, thresholding methods, and histogram visualization. It allows users to load images, apply processing operations, visualize the results in real time, and save the processed image.

## Table of Contents

- [Features](#features)
  - [Image Filtering Operations](#image-filtering-operations)
  - [Thresholding Operations](#thresholding-operations)
  - [Other Features](#other-features)
  - [Visualization](#visualization)
- [Python Application Details](#python-application)
- [Java Application Details](#java-application)
- [Required Libraries](#Required-Libraries)

## Features

### Image Filtering Operations

- **Noise Addition**: Adds random black and white pixels to the image to simulate noise.
- **Triangle Filtering**: Applies a 5x5 triangle filter for smoothing.
- **Gaussian Filtering**: Applies a 5x5 Gaussian filter with adjustable sigma for custom smoothing effects.
- **Median Filtering**: Applies a 5x5 median filter to reduce noise while preserving edges.
- **Kuwahara Filtering**: Applies a 5x5 Kuwahara filter for edge-preserving smoothing.

### Thresholding Operations

- **Manual Thresholding**: Allows the user to input a threshold value for binary thresholding.
- **Automatic Thresholding**: Uses the mean value of each color channel as the threshold.
- **Otsu’s Thresholding**: Applies Otsu’s method for automatic threshold selection.
- **Adaptive Thresholding**: Uses adaptive mean thresholding with a user-defined offset value.

### Other Features

- **Add Button**: Allows users to add an image from storage using GUI.
- **Save Button**: Saves the latest processed version of the image.

### Visualization

- **Image Display**: Shows the processed or thresholded image in real-time.
- **Histogram Display**: Visualizes the histogram of each color channel (blue, green, red), with optional threshold lines, aiding in image intensity distribution analysis.

---

## Python Application

### Overview
The Python application was built as part of COMP3301 course at MUN, with Tkinter for the GUI, utilizing OpenCV, Numpy, and Matplotlib for image processing and visualization.

### Key Libraries and Modules
- **Tkinter** for GUI elements and user interactivity.
- **OpenCV** (`cv2`) for image loading, filtering, and processing.
- **Matplotlib** for real-time histogram visualization.
### Python-Specific Features
- Interactive GUI with buttons to load images, save images, add noise, apply various filters, and perform thresholding.
- Real-time histogram updates using `FigureCanvasTkAgg` for seamless integration with Tkinter.

## Java Application

### Overview
The Java application was built for fun and to gain skills with Swing for the GUI and OpenCV for Java for image processing. It is simply a clone of the Python application.
### Java-Specific Features
- GUI implemented with Swing, including buttons for loading and saving images, adding noise, applying filters, and performing thresholding.
- Real-time display of processed images after each operation.
- Comprehensive OpenCV-based image processing, including thresholding and noise addition directly within Java.

## Required Libraries

- **Python Libraries**: `cv2`, `numpy`, `tkinter`, `matplotlib`
- **Java Libraries**: OpenCV for Java
