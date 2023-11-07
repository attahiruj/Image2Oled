import cv2

# Input video file
video_file = 'videos/pen.mp4'  # Replace with your video file path

# Output video file
output_video_file = 'videos/pen_r.mp4'

# Specify the new dimensions for resizing
new_width = 128 
new_height = 64  

# Open the video file
cap = cv2.VideoCapture(video_file)

# Get the original video's frame width, height, and frames per second
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = cap.get(5)

# Define a codec and create a VideoWriter object to save the resized video
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Adjust the codec as needed
out = cv2.VideoWriter(output_video_file, fourcc, fps, (new_width, new_height))

# Check if the video file was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Process each frame in the video
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Break the loop when all frames have been processed

    # Resize the frame to the new dimensions
    resized_frame = cv2.resize(frame, (new_width, new_height))

    # Write the resized frame to the output video
    out.write(resized_frame)

# Release the video capture and writer
cap.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
