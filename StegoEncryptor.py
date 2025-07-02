# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 11:15:04 2025

Updated: Wraps through all image rows/columns to hide full message in blue channel.
"""
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

def string_to_binary(input_string):
    """Converts a string to its binary representation (no spaces)."""
    return ''.join(format(ord(c), '08b') for c in input_string)

def int_to_binary(inp):
    binary_result = ''
    if inp == 0:
        binary_result = '0'
    else:
        while inp > 0:
            binary_result = str(inp % 2) + binary_result
            inp //= 2
    return binary_result.zfill(8)  # Make sure it's 8 bits

def binary_to_int(binary_input):
    return int(binary_input, 2)

# === INPUT ===
print("Input image file path:")
while True:
    image_path = input().strip()
    if os.path.exists(image_path):
        break
    print("File does not exist. Try again:")

img = Image.open(image_path).convert('RGB')
img_array = np.array(img)

print("What is the message you want to put in the image?")
message = input() + '\x00'  # Add null terminator
messageB = string_to_binary(message)

height, width, _ = img_array.shape
total_pixels = height * width

if len(messageB) > total_pixels:
    print("Image too small to hold the entire message.")
else:
    bit_index = 0
    for row in range(height):
        for col in range(width):
            if bit_index >= len(messageB):
                break  # Done hiding message
            blue_val = img_array[row, col, 2]
            blue_bin = int_to_binary(blue_val)
            blue_bin_list = list(blue_bin)
            blue_bin_list[-1] = messageB[bit_index]  # Replace LSB
            new_blue = binary_to_int(''.join(blue_bin_list))
            img_array[row, col, 2] = new_blue
            bit_index += 1
        if bit_index >= len(messageB):
            break

# === OUTPUT ===
output_image = Image.fromarray(img_array, mode='RGB')
output_image.save("hiddenMessageimage.png")
plt.imshow(output_image)
plt.axis('off')
plt.show()
