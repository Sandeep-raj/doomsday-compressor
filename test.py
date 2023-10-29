import cv2
import numpy as np

END_BYTES = b'===END==='

# Define the path for the output video file
output_video_path = './output_video.mp4'
# Set the frame dimensions (width and height)
frame_width = 640  # Adjust to your frame dimensions
frame_height = 480
fps = 30  # Adjust as needed


def read_file(file_path, chunk_size=4096):
    byte_array = bytearray()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            byte_array.extend(chunk)

    return byte_array


def pad_byte_array(input_byte_array, target_multiple):
    current_length = len(input_byte_array)
    remainder = current_length % target_multiple
    if remainder != 0:
        # Calculate the number of zeroes to add
        padding_length = target_multiple - remainder
        # Create a zero byte array of the required length
        padding = bytes([0] * padding_length)
        # Concatenate the padding to the input byte array
        padded_byte_array = input_byte_array + padding
    else:
        # The input byte array length is already a multiple of target_multiple
        padded_byte_array = input_byte_array
    return padded_byte_array


# Suppose you have a large byte array containing image data
# Replace this with your actual byte array
large_byte_array = read_file("./test.zip")

large_byte_array = large_byte_array + END_BYTES

large_byte_array = pad_byte_array(large_byte_array, 480*640*3)

# Convert the byte array to a NumPy array
image_data = np.frombuffer(large_byte_array, dtype=np.uint8)

# Reshape the NumPy array to the desired image dimensions (e.g., 3 channels, 640x480)
image_shape = (480, 640, 3)  # Modify the dimensions to match your image size
images = image_data.reshape(-1, *image_shape)


# Define the codec and frames per second (fps) for the video
# You can also use other codecs like 'XVID'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# Create a VideoWriter object
out = cv2.VideoWriter(output_video_path, fourcc, fps,
                      (frame_width, frame_height))

# Now, 'images' is a NumPy array of multiple images
# You can iterate over them or access individual images
for i, image in enumerate(images):
    # Convert the NumPy array to an OpenCV Mat-like object (if needed)
    # Use cv2.Mat or cv2.UMat based on your requirements
    # image_mat = cv2.UMat(image)
    # Process or save the image as needed
    # cv2.imwrite(f'./imgs/image_{i}.jpg', image_mat)

    # Write the frame to the video
    out.write(image)

# Release the VideoWriter when you're done
out.release()

# Clean up
cv2.destroyAllWindows()
