# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

num_range = 100
secret_number = 0
guesses_left = 7


# helper function to start and restart the game
def new_game():
    global num_range
    global guesses_left
    
    if num_range == 100:
        guesses_left = 7
    else:
        guesses_left = 10
    
    print "" 
    print "New game. Range is from 0 to " + str(num_range) + "."
    print "You have " + str(guesses_left) + " guesses left."
    
# define event handlers for control panel
def	range100():
    # button that changes the range to [0,1000) and starts a new game 
    global secret_number
    global num_range
    global guesses_left
    guesses_left = 7
    num_range = 100
    secret_number = random.randint(0, 100)
    return new_game()
          
def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global secret_number
    global num_range
    global guesses_left
    guesses_left = 10
    num_range = 1000
    secret_number = random.randint(0, 1000)
    return new_game()
          
def input_guess(guess):
    global guesses_left
    global secret_number
    guess = int(guess)
    guesses_left -= 1
    print ""
    print "Guess was " + str(guess)
    print "Number of remaining guesses is " + str(guesses_left)
    
    if guess == secret_number:
        print 'Correct!'
        new_game()
    elif guesses_left == 0:
        print 'You ran out of guesses. The correct number was ' + str(secret_number)
        new_game()
    elif guess < secret_number:
        print 'Higher!'
    else:
        print 'Lower!'
    
    
# create frame
frame = simplegui.create_frame('Guess the number game', 200, 200)


# register event handlers for control elements and start frame
frame.add_button('Range is in [0, 100)', range100, 200)
frame.add_button('Range is in [0, 1000)', range1000, 200)
frame.add_input('Enter a guess: ', input_guess, 200)

# call new_game 
new_game()

frame.start()
# always remember to check your completed program against the grading rubric
#range100()
#secret_number = 74	
#input_guess("50")
#input_guess("75")
#input_guess("62")
#input_guess("68")
#input_guess("71")
#input_guess("73")
#input_guess("74")



#range1000()
#secret_number = 375	
#input_guess("500")
#input_guess("250")
#input_guess("375")


#range100()
#secret_number = 28	
#input_guess("50")
#input_guess("50")
#input_guess("50")
#input_guess("50")
#input_guess("50")
#input_guess("50")
#input_guess("50")