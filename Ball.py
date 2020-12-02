import turtle

class Ball:
    ball = turtle.Turtle()
    ball.speed(0)

    direction_x,direction_y  = 2,2

    lose_turn = False
    ball_is_moving = True

    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.createBall(self.x,self.y)

    def createBall(self,x,y):
        self.ball.speed(1)
        self.ball.shape("circle")
        self.ball.color("white")
        self.ball.penup()
        self.ball.goto(self.x, self.y)

    def move_ball(self,player_down_limit, up_limit):

        self.ball.setx(self.ball.xcor() + self.direction_x)
        self.ball.sety(self.ball.ycor() + self.direction_y)

        if self.ball.ycor() >= up_limit:
            self.ball.sety(up_limit)
            self.direction_y *= -1

        elif self.ball.ycor() < player_down_limit:
            self.lose_turn = True
            return

        if self.ball.xcor() > 440:
            self.ball.setx(440)
            self.direction_x *= -1

        elif self.ball.xcor() < -440:
            self.ball.setx(-440)
            self.direction_x *= -1

    ## set the ball direction in case of new turn or catching ball
    def set_ball_start_y_direction(self):
        if self.direction_y < 0:
            self.direction_y *= -1

    def set_ball_start_x_direction(self, paddle_x):

        if paddle_x > 0:
            if self.direction_x > 0:
                return
            else:
                self.direction_x *= -1
        else:
            if self.direction_x < 0:
                return
            else:
                self.direction_x *= -1

    ## set ball position in case of new turn or catching ball
    def set_ball_start_position(self, paddle_x, paddle_y):
        self.ball.setx(paddle_x)
        self.ball.sety(paddle_y + 50)




