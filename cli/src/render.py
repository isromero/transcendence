import os

# Class to store the ASCII image and its corresponding 2D array
class AsciiImage:
    def __init__(self, filename):
        self.filename = filename
        self.array = self.read_file_to_array(filename)
        self.rows = len(self.array)
        # image.cols is defined as the max width among all rows
        self.cols = max(len(row) for row in self.array) if self.rows > 0 else 0

    def read_file_to_array(self, filename):
        array = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    # Convert each line into a list of characters (removing newline)
                    array.append(list(line.rstrip('\n')))
        except FileNotFoundError:
            print(f"File {filename} not found.")
        return array

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to print the canvas (2D array)
def print_canvas(canvas):
    for row in canvas:
        print(''.join(row))

# Function to place an image on the canvas at a given (x, y) position
# Only draws the characters that fall within the canvas boundaries.
def place_image_on_canvas(canvas, image, x, y):
    for i in range(image.rows):
        # Use the length of the current row so we don't go out of range
        for j in range(len(image.array[i])):
            canvas_x = x + i
            canvas_y = y + j
            if 0 <= canvas_x < len(canvas) and 0 <= canvas_y < len(canvas[0]):
                canvas[canvas_x][canvas_y] = image.array[i][j]

# Main execution block
if __name__ == "__main__":
    # Initialize the canvas of 54 (height) x 171 (width) filled with spaces
    canvas_height = 54
    canvas_width = 171
    canvas = [[' ' for _ in range(canvas_width)] for _ in range(canvas_height)]

    # Load images. Replace 'sky.txt' and 'ball.txt' with your actual ASCII art files.
    sky = AsciiImage('field.txt')   # Background, e.g., a sky
    ball = AsciiImage('ball.txt') # Foreground, e.g., a ball
    padle = AsciiImage('padle.txt') # Foreground, e.g., a ball

    # Place images onto the canvas:
    # First, place the sky at the top-left of the canvas.
    place_image_on_canvas(canvas, sky, 0, 0)
    # Then, place the ball so it overlaps the sky.
    place_image_on_canvas(canvas, ball, 5, 20)  # Adjust x,y coordinates as needed
    place_image_on_canvas(canvas, padle, 5, 20)  # Adjust x,y coordinates as needed

    # Clear the console and print the final composed canvas.
    clear_console()
    print_canvas(canvas)