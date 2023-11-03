import cv2 as cv

# Input video file
video_file = 'output/circles_r.mp4'

# Open the video file
cap = cv.VideoCapture(video_file)

# Check if the video file was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Output file for generated code
output_file = 'output/vid.txt'

max_width = 128
max_height = 64

# Get the width and height of the video
width = int(cap.get(3))  # Width
height = int(cap.get(4))  # Height

if  width > max_width:
    width = max_width 
if  height > max_height:
    height = max_height 
    
buffer = width*height

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
    thresh_value = 86
    _, thresh_frame = cv.threshold(gray_frame, thresh_value, 255, cv.THRESH_BINARY)

    # Generate code for the current frame
    frame_code = '\n{\n'
    for i in range(height):
        for j in range(width):
            pixel_value = int(thresh_frame[i, j])
            frame_code += '\t' + str(pixel_value)
            if j != width - 1:
                frame_code += ','
            # else:
            #     frame_code += '}'
        if i != height - 1:
            frame_code += ',\n'
        else:
            frame_code += '\n},\n'

    code += frame_code

    frame_count += 1
    
code += '};'
# Write the generated code to the output file
with open(output_file, 'w') as file:
    file.write(code)

# Release the video capture
cap.release()

print("Code generation complete. {} frames processed.".format(frame_count))
