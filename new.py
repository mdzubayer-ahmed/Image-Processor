import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive plots

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import os

def load_image(image_path):
    return plt.imread(image_path)

image_path = input("Enter the path to the image file: ").strip()

if not os.path.exists(image_path):
    raise FileNotFoundError(f"File not found: {image_path}")
image = load_image(image_path)  # Load the selected image

def is_grayscale(img):
    return len(img.shape) == 2 or img.shape[2] == 1

def rgb_to_gray(image):
    return np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])

original_image = rgb_to_gray(image) if is_grayscale(image) else image
current_image = original_image.copy()

def add_noise(image):
    """Manually add salt and pepper noise to the image."""
    noisy_image = np.copy(image)
    prob = 0.05
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            r = np.random.rand()
            if r < prob / 2:
                noisy_image[i, j] = 0  # Salt noise (black)
            elif r < prob:
                noisy_image[i, j] = 1  # Pepper noise (white)
    return noisy_image

def apply_triangle_filter(image):
    kernel = np.array([
        [1, 2, 3, 2, 1],
        [2, 4, 6, 4, 2],
        [3, 6, 9, 6, 3],
        [2, 4, 6, 4, 2],
        [1, 2, 3, 2, 1]
    ]) / 81

    return convolve_image(image, kernel)

def convolve_image(image, kernel):
    """Manually apply convolution with a given kernel."""
    output = np.zeros_like(image)
    pad_image = np.pad(image, 2, mode='edge')
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            output[y, x] = np.sum(pad_image[y:y+5, x:x+5] * kernel)
    return output

def apply_filter(image, filter_func, *args):
    if image.ndim == 3:
        filtered_image = np.zeros_like(image)
        for c in range(image.shape[2]):  # For each color channel
            filtered_image[..., c] = filter_func(image[..., c], *args)
        return filtered_image
    else:
        return filter_func(image, *args)

def on_add_noise(event):
    noisy_image = add_noise(original_image)
    update_image(noisy_image)

def on_triangle(event):
    triangle_filtered = apply_filter(original_image, apply_triangle_filter)
    update_image(triangle_filtered)

def on_save(event):
    output_filename = input("Enter the filename to save (e.g., output.png): ").strip()
    try:
        if current_image.ndim == 3:
            plt.imsave(output_filename, current_image)
        else:
            plt.imsave(output_filename, current_image, cmap='gray')
        print(f'Saved image as {output_filename}')
    except Exception as e:
        print(f'Error saving image: {e}')

# Create the plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

# Display the original image
ax.imshow(original_image)

# Add buttons for operations
ax_add_noise = plt.axes([0.1, 0.05, 0.2, 0.075])
btn_add_noise = Button(ax_add_noise, 'Add Noise')
btn_add_noise.on_clicked(on_add_noise)

ax_triangle = plt.axes([0.35, 0.05, 0.2, 0.075])
btn_triangle = Button(ax_triangle, 'Triangle Filter')
btn_triangle.on_clicked(on_triangle)

ax_save = plt.axes([0.6, 0.15, 0.2, 0.075])
btn_save = Button(ax_save, 'Save Image')
btn_save.on_clicked(on_save)

# Show the plot
plt.show()
