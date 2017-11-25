# implementation of card game - Memory

import simplegui
import random

turns = 0

# helper function to initialize globals
def new_game():
    # create a list of numbers
    global numbers, state, exposed, turns
    turns = 0
    state = 0
    exposed = [False for n in range(16)]
    numbers = [n for n in range(8)]
    numbers = numbers + numbers
    random.shuffle(numbers)
    label.set_text("Turns = " + str(turns))
    
# define event handlers
def mouseclick(pos):
    global state, exposed, card1_index, card2_index, turns
    
    # get the index from pos width
    index = pos[0]//50
    
    if not exposed[index]:
        exposed[index] = True
        if state == 0:
            card1_index = index
            state = 1
        elif state == 1:
            card2_index = index
            state = 2
        else:
            if numbers[card1_index] != numbers[card2_index]:
                exposed[card1_index], exposed[card2_index] = False, False
            card1_index = index
            state = 1
            turns += 1
            label.set_text("Turns = " + str(turns))
        
    
def reset():
    new_game()
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    num_height = 70
    num_width = 10
    pol_width = 0
    for number in numbers:
        # draw number
        canvas.draw_text(str(number), [num_width, num_height], 60, 'White')
        # draw vertical line
        num_width += 50
    
    for number in exposed:
        # draw rectangles
        canvas.draw_line((pol_width, 0), (pol_width, 100), 1, 'Red')
        if not number:
            canvas.draw_polygon([(pol_width, 0),(pol_width + 50, 0),(pol_width + 50, 100), (pol_width, 100)],
                                                    1, 'Green', 'Green')
        canvas.draw_line((pol_width, 0), (pol_width, 100), 1, 'Black')
        pol_width += 50 

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric