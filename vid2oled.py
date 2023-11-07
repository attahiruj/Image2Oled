import cv2 as cv

max_width = 128
max_height = 64
buffer = max_width * max_height
# Input video file
video_file = 'videos/kite.mp4'

# Open the video file
cap = cv.VideoCapture(video_file)

# Check if the video file was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Output file for generated code
output_file = 'output/kite.txt'

# Initialize variables to store the generated code
code = ''
code += 'const unsigned char frames[][{}] = {{\n'.format(buffer)
# Process each frame in the video
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Threshold the frame
    thresh_value = 128
    _, thresh_frame = cv.threshold(gray_frame, thresh_value, 255, cv.THRESH_BINARY)

    # Get the size (width and height) of the frame
    height, width = thresh_frame.shape
    if width > max_width:
        width = max_width
    if height > max_height:
        height = max_height
    # Generate code for the current frame
    frame_code = '\n{\n'
    for i in range(height):  # Loop over rows (height)
        frame_code += '    0b'  # Add '0b' before the first binary digit
        for j in range(width):  # Loop over columns (width)
            pixel_value = int(thresh_frame[i, j])  # Get the pixel value as an integer
            if pixel_value > thresh_value:
                frame_code += '1'  # Write '1' for white (above threshold)
            elif pixel_value < thresh_value:
                frame_code += '0'  # Write '0' for black (below threshold)

            if (j + 1) % 8 == 0 and j != width - 1:
                frame_code += ', 0b'  # Add a comma and '0b' for the next byte

        if i != height - 1:
            frame_code += ',\n'  # Add a comma and newline for the next row
        else:
            frame_code += '\n},\n'  # Close the array declaration

    code += frame_code

    frame_count += 1

code += '};'
# Write the generated code to the output file
with open(output_file, 'w') as file:
    file.write(code)

# Release the video capture
cap.release()

print("Code generation complete. {} frames processed.".format(frame_count))
