# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
score1 = 0
score2 = 0
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0 
paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    ball_vel[0] = random.randrange(120, 240)//30
    ball_vel[1] = random.randrange(60, 180)//30
    if direction:
        ball_vel[1] = -ball_vel[1]
    else:
        ball_vel[0] = -ball_vel[0]
        ball_vel[1] = -ball_vel[1]
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos
    paddle1_pos = HEIGHT/2
    paddle1_pos = HEIGHT/2
    # generate a random direction
    if random.random() < 0.5:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)      
            
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]    
    ball_pos[1] += ball_vel[1] 
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    # make sure that the paddles don't move if they reach the vertical ends
    if paddle1_pos < PAD_HEIGHT/2:
        paddle1_pos = PAD_HEIGHT/2
    elif paddle1_pos > HEIGHT - PAD_HEIGHT/2:
        paddle1_pos = HEIGHT - PAD_HEIGHT/2
        
    if paddle2_pos < PAD_HEIGHT/2:
        paddle2_pos = PAD_HEIGHT/2
    elif paddle2_pos > HEIGHT - PAD_HEIGHT/2:
        paddle2_pos = HEIGHT - PAD_HEIGHT/2
    
    
    # draw paddles
    canvas.draw_line([0, paddle1_pos + HALF_PAD_HEIGHT],[0, paddle1_pos - HALF_PAD_HEIGHT],
                     PAD_WIDTH*2, "White")
    canvas.draw_line([WIDTH, paddle2_pos + HALF_PAD_HEIGHT],[WIDTH, paddle2_pos - HALF_PAD_HEIGHT],
                     PAD_WIDTH*2, "White")
    
    # determine whether paddle and ball collide 
    ## specify the ball collision course
    # check if ball hits left paddle
    if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT and ball_pos[0] <= BALL_RADIUS:
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
    elif paddle2_pos - HALF_PAD_HEIGHT < ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT and ball_pos[0] + BALL_RADIUS >= WIDTH:
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
    elif ball_pos[0] <= BALL_RADIUS:
        score2 += 1
        new_game()    
    elif ball_pos[0] + BALL_RADIUS > WIDTH:
        score1 += 1
        new_game()
    # make sure that ball bounces of the top and bottom
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] + BALL_RADIUS > HEIGHT:
        ball_vel[1] = -ball_vel[1]
        
        
    # draw scores
    canvas.draw_text(str(score1), [WIDTH / 2 - 50, 100], 25, "White") 
    canvas.draw_text(str(score2), [WIDTH / 2 + 50, 100], 25, "White")         
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 6
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc 
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    elif key==simplegui.KEY_MAP["S"]:
        paddle1_vel += acc
    elif key==simplegui.KEY_MAP["W"]:
        paddle1_vel -= acc
    
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["W"] or key==simplegui.KEY_MAP["S"]:
        paddle1_vel = 0
    else: paddle2_vel = 0
    
def restart():
    global score1, score2 
    score1 = 0
    score2 = 0
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart, 100)


# start frame
new_game()
frame.start()
