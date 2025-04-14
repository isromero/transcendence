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
                if image.array[i][j] is not ' ':
                    canvas[canvas_x][canvas_y] = image.array[i][j]

# Main execution block
def render(ball_x, ball_y, padle1_y, padle2_y, score_l, score_r, timer):

    game_height = 400
    game_width = 800
    canvas_height = 54
    canvas_width = 171
    canvas = [[' ' for _ in range(canvas_width)] for _ in range(canvas_height)]

    sky = AsciiImage('src/field.txt')   # Background, e.g., a sky
    ball = AsciiImage('src/ball.txt') # Foreground, e.g., a ball
    padle = AsciiImage('src/padle.txt') # Foreground, e.g., a ball
    left_score = AsciiImage(f'src/numbers/{score_l}.txt') # Foreground, e.g., a ball
    right_score = AsciiImage(f'src/numbers/{score_r}.txt') # Foreground, e.g., a ball

    place_image_on_canvas(canvas, sky, 0, 0)
    place_image_on_canvas(canvas, padle, 5, 6)  # Adjust x,y coordinates as needed
    place_image_on_canvas(canvas, padle, 5, 171 - 6 - padle.rows) 
    # points 1
    place_image_on_canvas(canvas, left_score, 3, 70)  # Adjust x,y coordinates as needed
    place_image_on_canvas(canvas, right_score, 3, 171 - 70 - right_score.rows)  # Adjust x,y coordinates as needed
    place_image_on_canvas(canvas, ball, int((ball_y * canvas_height) / game_height) - int(ball.cols / 4), int((ball_x * canvas_width) / game_width) - int(ball.rows / 1.2))

    clear_console()
    print_canvas(canvas)

render(0, 1, 150, 150, 4, 5, 6)
