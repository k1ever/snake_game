import os
import random
import curses

# Initialize the screen
s = curses.initscr()
# Set the cursor state. 0 means invisible.
curses.curs_set(0)

# Get the terminal size
sh, sw = s.getmaxyx()

# Create a new window using screen height and width
w = curses.newwin(sh, sw, 0, 0)
# Draw a border around the window
w.box()
# Accept keypad input
w.keypad(1)
# Set the screen refresh rate
w.timeout(100)

# Set initial snake position
snk_x = sw//4
snk_y = sh//2
# Create the snake body parts
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

# Set initial food position
food = [sh//2, sw//2]
# Add the food to the screen
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)

# Initialize the snake direction to right
key = curses.KEY_RIGHT

# Initialize score
score = 0

# Start the game loop
while True:
    # Display score
    s.addstr(0, 0, 'Score: ' + str(score))

    # Get the next key
    next_key = w.getch()
    # If no key is pressed then continue in the current direction
    key = key if next_key == -1 else next_key

    # Determine the new head position based on the current direction
    new_head = [snake[0][0], snake[0][1]]

    # Update the position based on the key pressed
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    # If the snake hits the wall, make it appear on the opposite side
    if new_head[0] == 0:
        new_head[0] = sh - 2
    elif new_head[0] == sh - 1:
        new_head[0] = 1
    if new_head[1] == 0:
        new_head[1] = sw - 2
    elif new_head[1] == sw - 1:
        new_head[1] = 1

    # Insert the new head to the snake body
    snake.insert(0, new_head)

    # Check if snake has eaten the food
    if snake[0] == food:
        # If so, set food to None and increment score
        food = None
        score += 1
        while food is None:
            # Create new food
            nf = [
                random.randint(1, sh-2),
                random.randint(1, sw-2)
            ]
            # If the new food position is not part of the snake body, place it on the screen
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        # If not, keep moving the snake
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')

    # Add the new head to the screen
    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)