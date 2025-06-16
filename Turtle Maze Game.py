import turtle  # Used for drawing and game display.
import random  # For random enemy movement direction.
import math  # Used to calculate distances.
import sys,os
sys.stdout=open(os.devnull,'w')
import pygame  # Used for sound effects.
pygame.mixer.init()
sys.stdout=sys.__stdout__

pygame.mixer.init()
sound_collect=pygame.mixer.Sound("collect.wav")
special_collect=pygame.mixer.Sound("special_collect.wav")
sound_gameover=pygame.mixer.Sound("gameover.wav")
sound_win=pygame.mixer.Sound("win.wav")

images=[
    "run_right.gif","run_left.gif",
    "treasure.gif","special_gem.gif",
    "enemy_left.gif","enemy_right.gif"
]
for image in images:
    turtle.register_shape(image)
try:
    turtle.register_shape("wall.gif")
    WALL_SHAPE_IMAGE="wall.gif"
except turtle.TurtleGraphicsError:
    WALL_SHAPE_IMAGE="square"

screen=turtle.Screen()
screen.bgcolor("sky blue")
screen.title("Maze Game")
screen.setup(850,850)
screen.tracer(0)

class WallShape(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape(WALL_SHAPE_IMAGE)
        self.color("brown")
        self.penup()
        self.speed(0)

class Hero(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("run_right.gif")
        self.penup()
        self.speed(0)
        self.gem=0

    def move_up(self):
        move_x=round(self.xcor())
        move_y=round(self.ycor()+27)
        if (move_x,move_y) not in walls:
            self.goto(move_x,move_y)

    def move_down(self):
        move_x=round(self.xcor())
        move_y=round(self.ycor()-27)
        if (move_x,move_y) not in walls:
            self.goto(move_x,move_y)

    def move_left(self):
        move_x=round(self.xcor()-27)
        move_y=round(self.ycor())
        if (move_x,move_y) not in walls:
            self.goto(move_x,move_y)
        self.shape("run_left.gif")

    def move_right(self):
        move_x=round(self.xcor()+27)
        move_y=round(self.ycor())
        if (move_x,move_y) not in walls:
            self.goto(move_x,move_y)
        self.shape("run_right.gif")

    def collided(self,other):
        ax=self.xcor()-other.xcor()
        ay=self.ycor()-other.ycor()
        return (ax*ax+ay*ay)<400

class Gem(turtle.Turtle):
    def __init__(self,x,y,value=100):
        super().__init__()
        self.shape("treasure.gif")
        self.penup()
        self.speed(0)
        self.gem=value
        self.goto(x,y)

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

    def collided(self,other):
        ax=self.xcor()-other.xcor()
        ay=self.ycor()-other.ycor()
        return (ax*ax+ay*ay)<400

class Opponent(turtle.Turtle):
    def __init__(self,x,y):
        super().__init__()
        self.shape("enemy_left.gif")
        self.penup()
        self.speed(0)
        self.goto(x,y)
        self.direction=random.choice(["up","down","left","right"])

    def move(self):
        best_distance=float("inf")
        best_move=None

        directions={
            "up":(0,27),
            "down":(0,-27),
            "left":(-27,0),
            "right":(27,0)
        }

        other_enemy_positions={(round(enemy.xcor()),round(enemy.ycor())) for enemy in enemies if enemy!=self}

        for direction,(ax,ay) in directions.items():
            new_x=round(self.xcor()+ax)
            new_y=round(self.ycor()+ay)
            if (new_x,new_y) not in walls and (new_x,new_y) not in other_enemy_positions:
                dist=math.hypot(hero.xcor()-new_x,hero.ycor()-new_y)
                if dist<best_distance:
                    best_distance=dist
                    best_move=(new_x,new_y)
                    self.direction=direction

        if best_move:
            self.goto(best_move[0],best_move[1])
            if self.direction=="left":
                self.shape("enemy_left.gif")
            elif self.direction=="right":
                self.shape("enemy_right.gif")

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

level_1=[
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

walls=[]
treasures=[]
enemies=[]

wall_drawer=WallShape()
hero=Hero()

hud=turtle.Turtle()
hud.hideturtle()
hud.color("black")
hud.penup()
hud.goto(-320,360)

def update_hud():
    hud.clear()
    hud.write(f"Gems: {hero.gem}",font=("Arial",16,"bold"))

def show_message(text):
    message=turtle.Turtle()
    message.hideturtle()
    message.color("black")
    message.penup()
    message.goto(0,0)
    message.write(text,align="center",font=("Arial",24,"bold"))

def setup_maze(level):
    walls.clear()
    treasures.clear()
    enemies.clear()
    for y in range(len(level)):
        for x in range(len(level[y])):
            character=level[y][x]
            screen_x=-338+(x*27)
            screen_y=338-(y*27)
            pos=(round(screen_x),round(screen_y))

            if character=="X":
                wall_drawer.goto(screen_x,screen_y)
                wall_drawer.stamp()
                walls.append(pos)
            elif character=="P":
                hero.goto(screen_x,screen_y)
            elif character=="T":
                treasures.append(Gem(screen_x,screen_y,value=100))
            elif character=="G":
                gem=Gem(screen_x,screen_y,value=500)
                gem.shape("special_gem.gif")
                treasures.append(gem)
            elif character=="E":
                gem_positions=[(g.xcor(),g.ycor()) for g in treasures]
                if (screen_x,screen_y) not in gem_positions:
                    enemies.append(Opponent(screen_x,screen_y))

game_over=False

def game_loop():
    global game_over
    if game_over:
        return

    for treasure in treasures[:]:
        if treasure.collided(hero):
            hero.gem+=treasure.gem
            if treasure.shape()=="special_gem.gif":
                special_collect.play()
            else:
                sound_collect.play()
            update_hud()
            treasure.destroy()
            treasures.remove(treasure)

    if not treasures:
        sound_win.play()
        show_message("\U0001F3C6 You win! \U0001F3C6")
        print("\U0001F3C6 You win! \U0001F3C6 Final Gems:",hero.gem)
        game_over=True
        return

    for enemy in enemies:
        if hero.collided(enemy):
            sound_gameover.play()
            show_message("\U0001F480 Game Over! \U0001F480")
            print("\U0001F480 Game Over \U0001F480 Final Gems:",hero.gem)
            game_over=True
            return

    screen.update()
    screen.ontimer(game_loop,10)

def move_enemies():
    if game_over:
        return
    for enemy in enemies:
        enemy.move()
    if not game_over:
        screen.ontimer(move_enemies,280)

pressed_keys = set()
# A set to track which keys are currently being pressed.
# This allows for smooth, continuous movement when a key is held down.

#Arrow keys
def press_up():
    pressed_keys.add("Up")
# Adds "Up" to the set when the Up arrow is pressed.

def release_up():
    pressed_keys.discard("Up")
# Removes "Up" from the set when the Up arrow is released.

def press_down():
    pressed_keys.add("Down")
# Adds "Down" to the set when the Down arrow is pressed.

def release_down():
    pressed_keys.discard("Down")
# Removes "Down" from the set when the Down arrow is released.

def press_left():
    pressed_keys.add("Left")
# Adds "Left" to the set when the Left arrow is pressed.

def release_left():
    pressed_keys.discard("Left")
# Removes "Left" from the set when the Left arrow is released.

def press_right():
    pressed_keys.add("Right")
# Adds "Right" to the set when the Right arrow is pressed.

def release_right():
    pressed_keys.discard("Right")
# Removes "Right" from the set when the Right arrow is released.

#WASD Keys
def press_w():
    pressed_keys.add("w")
# Adds "w" (move up) to the set when pressed.

def release_w():
    pressed_keys.discard("w")
# Removes "w" from the set when released.

def press_a():
    pressed_keys.add("a")
# Adds "a" (move left) to the set when pressed.

def release_a():
    pressed_keys.discard("a")
# Removes "a" from the set when released.

def press_s():
    pressed_keys.add("s")
# Adds "s" (move down) to the set when pressed.

def release_s():
    pressed_keys.discard("s")
# Removes "s" from the set when released.

def press_d():
    pressed_keys.add("d")
# Adds "d" (move right) to the set when pressed.

def release_d():
    pressed_keys.discard("d")
# Removes "d" from the set when released.

def continuous_move():
    if game_over:
        return
    # Stops movement if the game has ended.

    # Checks which keys are currently pressed and moves the hero
    if "Up" in pressed_keys or "w" in pressed_keys:
        hero.move_up()
    if "Down" in pressed_keys or "s" in pressed_keys:
        hero.move_down()
    if "Left" in pressed_keys or "a" in pressed_keys:
        hero.move_left()
    if "Right" in pressed_keys or "d" in pressed_keys:
        hero.move_right()

    screen.ontimer(continuous_move, 90)
    # this function runs every 90 milliseconds
    # Creates a loop for smooth movement while keys are held.

setup_maze(level_1)
update_hud()

screen.listen()
screen.onkeypress(press_up,"Up")
screen.onkeyrelease(release_up,"Up")
screen.onkeypress(press_down,"Down")
screen.onkeyrelease(release_down,"Down")
screen.onkeypress(press_left,"Left")
screen.onkeyrelease(release_left,"Left")
screen.onkeypress(press_right,"Right")
screen.onkeyrelease(release_right,"Right")
screen.onkeypress(press_w,"w")
screen.onkeyrelease(release_w,"w")
screen.onkeypress(press_a,"a")
screen.onkeyrelease(release_a,"a")
screen.onkeypress(press_s,"s")
screen.onkeyrelease(release_s,"s")
screen.onkeypress(press_d,"d")
screen.onkeyrelease(release_d,"d")
#This is for the movement. Both WASD & Arrow keys work.

game_loop()
move_enemies()
continuous_move()
#Loops to play the game
turtle.done()
