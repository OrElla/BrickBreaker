#play_again = 0


def play(x,y):
    #global play_again
    #play_again +=1
    #print play_again
    new_board.new_game_titles()
    from Controller import Controller
    gameController = Controller()
    gameController.RunGame()
    #if play_again > 1:
     #   gameController.new_game_player()



def new_game():

    Start_game = True
    if Start_game:
        new_board.window.listen()
        new_board.window.onscreenclick(play)
        Start_game = False
    turtle.done()

if __name__=="__main__":

    from Board import *
    new_board = Board(Window_width, Window_height)
    new_game()


