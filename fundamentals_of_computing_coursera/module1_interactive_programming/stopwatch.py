# template for "Stopwatch: The Game"

import simplegui
import time

# define global variables
current_time = 0
rounds = 0
score = 0
watch_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global current_time
    ms = current_time % 10	 
    seconds = ((current_time - ms)/10) % 60
    # append a leading 0 to seconds if it is smaller than 10
    if seconds < 10:
        seconds = str(0) + str(seconds)
    
    
    minutes = ((current_time - ms)/10) / 60
    time = str(minutes)+":"+str(seconds)+"."+str(ms)
    return time
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global watch_running
    timer.start()
    watch_running = True

def stop():
    global rounds, score, current_time, watch_running
    timer.stop()
    if watch_running:
        rounds += 1
        if current_time%10 == 0:
            score += 1
    watch_running = False
    
def reset():
    stop()
    global current_time, score, rounds, watch_running
    current_time = 0
    score = 0
    rounds = 0
    watch_running = False
    
# define event handler for timer with 0.1 sec interval
def increment_time():
    global current_time
    current_time += 1
    return current_time

# define draw handler
def draw(canvas):
    global current_time, score
    canvas.draw_text(format(current_time),[120, 150], 30, "White")
    canvas.draw_text(str(score)+"/"+str(rounds),[250, 50], 24, "Green")
    
# create frame
frame = simplegui.create_frame('Timer game', 300, 300)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, increment_time)


# start frame
frame.start()


# Please remember to review the grading rubric