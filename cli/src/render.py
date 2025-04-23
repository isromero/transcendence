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
                if image.array[i][j] != ' ':
                    canvas[canvas_x][canvas_y] = image.array[i][j]

# Main execution block
def render(ball_x, ball_y, padle1_y, padle2_y, score_l, score_r, timer, side):

    game_height = 400
    game_width = 800
    canvas_height = 54
    canvas_width = 171
    canvas = [[' ' for _ in range(canvas_width)] for _ in range(canvas_height)]
    if timer is not None:
        timer = int(timer)
    else:
        timer = 0 

    sky = AsciiImage('src/field.txt')
    ball = AsciiImage('src/ball.txt')
    padle = AsciiImage('src/padle.txt')
    countdown = AsciiImage('src/countdown.txt')
    left_score = AsciiImage(f'src/numbers/{score_l}.txt')
    right_score = AsciiImage(f'src/numbers/{score_r}.txt')

    place_image_on_canvas(canvas, sky, 0, 0)
    if side == "right":
        padle = AsciiImage('src/padle_fill.txt')
    place_image_on_canvas(canvas, padle, int((padle1_y * canvas_height) / game_height), 6) 
    if side == "left":
        padle = AsciiImage('src/padle_fill.txt')
    place_image_on_canvas(canvas, padle, int((padle2_y * canvas_height) / game_height), 174 - padle.rows) 
    # points 1
    place_image_on_canvas(canvas, left_score, 3, 70)
    place_image_on_canvas(canvas, right_score, 3, 171 - 75 - right_score.rows) 
    place_image_on_canvas(canvas, ball, int((ball_y * canvas_height) / game_height) - int(ball.cols / 4), int((ball_x * canvas_width) / game_width) - int(ball.rows / 1.2))
    if (timer):
        timer_txt = AsciiImage(f'src/numbers/{timer}.txt')
        place_image_on_canvas(canvas, countdown, (int(canvas_height / 2) - int(countdown.cols / 4.2)), (int(canvas_width / 2) - int(countdown.rows)))
        place_image_on_canvas(canvas, timer_txt, 24, 82)

    clear_console()
    print_canvas(canvas)

#render(0, 1, 150, 150, 4, 5, 6)
