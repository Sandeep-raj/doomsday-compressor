import cv2
import numpy as np


def check_end_byte(input_byte_array, end_index):

    end_byte = input_byte_array[end_index-8:end_index+1]
    print("here", end_index, end_byte,
          input_byte_array[len(input_byte_array) - 1])
    return True
    if end_byte == b'===END===':
        print("here", True)
        return True
    return False


def trim_empty_end(input_byte_array):
    for i in range(len(input_byte_array) - 1, -1, -1):
        if input_byte_array[i] > 1 and check_end_byte(input_byte_array, i):
            return input_byte_array[0: i - 8]
    return input_byte_array[0:0]


# Replace 'input_video.mp4' with the path to your MP4 video file
input_video_path = './output_video.mp4'

# Open the video file for reading
cap = cv2.VideoCapture(input_video_path)

# Initialize a list to store video frames as byte arrays
frames_byte_arrays = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to a byte array
    frame_bytes = frame.tobytes()
    frames_byte_arrays.append(frame_bytes)

# Release the video capture object
cap.release()

# Convert the list of byte arrays into a single byte array
complete_byte_array = b''.join(frames_byte_arrays)

# Now, 'complete_byte_array' contains the byte data of the entire video
complete_byte_array = trim_empty_end(complete_byte_array)
print(len(complete_byte_array))
