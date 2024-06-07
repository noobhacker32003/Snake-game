from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from random import randint
import random
import time

# Game settings
window_width = 1000
window_height = 800
snake_size = 20
snake_speed = 10
score = 0
boundary_offset = 120                                                                               # eta ki: bairer box ta
point_frozen = False
animation_enabled = True
magic_circles = []
circle_duration = 3                                                                                 # eta ki: magic circle disappear
game_paused = False
#snake respawn
snake = [[window_width // 2, window_height // 2]]
game_over = False

#food random respawn 
max_x = (window_width - 2 * boundary_offset - snake_size) // snake_size
max_y = (window_height - 2 * boundary_offset - snake_size) // snake_size
food = [randint(0, max_x) * snake_size + boundary_offset, 
        randint(0, max_y) * snake_size + boundary_offset]
direction = [snake_speed, 0]

# obstacle position and size
obstacles = [
    # Small obstacles
    {'pos': (150, 150), 'size': (50, 100)},
    {'pos': (600, 400), 'size': (50, 100)},

    # Larger obstacles
    {'pos': (200, 300), 'size': (150, 50)},
    {'pos': (450, 150), 'size': (150, 50)}
]

def draw_line(x0, y0, x1, y1):
    """ Draw a line using the Midpoint Line Algorithm """
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    glBegin(GL_POINTS)
    while True:
        glVertex2f(x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    glEnd()
    
def magic_circle():
    global radius, magic_circles

    for _ in range(3):
        c_x = random.randint(120, 850)
        c_y = random.randint(120, 630)
        creation_time = time.time()
        magic_circles.append((c_x, c_y, creation_time))

    # Set a timer to remove the circles after 3 s econds
    glutTimerFunc(3000, remove_magic_circles, 0)

    glutPostRedisplay()

def remove_magic_circles(value):
    global magic_circles
    current_time = time.time()
    magic_circles = [(x, y, creation_time) for x, y, creation_time in magic_circles if current_time - creation_time < circle_duration]
    glutPostRedisplay()

def draw_magic_circles():
    current_time = time.time()
    global magic_circles, circle_duration
    # Filter out expired magic circles
    magic_circles = [(x, y, creation_time) for x, y, creation_time in magic_circles if current_time - creation_time < circle_duration]
    glColor3f(0.0, 0.0, 1.0)  # Blue color for magic circles
    for circle in magic_circles:
        x, y, _ = circle
        draw_circle(x, y, snake_size // 2)


def check_collision_with_self():
    global snake, magic_circles

    head = snake[0]
    for segment in snake[1:]:
        # Check if the head collides with any other segment of the snake's body
        if head[0] == segment[0] and head[1] == segment[1]:                                             # x, y coordinate matching
            return True  # Collision detected with itself

    return False  # No collision with itself



def restart_game():
    global snake, food, direction, score, magic_circles, game_paused
    snake = [[window_width // 2, window_height // 2]]
    respawn_food()
    direction = [snake_speed, 0]
    score = 0
    magic_circles = []
    game_paused = False


# checking collision with the obstacles
def check_collision_with_obstacles():
    global snake, obstacles

    head = snake[0]
    head_x, head_y = head[0], head[1]
    
    for obstacle in obstacles:
        obs_x, obs_y = obstacle['pos']
        obs_width, obs_height = obstacle['size']

        if (head_x < obs_x + obs_width and head_x + snake_size > obs_x and
            head_y < obs_y + obs_height and head_y + snake_size > obs_y):
            return True  # Collision detected with an obstacle
    return False  # No collision with any obstacle

def close_button():
    draw_line(850,700,900,740)
    draw_line(850,740,900,700)
def magic_button():
    draw_line(100,710,125,740)
    draw_line(125,740,150,710)
    draw_line(150,710,100,730)
    draw_line(100,730,150,730)
    draw_line(100,710,150,730)
    draw_line(125,720,125,690)
def pause_button():
    draw_line(800,700,800,740)
    draw_line(820,700,820,740)
def reset_button():
    draw_line(750,720,780,720)
    draw_line(780,720,770,740)
    draw_line(780,720,770,700)
def play_button():
    draw_line(800, 700, 800, 740)
    draw_line(800, 740, 850, 720)
    draw_line(850, 720, 800, 700)

def convert_coordinate(x, y):
    global window_width,window_height, game_over                                    # game over ken lagbe ekhane
    a = x
    b = window_height- y
    return a, b


def mouse_click(button, state, x, y):
    global point_frozen, animation_enabled, game_over, game_paused

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x, y = convert_coordinate(x, y)

        if 850 < x < 900 and 700 < y < 740:
            glutLeaveMainLoop()

        elif 800 < x < 820 and 700 < y < 740:
            point_frozen = not point_frozen
            animation_enabled = not point_frozen
            game_paused = not game_paused

            glutPostRedisplay()

        elif 90 < x < 160 and 690 < y < 740:
            magic_circle()
        elif 750 < x < 780 and 700 < y < 740:
            restart_game()
            game_over = False

def draw_circle(cx, cy, r):
    """ Draw a circle using the Midpoint Circle Algorithm """
    x = 0
    y = r
    d = 1 - r
    glBegin(GL_POINTS)
    while x <= y:
        glVertex2f(cx + x, cy + y)
        glVertex2f(cx + y, cy + x)
        glVertex2f(cx - y, cy + x)
        glVertex2f(cx - x, cy + y)
        glVertex2f(cx - x, cy - y)
        glVertex2f(cx - y, cy - x)
        glVertex2f(cx + y, cy - x)
        glVertex2f(cx + x, cy - y)
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
    glEnd()

def draw_rect(x, y, width, height):
    """ Draw a filled rectangle using horizontal lines """
    for i in range(y, y + height):                                                          # y+height+1 hobe bc for loop
        draw_line(x, i, x + width, i)

def draw_obstacles():
    """ Draw obstacles within the game window """
    glColor3f(0.6, 0.3, 1.0)  # Orange color for obstacles
    for obstacle in obstacles:
        draw_rect(*obstacle['pos'], *obstacle['size'])                                      # confusion!

def display():
    global game_over

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    if game_over:
        show_game_over()
        close_button()
        reset_button()

    else:
        # Draw boundary lines with an offset inside the window
        glColor3f(1.0, 1.0, 1.0)
        draw_line(boundary_offset, boundary_offset, window_width - boundary_offset, boundary_offset)
        draw_line(boundary_offset, window_height - boundary_offset, window_width - boundary_offset, window_height - boundary_offset)
        draw_line(boundary_offset, boundary_offset, boundary_offset, window_height - boundary_offset)
        draw_line(window_width - boundary_offset, boundary_offset, window_width - boundary_offset, window_height - boundary_offset)

        # Draw snake
        glColor3f(0.0, 1.0, 0.0)
        for segment in snake:
            draw_rect(segment[0], segment[1], snake_size, snake_size)

        # Draw food
        glColor3f(1.0, 0.0, 0.0)
        draw_circle(food[0] + snake_size // 2, food[1] + snake_size // 2, snake_size // 2)
        draw_magic_circles()
        # Draw obstacles
        draw_obstacles()

        # Display score
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(10, window_height - 30)
        for char in f"Score: {score}":
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))                                        # reconsider

        # Buttons
        close_button()
        magic_button()
        reset_button()
        if game_paused:
            play_button()
        else:
            pause_button()

    glutSwapBuffers()

def show_game_over():
    glColor3f(1.0, 0.0, 0.0) 
    glWindowPos2i(window_width // 2 - 50, window_height // 2)
    game_over_text = "GAME OVER!!!!!"
    for char in game_over_text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))                                             # reconsider
    glWindowPos2i(window_width // 2 - 50, window_height // 2 - 20)
    final_score_text = f"Final Score: {score}"
    for char in final_score_text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))                                             # reconsider

def respawn_food():
    global food, obstacles

    max_x = (window_width - 2 * boundary_offset - snake_size) // snake_size
    max_y = (window_height - 2 * boundary_offset - snake_size) // snake_size
    
    # Loop until the food is placed outside the obstacles
    while True:
        food = [randint(0, max_x) * snake_size + boundary_offset, 
                randint(0, max_y) * snake_size + boundary_offset]

        # Check for collision with any obstacle
        collision = False
        for obstacle in obstacles:
            obs_x, obs_y = obstacle['pos']
            obs_width, obs_height = obstacle['size']

            if (food[0] < obs_x + obs_width and food[0] + snake_size > obs_x and                          
                food[1] < obs_y + obs_height and food[1] + snake_size > obs_y):
                collision = True                                                                             # could increase range here: Shafi
                break  # Food collided with an obstacle, break the loop
        
        # If no collision occurred, break the loop
        if not collision:
            break

def update(value):
    global snake, food, direction, score, magic_circles, animation_enabled, game_paused, game_over

    if not game_paused and not game_paused:                                                                     # ekhane ekta ki game_over hobe? Shafi
        # Move the snake with Wrap-around logic
        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

        # Check if the snake's head goes outside the boundary
        if (new_head[0] >= window_width - boundary_offset or new_head[0] < boundary_offset or
                new_head[1] >= window_height - boundary_offset or new_head[1] < boundary_offset):       
            game_over = True
        else:
            # Continue moving the snake within the boundary
            snake.insert(0, new_head)

            # Check for collision with itself
            if check_collision_with_self():
                game_over = True
            elif check_collision_with_obstacles():
                game_over = True
            else:
                snake.pop()

        # Check for collision with magic circles
        collided_circles = []
        for circle in magic_circles:
            circle_x, circle_y, _ = circle
            circle_center_x = circle_x + snake_size // 2
            circle_center_y = circle_y + snake_size // 2

            # Check if the distance between the centers is less than or equal to the sum of the radii               # ei distance ta normal food eo apply kroa jae
            distance = ((new_head[0] + snake_size // 2 - circle_center_x) ** 2 +
                        (new_head[1] + snake_size // 2 - circle_center_y) ** 2) ** 0.5
            if distance <= snake_size // 2 + snake_size // 10:  # Adjust the divisor for 20% coverage               # confusion
                # Collision with a magic circle
                collided_circles.append(circle)

        # Remove collided magic circles
        for circle in collided_circles:
            magic_circles.remove(circle)

        # Increase score by 5 for each collided magic circle
        score += len(collided_circles) * 5

        # Check for collision with food
        if snake[0][0] == food[0] and snake[0][1] == food[1]:
            score += 1
            respawn_food()
            snake.append(snake[-1])

    glutPostRedisplay()
    glutTimerFunc(100, update, 0)

def toggle_pause():
    global game_paused
    if game_paused:
        game_paused = False
    else:
        game_paused = True

def keyboard(key, x, y):
    global direction, game_paused
    
    if key == GLUT_KEY_LEFT and direction[0] != snake_speed:
        direction = [-snake_speed, 0]
    elif  key == GLUT_KEY_RIGHT and direction[0] != -snake_speed:
        direction = [snake_speed, 0]
    elif key == GLUT_KEY_DOWN and direction[1] != snake_speed:
        direction = [0, -snake_speed]
    elif key == GLUT_KEY_UP and direction[1] != -snake_speed:
        direction = [0, snake_speed]
    elif key == b' ':
        toggle_pause()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Snake Game")
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(keyboard)
glutTimerFunc(100, update, 0)
glutMouseFunc(mouse_click)
glClearColor(0.0, 0.0, 0.0, 1.0)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, window_width, 0, window_height)
glMatrixMode(GL_MODELVIEW)
glutMainLoop()