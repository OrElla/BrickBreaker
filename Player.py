import turtle

class Player:
    paddle = turtle.Turtle()
    paddle.speed(0)
    Player_Moving_Limit = 100
    player_wid, player_len = 1, 5
    score = 0
    live = 3
    bullets = 0

    def __init__(self,x,y,Player_move, Left_Limit, Right_Limit):
        self.x = x
        self.y = y
        self.Player_move = Player_move
        self.Left_Limit = Left_Limit
        self.Right_Limit = Right_Limit
        self.createPlayer()


    def createPlayer(self):

        self.paddle.shape("square")
        self.paddle.color("white")
        self.paddle.shapesize(stretch_wid=self.player_wid, stretch_len=self.player_len)
        self.paddle.penup()
        self.paddle.goto(self.x, self.y)

    def move_left(self):

        if self.paddle.xcor()-Player.Player_Moving_Limit < -440:
            self.paddle.setx(self.Left_Limit)
        else:
            self.paddle.forward(-self.Player_move)

    def move_right(self):
        if self.paddle.xcor()+Player.Player_Moving_Limit > 440:
            self.paddle.setx(self.Right_Limit)
        else:
            self.paddle.forward(self.Player_move)
