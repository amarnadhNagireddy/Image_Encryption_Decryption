# encryption.py
import numpy as np
from PIL import Image
import io
def manipulate_image(image_path):
    # Open the image and convert to a NumPy array
    image = Image.open(image_path)
    image_array = np.array(image)

    height, width, channels = image_array.shape
    reverse_group_size = 5
    swap_group_size = 10

    # Step 1: Reverse groups of 5 columns alternately
    for start_col in range(0, width, reverse_group_size):
        end_col = min(start_col + reverse_group_size, width)
        group_index = start_col // reverse_group_size
        if group_index % 2 == 0:
            image_array[:, start_col:end_col] = image_array[:, start_col:end_col][:, ::-1]

    # Step 2: Reverse groups of 5 rows alternately
    for start_row in range(0, height, reverse_group_size):
        end_row = min(start_row + reverse_group_size, height)
        group_index = start_row // reverse_group_size
        if group_index % 2 == 0:
            image_array[start_row:end_row, :] = image_array[start_row:end_row, :][::-1, :]

    # Step 3: Swap groups of 10 columns alternately
    for start_col in range(0, width, swap_group_size * 2):
        odd_start = start_col
        even_start = start_col + swap_group_size

        if even_start + swap_group_size <= width:
            temp = image_array[:, odd_start:odd_start + swap_group_size].copy()
            image_array[:, odd_start:odd_start + swap_group_size] = image_array[:, even_start:even_start + swap_group_size]
            image_array[:, even_start:even_start + swap_group_size] = temp

    # Step 4: Swap groups of 10 rows alternately
    for start_row in range(0, height, swap_group_size * 2):
        odd_start = start_row
        even_start = start_row + swap_group_size

        if even_start + swap_group_size <= height:
            temp = image_array[odd_start:odd_start + swap_group_size, :].copy()
            image_array[odd_start:odd_start + swap_group_size, :] = image_array[even_start:even_start + swap_group_size, :]
            image_array[even_start:even_start + swap_group_size, :] = temp

    white_pixel = np.array([255, 255, 255])
    modified_array = white_pixel - image_array
    encrypted_array =  np.clip(modified_array, 0, 255).astype(np.uint8)

    encrypted_image = Image.fromarray(encrypted_array)
    encrypted_image_io = io.BytesIO()
    encrypted_image.save(encrypted_image_io, 'PNG')
    encrypted_image_io.seek(0)

    return encrypted_image_io

