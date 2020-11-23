import turtle
import random

class Enemy:

    enemy_t = []      # enemies_turtle list
    enemy_list = []   # enemies list and values
    counter_enemies = -1 # counter any created enemy
    num_of_enemies = 0 # defines current num of enemies

    # handle collisions states with player and bullet
    enemy_collide_player,enemy_collide_bullet = False, False
    # defines player's bullets status
    current_bullet = 0
    player_can_fire = False

    enemy_can_fire,enemy_fire_is_moving  = False, False

    enemy_fire = turtle.Turtle()
    enemy_fire.hideturtle()


    ### create enemies and updates enemy_list with value 1 (exist enemy)
    def create_enemy(self,x,y, level):
        self.counter_enemies += 1
        self.num_of_enemies += 1

        self.enemy_t.append(turtle.Turtle())
        self.enemy_list.append(1)
        self.enemy_t[self.counter_enemies].showturtle()


        if level >=4:
            if self.counter_enemies != 0 and (self.counter_enemies % 5 == 0 or self.counter_enemies % 2 == 0):
                if level >=5:
                    if self.counter_enemies % 10 != 0 and self.counter_enemies % 2 == 0:
                        self.enemy_t[self.counter_enemies].shape('pics/devil.gif')
                        #print "smart"
                    elif self.counter_enemies % 5 == 0:
                        self.enemy_t[self.counter_enemies].shape('pics/p.gif')
                        #print "enemy can shoot"
                else:
                    self.enemy_t[self.counter_enemies].shape('pics/devil.gif')
                    #print "smart"

            else:
                self.enemy_t[self.counter_enemies].shape('pics/d_r.gif')
                #print "regular"
        else:
            self.enemy_t[self.counter_enemies].shape('pics/d_r.gif')
            #print "regular"


        ### set other colors or pic ###
        self.enemy_t[self.counter_enemies].penup()
        self.enemy_t[self.counter_enemies].goto(x, y)

    ## defines enemies' according existance, limits, and coliisions
    def manage_enemies(self, player_down_limit, player, isCollision, ball_is_moving, level):

        for i in range(self.counter_enemies+1):
            # if there is no enemy in this cell
            if self.enemy_list[i] != 1:
                continue
            else:
                if ball_is_moving:
                    self.move_enemy(i, player, isCollision, level)
            if self.enemy_can_fire:
               self.move_enemy_fire(player,isCollision, i)

            ### collison enemy and Paddle
            if isCollision(self.enemy_t[i], player):
                self.clear_enemy(i)
                self.enemy_collide_player = True
            else:
                self.enemy_collide_player = False
                self.check_limits(i, player_down_limit)

    ## check limits of the enemy
    # if it's too down, remove it
    def check_limits(self, i, player_down_limit):
        if self.enemy_t[i].ycor() < player_down_limit:
            self.clear_enemy(i)

    ##clear enemy img, and update the list and num of enemies
    def clear_enemy(self, i):
        self.enemy_t[i].hideturtle()
        self.enemy_list[i] = 0
        self.num_of_enemies -= 1


    ## defines enemies' behavior while moving
    # smart enemy looks for the paddle, regular just go down
    # if player can fire, checks bullet coliision with enemy
    # if collision - kill enemy, and remove bullet object (in controller)
    def move_enemy(self,i, player_position,isCollision, level):

        if level >=4:
            if i != 0 and (i % 2 == 0 or i % 5 == 0):
                self.move_smart_enemies(i, player_position, isCollision, level)
            ## regular enemy
            else:
                self.enemy_t[i].sety(self.enemy_t[i].ycor() - 8)

        else:
            self.enemy_t[i].sety(self.enemy_t[i].ycor() - 8)


        if self.player_can_fire:
            ### collison enemy and bullet
            if isCollision(self.enemy_t[i], self.current_bullet):
                self.clear_enemy(i)
                self.enemy_collide_bullet = True


    def move_smart_enemies(self, i ,player_position, isCollision, level):
        ## smart enemies
        if i % 5 == 0 and level >=5:
            if self.enemy_t[i].ycor() >= 0:
                self.enemy_t[i].sety(self.enemy_t[i].ycor() - 2)
            else:
                if not self.enemy_fire_is_moving and self.enemy_list[i] != 0:
                    self.create_enemy_fire(i)
                #want_fire = random.randint(1,3)
                #print want_fire
                #if want_fire ==1 or want_fire == 3:
        else:
            self.enemy_t[i].sety(self.enemy_t[i].ycor() - 2)

        distance = player_position.xcor() - self.enemy_t[i].xcor()
        if distance != 0:
            if player_position.xcor() < self.enemy_t[i].xcor():
                self.enemy_t[i].setx(self.enemy_t[i].xcor() - 2)
            else:
                self.enemy_t[i].setx(self.enemy_t[i].xcor() + 2)


    def create_enemy_fire(self,i):
        self.enemy_fire.shape('pics/fire.gif')
        self.enemy_fire.penup()
        self.enemy_fire.setx(self.enemy_t[i].xcor())
        self.enemy_fire.sety(self.enemy_t[i].ycor())
        self.enemy_fire.showturtle()
        self.enemy_can_fire = True
        self.enemy_fire_is_moving = True


    def move_enemy_fire(self, player_position, isCollision,i):

        self.enemy_fire.sety(self.enemy_fire.ycor()-2)
        ## if the enemy_fire collided with player
        if isCollision(self.enemy_fire, player_position):
            self.clear_enemy_fire(player_position)
            self.enemy_collide_player = True

        if self.enemy_fire.ycor() < player_position.ycor() - 50 or self.enemy_list[i] != 1:
            self.clear_enemy_fire(player_position)
            self.enemy_can_fire = False
            self.enemy_fire_is_moving = False


    def clear_enemy_fire(self,player_position):
        self.enemy_fire.sety(player_position.ycor() - 100)
        self.enemy_fire.hideturtle()











    ## defines the enemy and bullets state collision
    #get the bullet from controlller, and check collision with enemy
    def enemy_bullet(self, bullet):
        self.current_bullet = bullet
        self.player_can_fire = True
        if self.enemy_collide_bullet:
            self.enemy_collide_bullet = False
            return True

















