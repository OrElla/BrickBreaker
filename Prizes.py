import turtle
import random
from Board import level_color, Window_width, Window_height, time

class Prizes:
    prize_color,game_timer, elapsed_time = 0, 0, 0
    time_off = 10

    is_prize,catch_ball,is_fire, is_protected = False, False, False, False

    fire_t = turtle.Turtle()
    fire_t.hideturtle()
    fire_t.penup()

    prize_t = []  # prize_turtle list
    prize_list = [] # prizes list and values
    counter_prizes = -1 # counter any created prize
    num_of_prizes = 0 # defines current num of prizes

    ### Prize state ###
    ### create the prize turtle ###
    def Create_Prize(self,x,y, level):

        self.counter_prizes += 1
        self.num_of_prizes += 1

        self.prize_t.append(turtle.Turtle())
        self.prize_list.append(1)
        self.prize_t[self.counter_prizes].showturtle()

        if level == 2:
            self.prize_color = random.randint(0, 3)
        elif level <= 4:
            self.prize_color = random.randint(0, 5)
        else:
            self.prize_color = random.randint(0, len(level_color) - 1)



        self.prize_list[self.counter_prizes] = self.prize_color

        self.prize_shape(self.counter_prizes)
        self.prize_t[self.counter_prizes].penup()
        self.prize_t[self.counter_prizes].goto(x, y)

    ## move the prize turtle ##
    def move_Prize(self, isCollision,Paddle_game,Ball_Game, Update_bar):

        for i in range(self.counter_prizes+1):
            # if there is no prize in this cell
            if self.prize_list[i] == -1:
                continue
            else:
                self.prize_t[i].sety(self.prize_t[i].ycor() - 2)
                self.prize_t[i].right(80)

                if isCollision(self.prize_t[i], Paddle_game.paddle):
                    self.ManagePrize(Ball_Game, Paddle_game, Update_bar, i)
                    # self.prize.reset()
                    self.clear_prize(i)
                    #self.prize_t[i].hideturtle()
                    #self.prize_t[i].sety(Paddle_game.paddle.ycor() - Window_height / 4)
                    #self.is_prize = False

                if self.prize_t[i].ycor() < Paddle_game.paddle.ycor() - 70:
                    self.clear_prize(i)
                    #self.is_prize = False

    ## define the prize according the color ##
    def ManagePrize(self,Ball_Game, Paddle_game, Update_bar,i):

        # red = faster ball
        if self.prize_list[i] == 0:
            if Ball_Game.direction_x <= 10 and Ball_Game.direction_y <= 10:
                self.faster_ball(Ball_Game)
            self.prize_list[i] =-1

        # green = slower paddle
        if self.prize_list[i] ==  1:
            if Ball_Game.direction_x >= 2 and Ball_Game.direction_y >= 2:
                self.slow_ball(Ball_Game)
            self.prize_list[i] = -1

        # blue = increase paddle
        if self.prize_list[i] == 2:
            self.increase_paddle(Paddle_game)
            self.prize_list[i] = -1

        # yellow - decrease paddle
        if self.prize_list[i] == 3:
            self.decrease_paddle(Paddle_game)
            self.prize_list[i] = -1

        # grey - catch ball
        if self.prize_list[i] == 4:
            self.catch_ball_state(Ball_Game, Paddle_game.paddle.xcor(), Paddle_game.paddle.ycor())
            self.prize_list[i] = -1

        # orange/bullet - bullet
        if self.prize_list[i] == 5:
            #self.prize.shape('pics/bullet.gif')
            self.create_fire_ball(Paddle_game,Update_bar)
            self.prize_list[i] = -1

        ##### fix ####
        # fire - flame
        if self.prize_list[i] == 6:
            #self.prize.shape('pics/fire.gif')
            self.create_fire_ball(Paddle_game,Update_bar)
            self.prize_list[i] = -1

        if self.prize_list[i] == 7:
            self.protecetd_player(Paddle_game)

        if self.prize_list[i] == 8:
            self.add_live(Paddle_game, Update_bar)


    ## defines thr prize's shape and color
    def prize_shape(self, i):
        # if self.prize_color == 5:
        if self.prize_list[i] == 5:
            #print "new bullet"
            self.prize_t[i].shape('pics/bullet.gif')

        elif self.prize_list[i] == 6:
            self.prize_t[i].shape('pics/fire.gif')
            #print "new fire"

        elif self.prize_list[i] == 8:
            self.prize_t[i].shape('pics/life.gif')

        else:
            self.prize_t[i].shape("square")
            self.prize_t[i].color(level_color[self.prize_list[i]])



    ### fire state ###
    ## create the bullet turtle ##
    def create_fire_ball(self,Paddle_game, Update_bar):

        Paddle_game.bullets += 1
        self.fire_t.speed(1)

        self.prize_color = random.randint(5,6)

        #self.fire_t.shape("triangle")
        if self.prize_color == 5:
            self.fire_t.shape("pics/bullet.gif")
        if self.prize_color == 6:
            self.fire_t.shape("pics/fire.gif")

        self.fire_t.penup()
        Update_bar()


    ## move the bullet turtle ##
    def fire_move(self,up_limit,Update_bar,Paddle_game):
        self.fire_t.showturtle()
        self.fire_t.sety(self.fire_t.ycor() + 4)

        if self.fire_t.ycor() > up_limit and self.is_fire:
            self.fire_t.hideturtle()
            Paddle_game.bullets -= 1
            self.is_fire = False
            Update_bar()



    # increase ball's velocity
    def slow_ball(self, Ball_game):
        Ball_game.direction_x /= 1.5
        Ball_game.direction_y /= 1.5

    # decrease ball's velocity
    def faster_ball(self, Ball_game):
        Ball_game.direction_x *= 1.5
        Ball_game.direction_y *= 1.5

    def increase_paddle(self, Paddle_game):
        if Paddle_game.player_len < 9:
            if Paddle_game.player_len + 4 > 9:
                Paddle_game.player_len = 9
            else:
                Paddle_game.player_len += 4
        Paddle_game.paddle.shapesize(Paddle_game.player_wid, Paddle_game.player_len)


    def decrease_paddle(self, Paddle_game):
        if Paddle_game.player_len > 1:
            if Paddle_game.player_len - 2 < 1:
                Paddle_game.player_len = 1
            else:
                Paddle_game.player_len -= 2
        Paddle_game.paddle.shapesize(Paddle_game.player_wid, Paddle_game.player_len)


    def catch_ball_state(self, Ball_Game, paddle_x, paddle_y):

        Ball_Game.ball.setx(paddle_x)
        Ball_Game.ball.sety(paddle_y + 20)
        self.catch_ball = True

        Ball_Game.set_ball_start_y_direction()
        Ball_Game.set_ball_start_x_direction(paddle_x)


    def protecetd_player(self, paddle):
        self.is_protected = True
        paddle.paddle.color("gold")


    def manage_protected_time(self, paddle, Update_game_titles , Board_game_titles):
        ## start timer
        if self.game_timer == 0:
            self.game_timer = time.time()

        # if timer already started, compare with elapsed_time
        else:
            self.elapsed_time = time.time() - self.game_timer
            time_left = int(self.time_off - self.elapsed_time)

            if time_left > 0:
                Board_game_titles.goto(0, 50)
                self.protected_timer_and_alerts(time_left, Update_game_titles, Board_game_titles)
            else:
                Board_game_titles.goto(0,0)
                Board_game_titles.clear()
                paddle.color("white")
                self.clear_player_protected()

    def protected_timer_and_alerts(self,time_left, Update_game_titles , Board_game_titles):
        # alerts to the player
        if time_left > 0:
            if time_left >= 9:
                Update_game_titles("10 seconds of protected")
            elif time_left <= 3:
                Board_game_titles.clear()
                Update_game_titles(time_left)
            else:
                Board_game_titles.clear()


    def add_live(self, paddle, Update_Bar):
        paddle.live += 1
        Update_Bar()

    def clear_player_protected(self):
        self.is_protected = False
        self.game_timer = 0
        self.elapsed_time = 0


    ##clear prize img, and update the list and num of prizes
    def clear_prize(self, i):
            self.prize_t[i].hideturtle()
            self.num_of_prizes -= 1
            self.prize_list[i] = -1




