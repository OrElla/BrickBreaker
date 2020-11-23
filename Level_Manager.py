import turtle

class Level:

    def level_up(self, Ball_Game, Bricks, Build_Brick, level, num):
        Ball_Game.ball.setx(0)
        Ball_Game.ball.sety(0)


        num = Bricks.NUM_OF_BRICKS
        level += 1

        Bricks.Brick_Board = []
        Bricks.Bricks_list = []

        Bricks(Build_Brick[0], Build_Brick[1], Build_Brick[2], Build_Brick[3], Build_Brick[4], Build_Brick[5])
        return

