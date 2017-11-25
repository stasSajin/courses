# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [135, 45], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius
        
    # thrust should trigger sound
    def play_thrust(self, thrusting):
        self.thrust = thrusting
        if thrusting:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
        
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
    
        vel_update = 0.30 
        friction = 0.02 # make this close to 0
    
        self.vel[0] *= (1 - friction)
        self.vel[1] *= (1 - friction)
        
        # make the ship move foward when thrust is on
        if self.thrust:
            direction = angle_to_vector(self.angle)
            self.vel[0] += vel_update * direction[0]
            self.vel[1] += vel_update * direction[1]
    
    def increment_angvel(self):
        self.angle_vel += 0.2
        
    def decrement_angvel(self):
        self.angle_vel -= 0.2
    
    def shoot(self):
        global a_missile
        # specify missle direction
        direction = angle_to_vector(self.angle)
        mis_pos = [self.pos[0] + self.radius * direction[0], self.pos[1] + self.radius * direction[1]]
        mis_vel = [self.vel[0] + 5 * direction[0], self.vel[1] + 5 * direction[1]]
        # add the missiles in sequence
        missile_group.add(Sprite(mis_pos, mis_vel, self.angle, 0, missile_image, missile_info, missile_sound))
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            tile = (self.age % 20) // 1
            self.image_center = [self.image_center[0] + tile * self.image_size[0], self.image_center[1]]
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def update(self):
        #angle update
        self.angle += self.angle_vel

        #position + velocity update
        # we're taking the modulo of width and height,
        #so that everything stays in screen
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
    
        
        # create logic to make sure that bullets dissapear
        if self.lifespan:
            if self.age > self.lifespan:
                return True
            else:
                self.age += 1
        return False
 
    def collide(self, obj):
        # this defines the collision logic decribed in the video
        if dist(self.pos, obj.get_position()) < self.radius + obj.get_radius():
            return True
        else:
            return False
    
    
# handler functions
def keydown(key):
    # countercloscwise decrements angular vel
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angvel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angvel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.play_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angvel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angvel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.play_thrust(False)

def click(pos):
    global started, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = 3
        timer.start()
        soundtrack.rewind()
        soundtrack.play()
        

def draw(canvas):
    global time, started, rock_group, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 40, "White")
    canvas.draw_text("Score", [680, 50], 40, "White")
    canvas.draw_text(str(lives), [50, 80], 35, "White")
    canvas.draw_text(str(score), [680, 80], 35, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    
    # draw the groups
    process_sprite_group (rock_group, canvas)
    process_sprite_group (explosion_group, canvas)
    process_sprite_group (missile_group, canvas)
    
    # update ship and sprites
    my_ship.update()
    
    if group_collide(rock_group, my_ship) > 0:
        lives -= 1
    score += group_group_collide(missile_group, rock_group)
    
    # reset the game if lives smaller than 1
    if lives < 1:
        rock_group = set([])
        soundtrack.pause()
        timer.stop()
        started = False
        soundtrack.rewind()
        soundtrack.play()
       
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, my_ship
    rock_pos = [random.randrange (0, WIDTH), random.randrange (0, HEIGHT)]
    rock_vel = [random.random () * .6 - .3, random.random () * .6 - .3]
    rock_avel = random.random () * .2 - .1
    if started and len(rock_group) < 12:
        while dist(rock_pos, my_ship.pos) < 100:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]        
        rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))

def group_collide(group,obj):
    count_collision=0
    for sprite in set(group):
        if sprite.collide(obj):
            explosion_group.add(Sprite(sprite.get_position(), (0, 0), 0, 0, explosion_image, explosion_info, explosion_sound))
            group.remove(sprite)
            count_collision+=1
    return count_collision

def group_group_collide(group, group_two):
    total = 0
    for collide in set(group):
        count = group_collide(group_two, collide)
        if count > 0:
            group.remove(collide)
        total += count
    return total

        
def process_sprite_group(group, canvas):
    removeSet = set([])
    for sprite in group:
        if sprite.update():
            removeSet.add(sprite)
        else:
            sprite.draw(canvas)
    if len(removeSet) > 0:
        group.difference_update(removeSet)

            
        
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])
 

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()