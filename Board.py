import turtle
import time

Window_width = 900
Window_height = 800

Right_Limit = Window_width / 2 - 55
Left_Limit = -Right_Limit
Player_move = abs((Left_Limit-Right_Limit)/10)
up_limit = Window_height / 2 - 15 - Player_move / 2
down_limit_player = -Window_height / 2.5 - 20
N = 11

### inc. ball veloc, dec. ball veloc, inc. paddle, dec. paddle, catch ball, bullet, fire, protect, life

level_color = ["red", "green", "blue",  "yellow", "cornsilk4", "orange", "DarkOrange3", "purple", "VioletRed4"]
intro_titles = ["Faster Ball","Slower Ball", "Increase Paddle","Decrease Paddle","Catch Ball","Bullet",
                "Destroy Enemy & Bricks", "Enemy"]

def create_rectangle(obj):
    for i in range(4):
        if i % 2 == 0:
            obj.backward(Player_move)
        else:
            obj.backward(Player_move / 2)
        obj.left(90)

class Board():

    window = turtle.Screen()
    score_bar = turtle.Turtle()
    game_titles = turtle.Turtle()

    intro_shape = turtle.Turtle()


    def __init__(self,win_width, win_height):
        self.window.title("Brick Breaker")
        self.window.setup(width=Window_width, height=Window_height)
        self.add_game_images()
        #self.window.bgcolor("black")
        self.window.bgpic('pics/space.gif')
        self.window.tracer(0)

        self.line_bar()


    def line_bar(self):

        up_line_bar = turtle.Turtle()
        up_line_bar.color("white")
        up_line_bar.penup()
        up_line_bar.hideturtle()
        up_line_bar.goto(Right_Limit+40,Window_height / 2 - Player_move / 2 -5)
        up_line_bar.pendown()
        up_line_bar.setheading(180)
        up_line_bar.forward(Window_width-20)
        up_line_bar.penup()
        self.create_bar()


    def create_bar(self):

        self.score_bar.speed(0)
        self.score_bar.color("yellow")
        self.score_bar.penup()
        self.score_bar.hideturtle()
        self.score_bar.goto(0, Window_height / 2 - 40)

        score_str = "Score: " + str(0) + "     Live:  " + str(3) + "     Level:  " + str(1)
        self.score_bar.write(score_str, align="center", font=("Courier", 24, "normal"))
        self.game_titles.hideturtle()
        self.game_titles.goto(0,0)
        self.game_titles.color("white")
        self.create_intro()



    def add_game_images(self):
        self.window.addshape('pics/space.gif')
        self.window.addshape('pics/devil.gif')
        self.window.addshape('pics/fire.gif')
        self.window.addshape('pics/bullet.gif')
        self.window.addshape('pics/life.gif')
        self.window.addshape('pics/p.gif')
        self.window.addshape('pics/d_r.gif')







    def create_intro(self):

        self.intro_shape.hideturtle()
        self.intro_shape.penup()
        self.game_titles.penup()

        ## New Game Title ##
        self.intro_game_title(0,250,"New Game", "gold")

        ## intro ##
        self.intro_game_title(0,180,"Intro", "green")

        x,y = -100, 100
        for i in range(len(level_color)-1):
            self.intro_game_title(x, y, intro_titles[i], level_color[i])
            y -=50


    def intro_game_title(self,x,y,str, color):

        if str == "New Game":
            self.game_titles.color("gold")
            font = 60
        elif str == "Intro":
            self.game_titles.color("green")
            font = 48
        else:
            font = 36
            self.game_titles.color("white")
            self.intro_shape.begin_fill()
            self.intro_shape.goto(x + 300, y)
            self.intro_shape.color(color)
            self.intro_shape.circle(20)
            self.intro_shape.end_fill()

        self.game_titles.goto(x,y)
        self.game_titles.write(str, align="center", font=("Courier", font, "normal"))



    def new_game_titles(self):

        self.game_titles.goto(0,0)
        self.game_titles.clear()
        self.intro_shape.clear()












