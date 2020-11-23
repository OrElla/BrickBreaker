import turtle

class Bricks:

    Bricks_list,Brick_Board  = [], []
    level_Bricks = [44, 36, 36, 71, 65, 65, 65]
    NUM_OF_BRICKS, x, y, start_x_right, x_left_limit = 0, 0, 0, 0, 0

    def __init__(self, value ,Right_Limit, up_limit, Player_move ,Left_Limit ,N):
        self.value = value
        self.Right_Limit = Right_Limit
        self.up_limit = up_limit
        self.Player_move = Player_move
        self.Left_Limit, self.x_left_limit = Left_Limit, Left_Limit
        self.N = N
        self.CreateBricks(value)


    def Create_Bricks_list(self, x,y, count, level):

        self.Bricks_list.append([])
        self.Bricks_list[count].append(count)
        self.Bricks_list[count].append(x)
        self.Bricks_list[count].append(y)

        if level < 3 or level >5:
            self.Bricks_list[count].append(self.value)
        else:
            self.Bricks_list[count].append(2)



    def create_rectangle(self, obj):
        for i in range(4):
            if i % 2 == 0:
                obj.backward(self.Player_move)
            else:
                obj.backward(self.Player_move / 2)
            obj.left(90)

    ## value  = level -> value of any brick is equal to the level
    def CreateBricks(self, value):
        self.value = value
        self.x = self.Right_Limit
        self.y = self.up_limit
        self.start_x_right = self.x
        self.Left_Limit = self.x_left_limit
        # start_y = y
        count = 0

        self.NUM_OF_BRICKS = self.level_Bricks[value-1]

        if self.value == 3:
            self.y = 2* self.Player_move - self.N


        while (count < self.NUM_OF_BRICKS):

            self.StartCreateBrick(count, self.x, self.y)
            self.x -= self.Player_move

            self.Create_Bricks_list(self.x, self.y, count, self.value)
            self.create_rectangle(self.Brick_Board[count])
            self.EndCreateBrick(count)

            if self.x < self.Left_Limit:
                self.manage_bricks_by_level(self.value, count)
                if self.value ==3:
                    if self.y > (self.up_limit):
                        break
                else:
                    #if self.y <= -(self.Player_move * self.NUM_OF_BRICKS % self.N):
                    if self.y <= -2*self.Player_move:
                        if count <= self.NUM_OF_BRICKS:
                            print "level = " , self.value
                            print "count = ", count
                            continue
                        else:
                             break
            count += 1



    def manage_bricks_by_level(self,level, count):
        if level == 1:
            self.x = self.start_x_right
            self.y -= self.Player_move / 2
            self.Brick_Board[count].penup()

        ## regular triangle
        elif level == 2:
            self.Left_Limit += self.Player_move
            self.x = self.start_x_right - self.Player_move
            self.start_x_right = self.x
            self.y -= self.Player_move / 2
            self.Brick_Board[count].penup()

        ## opp triangle
        elif level == 3:
            self.Left_Limit += self.Player_move
            self.x = self.start_x_right - self.Player_move
            self.start_x_right = self.x
            self.y += self.Player_move / 2
            self.Brick_Board[count].penup()


        ## combined triangle
        elif level == 4:
            if count <= self.NUM_OF_BRICKS/2-1:
                self.Left_Limit += self.Player_move
                self.x = self.start_x_right - self.Player_move

            if count >= self.NUM_OF_BRICKS/2:
                self.Left_Limit -= self.Player_move
                self.x = self.start_x_right + self.Player_move

            self.start_x_right = self.x
            self.y -= self.Player_move / 2
            self.Brick_Board[count].penup()
        ## left hugh trianle
        else:
            # self.Left_Limit += self.Player_move
            self.x = self.start_x_right - self.Player_move
            self.start_x_right = self.x
            self.y -= self.Player_move / 2
            self.Brick_Board[count].penup()

    def StartCreateBrick(self,count,x,y):

        # self.Brick_Board[0].hideturtle()
        self.Brick_Board.append(turtle.Turtle())
        self.Brick_Board[count].hideturtle()
        self.Brick_Board[count].penup()
        self.Brick_Board[count].goto(x, y)
        self.Brick_Board[count].begin_fill()
        self.Brick_Board[count].pendown()

    def EndCreateBrick(self,count):

        self.Brick_Board[count].fillcolor("red")
        self.Brick_Board[count].penup()
        self.Brick_Board[count].end_fill()