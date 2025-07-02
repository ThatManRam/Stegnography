from PIL import Image
import numpy as np

def int_to_binary(inp):
    """Converts an integer to an 8-bit binary string."""
    return format(inp, '08b')

def binary_to_string_no_spaces(binary_input):
    """Converts binary string (no spaces) into a regular text string."""
    characters = [
        chr(int(binary_input[i:i+8], 2)) 
        for i in range(0, len(binary_input), 8)
    ]
    return ''.join(characters)

def extract_message_until_null(img_array):
    """
    Extracts LSBs from blue channel of the entire image until a null byte (\x00) is found.
    """
    recovered_bits = []
    height, width, _ = img_array.shape

    for row in range(height):
        for col in range(width):
            blue = img_array[row, col, 2]
            binary = int_to_binary(blue)
            recovered_bits.append(binary[-1])  # LSB of blue channel

            # Check for null terminator every 8 bits
            if len(recovered_bits) % 8 == 0:
                last_char_bits = recovered_bits[-8:]
                char = chr(int(''.join(last_char_bits), 2))
                if char == '\x00':
                    binary_message = ''.join(recovered_bits[:-8])  # Exclude null byte
                    return binary_to_string_no_spaces(binary_message)
    
    # In case null byte is never found
    return "[ERROR: Null terminator not found]"

# === Main ===
image_path = "hiddenMessageimage.png"
img = Image.open(image_path).convert("RGB")
img_array = np.array(img)

recovered_message = extract_message_until_null(img_array)
print("Recovered message:", recovered_message)
