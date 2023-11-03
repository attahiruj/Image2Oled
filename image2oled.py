# Import the OpenCV library
import cv2 as cv

# Load the image from the file 'heart.png'
image = cv.imread('images/heart.png')

# Check if the image was loaded successfully
if image is not None:
    # Optional: Resize the image to the desired dimensions
    resize_width = 32  # Adjust this value as needed
    resize_height = 32  # Adjust this value as needed
    image = cv.resize(image, (resize_width, resize_height))

    # Convert RGBA image to grayscale
    bw_image = cv.cvtColor(image, cv.COLOR_RGBA2GRAY)

    # Check if the image should be inverted
    invert_image = True  # Set to True to invert the image
    if invert_image:
        bw_image = cv.bitwise_not(bw_image)  # Invert the image
        
    # Threshold the grayscale image to create a binary image
    thresh_value = 128
    _, thresh_image = cv.threshold(bw_image, thresh_value, 255, cv.THRESH_BINARY)

    # Get the size (width and height) of the thresholded image as an array
    size_array = thresh_image.shape

    # Extract the width and height from the size array
    width = size_array[1]
    height = size_array[0]

    # Define the output file path for the binary data
    file_path = 'output.txt'
    with open(file_path, 'w') as file:
        # Write data to the file in a format suitable for embedded systems
        file.write('const unsigned char frames[] = {\n')  # Assuming 8 bits (1 byte) per row
        for i in range(height):  # Loop over rows (height)
            file.write('    0b')  # Add '0b' before the first binary digit
            for j in range(width):  # Loop over columns (width)
                pixel_value = int(thresh_image[i, j])  # Get the pixel value as an integer
                if pixel_value > thresh_value:
                    file.write('1')  # Write '1' for white (above threshold)
                elif pixel_value < thresh_value:
                    file.write('0')  # Write '0' for black (below threshold)
                
                if (j + 1) % 8 == 0 and j != width - 1:
                    file.write(', 0b')  # Add a comma and '0b' for the next byte

            if i != height - 1:
                file.write(',\n')  # Add a comma and newline for the next row
            else:
                file.write('\n};\n')  # Close the array declaration

    # Display the thresholded image using cv.imshow
    cv.imshow('Thresholded Image', thresh_image)

    # Wait for a key press and then close the window
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print("Image not found or could not be loaded.")
