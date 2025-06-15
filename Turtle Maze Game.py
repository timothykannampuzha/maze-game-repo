import turtle  # Used for drawing and game display.
import random  # For random enemy movement direction.
import math  # Used to calculate distances.
import sys, os
# Hide Pygame's welcome message
sys.stdout = open(os.devnull, 'w')
import pygame  # Used for sound effects.
pygame.mixer.init()
sys.stdout = sys.__stdout__

# Initialize sound
pygame.mixer.init()
sound_collect = pygame.mixer.Sound("collect.wav")
special_collect = pygame.mixer.Sound("special_collect.wav")
sound_gameover = pygame.mixer.Sound("gameover.wav")
sound_win = pygame.mixer.Sound("win.wav")
# Loads different sound files for events like collecting gems, winning, and losing.

# Register images
images = [
    "run_right.gif", "run_left.gif",
    "treasure.gif", "special_gem.gif",
    "enemy_left.gif", "enemy_right.gif"
]
# Registers .gif images used for the player, enemies, and gems.
for image in images:
    turtle.register_shape(image)
try:
    turtle.register_shape("wall.gif")
    WALL_SHAPE_IMAGE = "wall.gif"
except turtle.TurtleGraphicsError:
    WALL_SHAPE_IMAGE = "square"
# Tries to use a custom wall image, falls back to a square if it fails.

screen = turtle.Screen()
screen.bgcolor("sky blue")
screen.title("Maze Game")
screen.setup(850, 850)
screen.tracer(0)
# Sets up the screen with a background, title, size, and disables auto-refresh.

# Wall Class
class WallShape(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape(WALL_SHAPE_IMAGE)
        self.color("brown")
        self.penup()
        self.speed(0)
# A turtle with a wall shape used to draw the walls.
# It is hidden and used only to stamp wall tiles onto the screen.

# Hero Class
class Hero(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("run_right.gif")
        self.penup()
        self.speed(0)
        self.gem = 0
    # Player character
    # Can move in 4 directions using arrow keys or WASD.
    # Avoids moving into wall coordinates stored in walls.
    # Tracks how many gems the player has collected.
    # collided(other): Checks if the hero is near another object (e.g. enemy or gem).

    def move_up(self):
        move_x = round(self.xcor())
        move_y = round(self.ycor() + 27)
        if (move_x, move_y) not in walls:
            self.goto(move_x, move_y)

    def move_down(self):
        move_x = round(self.xcor())
        move_y = round(self.ycor() - 27)
        if (move_x, move_y) not in walls:
            self.goto(move_x, move_y)

    def move_left(self):
        move_x = round(self.xcor() - 27)
        move_y = round(self.ycor())
        if (move_x, move_y) not in walls:
            self.goto(move_x, move_y)
        self.shape("run_left.gif")

    def move_right(self):
        move_x = round(self.xcor() + 27)
        move_y = round(self.ycor())
        if (move_x, move_y) not in walls:
            self.goto(move_x, move_y)
        self.shape("run_right.gif")

    def collided(self, other):
        ax = self.xcor() - other.xcor()
        ay = self.ycor() - other.ycor()
        return (ax * ax + ay * ay) < 400


# Gem Class
class Gem(turtle.Turtle):
    def __init__(self, x, y, value=100):
        super().__init__()
        self.shape("treasure.gif")
        self.penup()
        self.speed(0)
        self.gem = value
        self.goto(x, y)
    # Represents gems to be collected.
    # value: Score added when collected (100 or 500 for special gem).
    # destroy(): Hides the gem.
    # collided(): Checks if the player has touched it.

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

    def collided(self, other):
        ax = self.xcor() - other.xcor()
        ay = self.ycor() - other.ycor()
        return (ax * ax + ay * ay) < 400


# Opponent Class
class Opponent(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("enemy_left.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])
    # Enemy that moves toward the hero.
    # Chooses the next move that brings it closer (shortest distance).
    # Changes image based on direction (left/right).
    # destroy(): Hides the enemy.

    def move(self):
        best_distance = float("inf")
        best_move = None

        directions = {
            "up": (0, 27),
            "down": (0, -27),
            "left": (-27, 0),
            "right": (27, 0)
        }

        # Collect all enemy positions except self
        other_enemy_positions = {(round(enemy.xcor()), round(enemy.ycor())) for enemy in enemies if enemy != self}

        for direction, (ax, ay) in directions.items():
            new_x = round(self.xcor() + ax)
            new_y = round(self.ycor() + ay)
            if (new_x, new_y) not in walls and (new_x, new_y) not in other_enemy_positions:
                dist = math.hypot(hero.xcor() - new_x, hero.ycor() - new_y)
                if dist < best_distance:
                    best_distance = dist
                    best_move = (new_x, new_y)
                    self.direction = direction

        if best_move:
            self.goto(best_move[0], best_move[1])
            if self.direction == "left":
                self.shape("enemy_left.gif")
            elif self.direction == "right":
                self.shape("enemy_right.gif")

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP      XX       TXXE TX",
    "XXX     XX  XXXXX  XX  XX",
    "X              XX     GXX",
    "X   XXXXXXX   XXXX XXXXX",
    "X   XXT   XX    XX    TX",
    "XX  XX    XX    XX     X",
    "XX  XX    XX   XXXX    X",
    "XX  XX             E   X",
    "XX  XXXXXX  XXXXXXXXXXTX",
    "X       XX     XXT    XX",
    "X   XX  XX     XX     XX",
    "X   XX  XX         XXXXX",
    "X   XX  XX     XX  XXT X",
    "X   XX  XXT    XX  XX  X",
    "X   XX  XXXXX  XX  XX  X",
    "X       XXXXXX XX  XX  X",
    "X     E XX        XXXX X",
    "X   XXXXXX      XXXXX  X",
    "X       TXX     XXX    X",
    "X        XXXX  EXX     X",
    "X        XXXX  XXX     X",
    "X     XXXX             X",
    "X  T         XXXXXXXX  X",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"
]

# A list of strings that forms the game level.
# Symbols:
# X: Wall
# P: Player start position
# T: Normal gem
# G: Special gem
# E: Enemy
walls = []
treasures = []
enemies = []
# walls: Stores (x,y) positions of wall tiles.
# treasures: Stores all gem objects.
# enemies: Stores enemy objects.
# hud: Displays the number of gems collected.

wall_drawer = WallShape()
hero = Hero()

hud = turtle.Turtle()
hud.hideturtle()
hud.color("black")
hud.penup()
hud.goto(-320, 360)


def update_hud():
    hud.clear()
    hud.write(f"Gems: {hero.gem}", font=("Arial", 16, "bold"))
# Updates the score display.
# Shows a win or game-over message.


def show_message(text):
    message = turtle.Turtle()
    message.hideturtle()
    message.color("black")
    message.penup()
    message.goto(0, 0)
    message.write(text, align="center", font=("Arial", 24, "bold"))


def setup_maze(level):
    walls.clear()
    treasures.clear()
    enemies.clear()
    # Goes through each row and character in level_1.
    # Converts characters into positions and creates corresponding objects:
    # Wall → stamped at position
    # Player → placed there
    # Treasure/Special gem → added to list
    # Enemy → added to list
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -338 + (x * 27)
            screen_y = 338 - (y * 27)
            pos = (round(screen_x), round(screen_y))

            if character == "X":
                wall_drawer.goto(screen_x, screen_y)
                wall_drawer.stamp()
                walls.append(pos)
            elif character == "P":
                hero.goto(screen_x, screen_y)
            elif character == "T":
                treasures.append(Gem(screen_x, screen_y, value=100))
            elif character == "G":
                gem = Gem(screen_x, screen_y, value=500)
                gem.shape("special_gem.gif")
                treasures.append(gem)
            elif character == "E":
                gem_positions = [(g.xcor(), g.ycor()) for g in treasures]
                if (screen_x, screen_y) not in gem_positions:
                    enemies.append(Opponent(screen_x, screen_y))


game_over = False


def game_loop():
    global game_over
    if game_over:
        return

    for treasure in treasures[:]:
        if treasure.collided(hero):
            hero.gem += treasure.gem
            if treasure.shape() == "special_gem.gif":
                special_collect.play()
            else:
                sound_collect.play()
            update_hud()
            treasure.destroy()
            treasures.remove(treasure)

    # Checks for win:
    if not treasures:
        sound_win.play()
        show_message("\U0001F3C6 You win! \U0001F3C6")  # \U0001F3C6 is this "🏆"
        print("\U0001F3C6 You win! \U0001F3C6 Final Gems:", hero.gem)
        game_over = True
        return

    # Checks for enemy collision:
    for enemy in enemies:
        if hero.collided(enemy):
            sound_gameover.play()
            show_message("\U0001F480 Game Over! \U0001F480")
            print("\U0001F480 Game Over \U0001F480 Final Gems:", hero.gem)
            game_over = True
            return

    screen.update()
    screen.ontimer(game_loop, 20)


def move_enemies():
    if game_over:
        return  # Don't move anything if game ended

    for enemy in enemies:
        enemy.move()

    if not game_over:
        screen.ontimer(move_enemies, 500)


pressed_keys = set()

# Functions for key press
def press_up():
    pressed_keys.add("Up")
def release_up():
    pressed_keys.discard("Up")

def press_down():
    pressed_keys.add("Down")
def release_down():
    pressed_keys.discard("Down")

def press_left():
    pressed_keys.add("Left")
def release_left():
    pressed_keys.discard("Left")

def press_right():
    pressed_keys.add("Right")
def release_right():
    pressed_keys.discard("Right")

def press_w():
    pressed_keys.add("w")
def release_w():
    pressed_keys.discard("w")

def press_a():
    pressed_keys.add("a")
def release_a():
    pressed_keys.discard("a")

def press_s():
    pressed_keys.add("s")
def release_s():
    pressed_keys.discard("s")

def press_d():
    pressed_keys.add("d")
def release_d():
    pressed_keys.discard("d")

def continuous_move():
    if game_over:
        return

    # Check all pressed keys and move accordingly
    if "Up" in pressed_keys or "w" in pressed_keys:
        hero.move_up()
    if "Down" in pressed_keys or "s" in pressed_keys:
        hero.move_down()
    if "Left" in pressed_keys or "a" in pressed_keys:
        hero.move_left()
    if "Right" in pressed_keys or "d" in pressed_keys:
        hero.move_right()

    screen.ontimer(continuous_move, 100)  


setup_maze(level_1)
update_hud()

screen.listen()

# Assign key press/release handlers explicitly
screen.onkeypress(press_up, "Up")
screen.onkeyrelease(release_up, "Up")

screen.onkeypress(press_down, "Down")
screen.onkeyrelease(release_down, "Down")

screen.onkeypress(press_left, "Left")
screen.onkeyrelease(release_left, "Left")

screen.onkeypress(press_right, "Right")
screen.onkeyrelease(release_right, "Right")

screen.onkeypress(press_w, "w")
screen.onkeyrelease(release_w, "w")

screen.onkeypress(press_a, "a")
screen.onkeyrelease(release_a, "a")

screen.onkeypress(press_s, "s")
screen.onkeyrelease(release_s, "s")

screen.onkeypress(press_d, "d")
screen.onkeyrelease(release_d, "d")

game_loop()
move_enemies()
continuous_move()

turtle.done()

