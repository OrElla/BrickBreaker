from Board import *
from Player import Player
from Ball import Ball
from Bricks import Bricks
from Enemy import Enemy
from Prizes import Prizes
# from Level_Manager import Level

class Controller():
    level = 1
    game_over = False

    #Board(Window_width, Window_height)
    BrickS = Bricks(level, Right_Limit + 35, up_limit, Player_move, Left_Limit, N)
    Paddle_game = Player(0, down_limit_player +20, Player_move, Left_Limit, Right_Limit)
    Ball_Game = Ball(Paddle_game.paddle.xcor() / 2 - 50, Paddle_game.Player_Moving_Limit / 2)
    Enemies = Enemy()
    Prize = Prizes()
    num = BrickS.NUM_OF_BRICKS


    #Board.window.listen()
    Board.window.onkey(Paddle_game.move_left, "Left")
    Board.window.onkey(Paddle_game.move_right, "Right")
    # Build_Brick = level, Right_Limit + 35, up_limit , Player_move, Left_Limit, N

    def levelUp(self):

        self.Ball_Game.set_ball_start_position(self.Paddle_game.paddle.xcor(), self.Paddle_game.paddle.ycor())
        self.Ball_Game.set_ball_start_y_direction()
        self.level += 1
        self.Update_bar()
        self.BrickS.Brick_Board = []
        self.BrickS.Bricks_list = []
        self.BrickS.CreateBricks(self.level)
        self.num = self.BrickS.NUM_OF_BRICKS

        ########################### update ###########################
        if self.level > 3:
            self.Enemies.enemy_list, self.Enemies.enemy_t = [], []
            self.Enemies.counter_enemies, self.Enemies.num_of_enemies = -1, 0

        time.sleep(1)
        Board.game_titles.clear()
        self.RunGame()

    def get_level(self):
        return self.level

    def fill_color_brick(self, obj, color):
        obj.goto(obj.xcor(), obj.ycor())
        obj.begin_fill()
        obj.pendown()
        create_rectangle(obj)
        #obj.fillcolor(level_color[color])
        obj.fillcolor(level_color[self.level-1])
        obj.penup()
        obj.end_fill()

    ### if the brick's value is 0, it'll disappear
    # updates the currently left bricks
    def clear_brick(self, brick):
        brick.reset()
        brick.clear()
        brick.hideturtle()
        self.num -= 1

    ### check the status of the bricks ###
    def checkBricks(self):

        for i in range(self.BrickS.NUM_OF_BRICKS):
            if self.BrickS.Bricks_list[i][3] > 0:
                if self.isCollision(self.BrickS.Brick_Board[i], Ball.ball):
                    self.manage_collisions(i, 0) # 0 = ball and brick

                if self.Paddle_game.bullets > 0 and self.Prize.is_fire:
                    if self.isCollision(self.BrickS.Brick_Board[i], self.Prize.fire_t):
                        self.manage_collisions(i, 1) # 1 = bullet/flame and brick
                        self.bullet_collision_states()


    ### manage collision of bricks
    # collide item: 0 - collision ball and brick, 1 - bullet and brick
    # i = index of this brick
    def manage_collisions(self, i, collide_item):

        # if there are no bullets or flames
        if self.level == 1 or collide_item == 0:
            if collide_item == 0:
                #print "ball"
                self.BrickS.Bricks_list[i][3] -= 1

        # if collide_item = 1 -> bullet or flame:
        else:
            self.BrickS.Bricks_list[i][3] = 0

        if self.level > 1:
            if collide_item == 0:
               self.Ball_Game.direction_y *= -1

            if self.BrickS.Bricks_list[i][3] >= 1:
               self.fill_color_brick(self.BrickS.Brick_Board[i], self.BrickS.Bricks_list[i][3])

               self.Prize.is_prize = True
        self.Paddle_game.score += 1 * self.level
        self.Update_bar()

        if i % 2 == 0 and self.BrickS.Bricks_list[i][3] >= 1:
            self.Prize.Create_Prize(self.BrickS.Bricks_list[i][1], self.BrickS.Bricks_list[i][2], self.level)
        if self.level >2 and i % 3 == 0 and self.BrickS.Bricks_list[i][3] >= 1 :
            self.Enemies.create_enemy(self.BrickS.Bricks_list[i][1] + 50, self.BrickS.Bricks_list[i][2], self.level)

        if self.BrickS.Bricks_list[i][3] == 0:
            self.clear_brick(self.BrickS.Brick_Board[i])

    ### should be updated and added to the main loop
    def Game_States(self):
        if not self.game_over and self.num >0 and self.level <= len(level_color):
            return True
        else:
            return False


    #####  Run Game - Main Game Loop  #####
    def RunGame(self):

        self.define_keys_states()

        while self.Game_States():
            Board.window.update()

            if not self.Prize.catch_ball and self.Ball_Game.ball_is_moving:
                self.Ball_Game.move_ball(down_limit_player, up_limit)

            if self.Ball_Game.lose_turn:
                self.manage_turn()

            if self.isCollision(self.Ball_Game.ball, self.Paddle_game.paddle):
                self.Ball_Game.direction_y *= -1

            if self.level > 1 and self.Prize.is_prize:
                self.prizes_states()

            self.checkBricks()

        if self.num == 0:
            Board.window.update()
            self.Update_game_titles("Level Up")
            self.levelUp()

    ### define the next state if player lost a turn
    def manage_turn(self):
        self.Ball_Game.lose_turn = False
        self.Paddle_game.live -= 1

        self.Ball_Game.set_ball_start_position(self.Paddle_game.paddle.xcor(), self.Paddle_game.paddle.ycor())
        self.Ball_Game.set_ball_start_y_direction()

        if self.Paddle_game.live == 0:
            self.game_over = True
            self.Update_game_titles("Game Over")
        self.Update_bar()


    ###   Check Collision   ###
    def isCollision(self, obj1, obj2):

        ### collison Ball and Paddle
        if obj2 == self.Paddle_game.paddle:
            if ((obj1.ycor() <= obj2.ycor() + 25) and
                 (obj1.xcor() <= obj2.xcor() + 75) and
                  (obj1.xcor() >= obj2.xcor() - 75)):

                if obj1 == self.Ball_Game.ball:
                    d = obj2.xcor() - self.Ball_Game.ball.xcor()
                    if obj2.xcor() > 0:
                        if d > 55:
                            self.Ball_Game.direction_x *= -1
                    elif obj2.xcor() < 0:
                        if d < -55:
                            self.Ball_Game.direction_x *= -1
                return True

        ## collison Brick and Ball ##
        ## collison Brick and Bullet ##
        else:
            if ((obj1.ycor() >= obj2.ycor()) and
                    ((obj1.ycor() <= obj2.ycor() + Player_move * 2 / 3))
                    and
                    (obj1.xcor() >= obj2.xcor()) and
                    ((obj1.xcor() <= obj2.xcor() + Player_move + 10))):

                if obj2.xcor > 0 and self.level > 1:
                    if obj2 == self.Ball_Game.ball: ## only if collision with ball
                        self.Ball_Game.direction_x *= -1
                return True
        return False

    ## check if player can fire and already clicked on fire ##
    def can_fire(self):
        if self.Paddle_game.bullets > 0 and not self.Prize.is_fire:
            self.Prize.is_fire = True
            self.Prize.fire_t.goto(self.Paddle_game.paddle.xcor(), self.Paddle_game.paddle.ycor()+10)
        self.checkBricks()



    ###  define the prizes states  ###
    def prizes_states(self):

        if self.Prize.is_protected:
            self.Prize.manage_protected_time(self.Paddle_game.paddle,self.Update_game_titles,Board.game_titles)


        # move the prize, if game isn't paused #
        if self.Prize.is_prize and self.Ball_Game.ball_is_moving:
            self.Prize.move_Prize(self.isCollision, self.Paddle_game, self.Ball_Game, self.Update_bar)
        # catch ball state #
        if self.Prize.catch_ball:
            self.Ball_Game.set_ball_start_position(self.Paddle_game.paddle.xcor(),self.Paddle_game.paddle.ycor()-20)
        # if player has bullets, move them #
        if self.Paddle_game.bullets > 0 and self.Prize.is_fire:
            self.Prize.fire_move(up_limit, self.Update_bar, self.Paddle_game)
        # if there are enemies, manage their behavior #
        if self.Enemies.num_of_enemies > 0:
            self.Enemies.manage_enemies(down_limit_player, self.Paddle_game.paddle ,
                                        self.isCollision, self.Ball_Game.ball_is_moving, self.level)
            #if self.Enemies.enemy_can_fire:
             #   self.Enemies.move_enemy_fire(self.Paddle_game.paddle,self.isCollision)

            # if enemy collides with player, player loses 1 live #
            if self.Enemies.enemy_collide_player and not self.Prize.is_protected:
                self.manage_turn()
            # check collision of enemy and bullet #
            if self.Paddle_game.bullets > 0:
                if self.Enemies.enemy_bullet(self.Prize.fire_t):
                    self.Paddle_game.score += 10
                    #print "killed enemy!"
                    self.bullet_collision_states()


    ## after bullet collision with something update it's state
    def bullet_collision_states(self):
        self.Paddle_game.bullets -= 1
        self.Prize.is_fire = False
        self.Prize.fire_t.sety(self.Paddle_game.paddle.ycor() - Window_height / 4)
        self.Prize.fire_t.hideturtle()
        self.Update_bar()

    # if the player caught, update ball position, and do it again after he released it
    def PlayBall(self):
        if self.Prize.catch_ball:
            self.Ball_Game.set_ball_start_position(self.Paddle_game.paddle.xcor(),self.Paddle_game.paddle.ycor())
        self.Prize.catch_ball = False


    # in case of new game, restore player's data
    def new_game_player(self):
        self.Paddle_game.live = 3
        self.Paddle_game.score = 0
        self.level = 0
        self.game_over = False
        self.levelUp()
        Board.window.update()
        print "new player"



    ## on click states##
    def define_keys_states(self):

        Board.window.onkey(self.PlayBall, "Up")
        Board.window.onkey(self.can_fire, "Down")
        Board.window.onkey(self.fire_cheat, "p")
        Board.window.onkey(self.life_cheat, "l")
        Board.window.onkey(self.Pause_Game, "b")
        Board.window.onkey(self.slow_ball_cheat, "s")
        Board.window.onkey(self.faster_ball_cheat, "f")
        Board.window.onkey(self.increase_paddle_cheat, "i")
        Board.window.onkey(self.decrease_ball_cheat, "d")
        Board.window.onkey(self.catch_ball_cheat, "c")
        Board.window.onkey(self.protected_from_enemy_cheat, "w")
        Board.window.onkey(self.delete_bricks_cheat, "o")



    ## Title Bar
    def Update_bar(self):
        Board.score_bar.clear()
        score_str = "Score: " + str(self.Paddle_game.score) + "     Live:  " + str(self.Paddle_game.live) + \
                "     Level:  " + str(self.level)

        if self.Paddle_game.bullets > 0:
            score_str = score_str + "   Fire: " + str(self.Paddle_game.bullets)
        Board.score_bar.write(score_str, align="center", font=("Courier", 24, "normal"))


    def Update_game_titles(self,str):
        Board.game_titles.write(str, align="center", font=("Courier", 48, "normal"))



    ## click 'b' - hold the ball, pause game
    def Pause_Game(self):
        if self.Ball_Game.ball_is_moving:
            self.Ball_Game.ball_is_moving = False
            self.Update_game_titles("Paused")

        else:
            Board.game_titles.clear()
            self.Ball_Game.ball_is_moving = True


    ### Cheats ###
    # add bullets

    # add bullets - click 'p'
    def fire_cheat(self):
        self.Paddle_game.bullets += 2

    # add life - click 'l'
    def life_cheat(self):
        self.Prize.add_live(self.Paddle_game, self.Update_bar)

    # increase ball's velocity - click 's'
    def slow_ball_cheat(self):
        self.Prize.slow_ball(self.Ball_Game)

    # decrease ball's velocity - click 'f'
    def faster_ball_cheat(self):
        self.Prize.faster_ball(self.Ball_Game)

    # increase paddle size - click 'i'
    def increase_paddle_cheat(self):
        self.Prize.increase_paddle(self.Paddle_game)

    # decrease paddle size - click 'd'
    def decrease_ball_cheat(self):
        self.Prize.decrease_paddle(self.Paddle_game)

    # handle the ball - click 'c'
    def catch_ball_cheat(self):
        self.Prize.catch_ball_state(self.Ball_Game, self.Paddle_game.paddle.xcor(), self.Paddle_game.paddle.ycor())

    # protected from enemy's attack - click 'w'
    def protected_from_enemy_cheat(self):
        self.Prize.protecetd_player(self.Paddle_game)

    # clear all bricks but 2 - click 'o'
    def delete_bricks_cheat(self):
        i = 0
        while i < self.BrickS.NUM_OF_BRICKS -2:
            self.BrickS.Bricks_list[i][3] = 0
            self.clear_brick(self.BrickS.Brick_Board[i])
            i += 1








