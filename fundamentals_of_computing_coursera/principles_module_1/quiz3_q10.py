# Working Checker for Question 10 of the Homework
# This homework assignment was quite poorly explained but after several hours I was able to build this
# 
# Copy/Paste the incorrect function into the function bad_format()
# make sure you change the parameter to the name the used as sometimes it isn't t

ALL_CASES = range(6000)
TEST_CASES = [0, 10, 11, 60, 100, 103, 670, 599, 600, 700]

BAD_TESTS = []

def bad_format1(t):
    D = (t % 10)
    tenth = (t / 10)
    if ((tenth >= 60) or (tenth <= 9)):
        B = 0
        C = (tenth % 10)
    else:
        B = (tenth / 10)
        C = (tenth % 10)
    A = (t / 600)
    return (((((str(A) + ':') + str(B)) + str(C)) + '.') + str(D))

def bad_format2(run_time):
    global run_time_str, d_run_time
    bc_run_time = (run_time / 10)
    d_run_time = (run_time % 10)
    if (bc_run_time > 59):
        a_run_time = (bc_run_time / 60)
        bc_run_time = (bc_run_time - (60 * a_run_time))
    else:
        a_run_time = 0
    if (bc_run_time > 10):
        str_current_time = ((((str(a_run_time) + ':') + str(bc_run_time)) + '.') + str(d_run_time))
    else:
        str_current_time = (((((str(a_run_time) + ':') + '0') + str(bc_run_time)) + '.') + str(d_run_time))
    return str_current_time

minutes = 0
def bad_format3(t):
    global dot, sec, minutes
    dot = (t % 10)
    if (t < 600):
        sec = (t // 10)
    else:
        sec = ((t % 600) // 10)
        minutes = (t // 600)
    if (sec < 10):
        str_sec = ('0' + str(sec))
    else:
        str_sec = str(sec)
    return ((((str(minutes) + ':') + str_sec) + '.') + str(dot))

def bad_format4(t):
    return ((((str((t / 600)) + ':') + str(((t / 10) % 60))) + '.') + str((t % 10)))


def bad_format5(t):
    if (t <= 9):
        A = '0'
        B = '0'
        C = '0'
    elif (len(str(t)) == 2):
        A = '0'
        B = '0'
        C = (t // 10)
    else:
        A = (t // 600)
        t = (t % 600)
        if (len(str(t)) == 3):
            B = ((t // 10) // 10)
            C = ((t // 10) % 10)
        elif (len(str(t)) < 3):
            if (t <= 59):
                B = '0'
                C = (t // 10)
            else:
                B = (((t % 60) // 10) % 10)
                C = (t // 10)
    D = (t % 10)
    return (((((str(A) + ':') + str(B)) + str(C)) + '.') + str(D))

def bad_format6(t):
    a = (t // 600)
    b = (((t % 600) / 10) / 10)
    c = '0'
    if (t > 10):
        c = str(t)[(-2)]
    d = str(t)[(-1)]
    formatedTime = (((((str(a) + ':') + str(b)) + c) + '.') + d)
    return formatedTime

def good_format(t):
    minutes = str(t // 600)
    secs = str(t % 600)
    while len(secs) < 3:
        secs = "0" + secs
    return minutes + ":" + secs[:-1] + "." + secs[-1]


bad1=[]
bad2=[]
bad3=[]
bad4=[]
bad5=[]
bad6=[]
for i in ALL_CASES:
    good = good_format(i)
    if bad_format1(i) != good:
        bad1.append(i)
    if  bad_format2(i) != good:
        bad2.append(i)
    if  bad_format3(i) != good:
        bad3.append(i)
    if  bad_format4(i) != good:
        bad4.append(i)
    if  bad_format5(i) != good:
        bad5.append(i)
    if  bad_format6(i) != good:
        bad6.append(i)
    
    
        
print bad1
print bad2
print bad3
print bad4
print bad5
print bad6