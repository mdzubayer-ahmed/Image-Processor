# Image Processing Application

A comprehensive Python GUI application for image processing and thresholding, with features including noise addition, multiple filtering techniques, and thresholding methods. This tool allows users to load images, apply processing operations, and visualize the results with histograms.

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

### Other features
- **Add Button**: Allows user to add an image from storage using GUI
- **Save Button**: Saves the latest processed version of the image.

### Visualization

- **Image Display**: Shows the processed or thresholded image in real-time using `matplotlib` integrated within the Tkinter GUI.
- **Histogram Display**: Visualizes the histogram of each color channel (blue, green, red) with optional threshold lines, making it easier to analyze image intensity distributions.

### Interactive GUI

- Built with Tkinter, the application provides buttons for loading images, applying filters, and selecting thresholding methods.
- Real-time updates of images and histograms after each operation for immediate visualization.

## Requirements

- **Libraries**: `cv2`, `numpy`, `tkinter`, `matplotlib`
- **Backend**: Utilizes `FigureCanvasTkAgg` to integrate `matplotlib` figures with Tkinter, and `matplotlib.use('TkAgg')` for interactive image and histogram display.
