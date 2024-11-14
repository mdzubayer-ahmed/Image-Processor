import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import os

# User input for the image path
image_path = input("Enter the path to the image file with the extension (baboon.jpg/fingerprint.png): ").strip()

# Load the image
if not os.path.exists(image_path):
    raise FileNotFoundError(f"File not found: {image_path}")
image = plt.imread(image_path)

def is_grayscale(img):
    """Check whether the input image is in grayscale."""
    return len(img.shape) == 2 or img.shape[2] == 1

def rgb_to_gray(image):
    """Convert an RGB image to a grayscale image for filtering operations."""
    if is_grayscale(image):
        return image
    return np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])

# If the image is grayscale, keep it as is, but if it's RGB, convert it to grayscale
original_image = rgb_to_gray(image) if is_grayscale(image) else image
current_image = original_image.copy()

def add_noise(image):
    """Randomly add black and white noise throughout the image."""
    noisy_image = np.copy(image)
    prob = 0.05
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            r = np.random.rand()
            if r < prob / 2:
                noisy_image[i, j] = 0
            elif r < prob:
                noisy_image[i, j] = 1
    return noisy_image

def triangle_filter(image):
    """Applying a 5x5 triangle filter using S(tri)^5 kernel from the slides."""
    kernel = np.array([
        [1, 2, 3, 2, 1],
        [2, 4, 6, 4, 2],
        [3, 6, 9, 6, 3],
        [2, 4, 6, 4, 2],
        [1, 2, 3, 2, 1]
    ]) / 81

    if image.ndim == 3:
        filtered_image = np.zeros_like(image)
        for c in range(3):
            filtered_image[..., c] = convolve(image[..., c], kernel)
        return filtered_image
    else:
        return convolve(image, kernel)

def gaussian_filter(image, sigma):
    """Applying a 5x5 triangle filter using Gaussian function."""
    size = 5
    kernel = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            x0 = x - size // 2
            y0 = y - size // 2
            kernel[x, y] = (1 / (2 * np.pi * sigma**2)) * np.exp(-(x0**2 + y0**2) / (2 * sigma**2))
    kernel /= np.sum(kernel)

    if image.ndim == 3:
        filtered_image = np.zeros_like(image)
        for c in range(3):
            filtered_image[..., c] = convolve(image[..., c], kernel)
        return filtered_image
    else:
        return convolve(image, kernel)


def median_filter(image, size=5):
    """Applying a median filter."""
    if image.ndim == 3:  # RGB
        pad_image = np.pad(image, ((size // 2, size // 2), (size // 2, size // 2), (0, 0)), mode='edge')
        output = np.zeros_like(image)
        for c in range(image.shape[2]):
            for y in range(image.shape[0]):
                for x in range(image.shape[1]):
                    neighborhood = pad_image[y:y + size, x:x + size, c]
                    output[y, x, c] = np.median(neighborhood)
    else:  # Grayscale
        pad_image = np.pad(image, ((size // 2, size // 2), (size // 2, size // 2)), mode='edge')
        output = np.zeros_like(image)
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                neighborhood = pad_image[y:y + size, x:x + size]
                output[y, x] = np.median(neighborhood)

    return output

def kuwahara_filter(image):
    """Applying a 5x5 Kuwahara filter"""
    if image.ndim == 3:
        output = np.zeros_like(image)
        h, w = image.shape[:2]
        for y in range(2, h-2):
            for x in range(2, w-2):
                regions = []
                for i in range(2):
                    for j in range(2):
                        region = image[y-2+i*2:y+1+i*2, x-2+j*2:x+1+j*2]
                        regions.append((np.mean(region, axis=(0, 1)), np.var(region, axis=(0, 1))))
                mean, _ = min(regions, key=lambda r: np.sum(r[1]))
                output[y, x] = mean
        return output
    else:
        output = np.zeros_like(image)
        h, w = image.shape
        for y in range(2, h-2):
            for x in range(2, w-2):
                region = image[y-2:y+3, x-2:x+3]
                output[y, x] = np.mean(region)
        return output

def convolve(image, kernel):
    """Manually apply convolution with a given kernel."""
    output = np.zeros_like(image)
    pad_image = np.pad(image, 2, mode='edge')
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            output[y, x] = np.sum(pad_image[y:y+5, x:x+5] * kernel)
    return output

def update_image(img):
    """Update the display with a new image."""
    global current_image
    axis.clear()
    if is_grayscale(img):
        axis.imshow(img, cmap='gray')
    else:
        axis.imshow(img)
    current_image = img
    plt.draw()

# Clicking on buttons
def add_noise_click(event):
    noisy_image = add_noise(original_image)
    update_image(noisy_image)

def triangle_click(event):
    triangle_filtered = triangle_filter(original_image)
    update_image(triangle_filtered)

def gaussian_click(event):
    gaussian_filtered = gaussian_filter(original_image, sigma=1.0)
    update_image(gaussian_filtered)

def median_click(event):
    median_filtered = median_filter(original_image)
    update_image(median_filtered)

def kuwahara_click(event):
    kuwahara_filtered = kuwahara_filter(original_image)
    update_image(kuwahara_filtered)

def save_click(event):
    output = input("Enter the filename to save with the extension (output.png): ").strip()
    try:
        plt.imsave(output, current_image)
        print(f'Image saved as {output}')
    except Exception as e:
        print(f'Couldn\'t save the image. Please check the extension (abc.png): {e}')

# Display images
figure, axis = plt.subplots()
plt.subplots_adjust(bottom=0.2)
axis.imshow(original_image)

# Display interactive buttons
axis_add_noise_button = plt.axes([0.1, 0.05, 0.2, 0.075])
button_add_noise = Button(axis_add_noise_button, 'Add Noise')
button_add_noise.on_clicked(add_noise_click)

axis_triangle_filter_button = plt.axes([0.35, 0.05, 0.2, 0.075])
button_triangle_filter = Button(axis_triangle_filter_button, 'Triangle Filter')
button_triangle_filter.on_clicked(triangle_click)

axis_gaussian_filter_button = plt.axes([0.6, 0.05, 0.2, 0.075])
button_gaussian_filter = Button(axis_gaussian_filter_button, 'Gaussian Filter')
button_gaussian_filter.on_clicked(gaussian_click)

axis_median_filter_button = plt.axes([0.1, 0.15, 0.2, 0.075])
button_median_filter = Button(axis_median_filter_button, 'Median Filter')
button_median_filter.on_clicked(median_click)

axis_kuwahara_filter_button = plt.axes([0.35, 0.15, 0.2, 0.075])
button_kuwahara_filter = Button(axis_kuwahara_filter_button, 'Kuwahara Filter')
button_kuwahara_filter.on_clicked(kuwahara_click)

axis_save_image_button = plt.axes([0.6, 0.15, 0.2, 0.075])
button_save_image = Button(axis_save_image_button, 'Save Image')
button_save_image.on_clicked(save_click)

# Plot
plt.show()
