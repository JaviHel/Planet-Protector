import pygame as pg
import math, random, time
from sys import exit

from vector_math import *
from utility_functions import *
from font import *

SZ = 2.4
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
            #### #### #### #### CLASSES #### #### #### ####
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####

class Rock:
    rocks = []
    rock_shape = []
    def __init__(self, pg):
        self.pg = pg
        self.dt = 0
        #### VALUES TO CREATE THE ROCK ####
        self.x, self.y = 0, 0
        self.r = random.randint(int(pg.canvas_size[0]*0.05), int(pg.canvas_size[0]*0.06)) # Initial rock radius
        self.scalar = 1
        self.sides = 5
        self.angle = 0
        #### VALUES TO UPDATE IT'S POSITION ####
        self.cx, self.cy = pg.canvas_size[0]//2, pg.canvas_size[1]//2 # Point to orbit around
        self.orbit_pos = random.randint(-180, 180) # Initial position and angle of the path
        self.orbit_speed = random.choice([-0.1,-0.8,-0.6,-0.4,-0.2, 0.2,0.4,0.6,0.8,0.1])
        self.orbit_rad = random.randint(int(pg.canvas_size[0]*0.30), int(pg.canvas_size[0]*0.6))
        self.center_pull = random.choice([0.02, 0.05, 0.08, 0.1, 0.2]) # Fast=0.08, Normal=0.05, Slow=0.02 
        self.rot_speed = random.randint(1, 10)
        #### STYLE ####
        self.stroke_width = 1
        self.stroke = "" #"saddlebrown"
        self.fill = random.choice(["brown", "saddlebrown", "sienna", "peru", "burlywood",
                                   "rosybrown", "chocolate", "tan", "sandybrown", "maroon"])
        #### FLAGS ####
        self.is_moving = True
        self.is_visible = True

        #### INIT FUNCTIONS ####
        self.shape_id = random.randint(0,9)
        self.create_rock_shape()
        self.coords = self.rock_shape[self.shape_id]

    #### GETTERS ####
    def get_pos(self, adjust_radius=1):
        return (self.x, self.y, (self.r*self.scalar)*adjust_radius)
    def get_radius(self, adjust_rad=1):
        return self.r*adjust_rad
    def get_scalar(self):
        return self.scalar
    def get_fill(self):
        return self.fill
    def get_orbit_pos(self):
        return self.orbit_pos
    def get_orbit_rad(self):
        return self.orbit_rad
    def get_orbit_speed(self):
        return self.orbit_speed
    def get_rot_speed(self):
        return self.rot_speed
    def get_center_pull(self):
        return self.center_pull
    def get_style(self):
        return(f"fill: {self.fill}, stroke: {self.stroke}")
    
    #### SETTERS ####
    def set_pos(self, x, y):
        self.x, selfy = x, y
    def set_scalar(self, scalar=None):
        self.scalar = scalar
    def set_fill(self, fill=None):
        self.fill = fill
    def set_orbit_pos(self, orbit_pos=None):
        self.orbit_pos = orbit_pos
    def set_orbit_rad(self, orbit_rad=None):
        self.orbit_rad = orbit_rad
    def set_orbit_speed(self, orbit_speed=None):
        self.orbit_speed = orbit_speed
    def set_rot_speed(self, rot_speed=None):
        self.rot_speed = rot_speed
    def set_center_pull(self, center_pull=None):
        self.center_pull = center_pull
    def set_shape(self, shape=random.randint(0, 9)):
        self.shape_id = shape
    def set_style(self, fill=None, stroke=None):
        self.fill, self.stroke = fill, stroke
    def set_stroke_width(self, width=None):
        self.stroke_width = width
    def set_is_moving(self, is_moving=None):
        self.is_moving = is_moving
    def set_is_visible(self, is_visible=None):
        self.is_visible = is_visible

    #### #### #### ####
    def create_rock_shape(self):
        if self.rock_shape == []: # The Original created infinite amount of rocks
            for i in range(10):
                self.append_rock_shape()

    def append_rock_shape(self):
        coordinates = []
        full_circle = 360
        while self.angle <= full_circle:
            dx = math.cos(math.radians(self.angle)) * self.r
            dy = math.sin(math.radians(self.angle)) * self.r
            self.angle += full_circle//random.randint(self.sides, int(self.sides*2))
            coordinates.append([dx, dy])
        self.angle = 0
        if coordinates != []: self.rock_shape.append(coordinates)
        return coordinates

    #### VECTOR OPERATIONS ####
    def add_vec(self, coords, npos):
        """ Add vectors to update the position of the object.
            coords is a list of vectors """
        new_coords = []
        for c in coords:
            nc = [c[0] + npos[0],
                  c[1] + npos[1]]
            new_coords.append(nc)
        return new_coords

    def rotate(self, coords, theta):
        """ coords is a list of vector coordinates.
            theta is the angle of rotation """
        cos_theta = math.cos(math.radians(theta))
        sin_theta = math.sin(math.radians(theta))

        new_c = []
        for i, v in enumerate(coords):
            nc = [v[0] * cos_theta + v[1] * -sin_theta,
                  v[1] * cos_theta + v[0] * sin_theta]
            new_c.append(nc)
        return new_c

    def scale(self, coords, scalar):
        """ Changes the size of the rock.
            coords is a list of vector coordinates """
        new_c = []
        for i, v in enumerate(coords):
            nc = [v[0] * scalar,
                  v[1] * scalar]
            new_c.append(nc)
        return new_c
    
    #### DRAWING METHODS ####

    def outside(self):
        """ If rock is outside of the screen dont draw it """
        if (int(self.x+self.r) < 0 or int(self.x-self.r) > pg.canvas_size[0] or
            int(self.y+self.r) < 0 or int(self.y-self.r) > pg.canvas_size[1]):
            self.is_visible = False
        else:
            self.is_visible = True

    def move(self):
        """ Updates the position x,y of the object """
        self.orbit_pos += self.orbit_speed*self.dt
        self.orbit_rad -= self.center_pull*self.dt
        self.x = self.cx + math.cos(math.radians(self.orbit_pos)) * self.orbit_rad
        self.y = self.cy + math.sin(math.radians(self.orbit_pos)) * self.orbit_rad        

    def kill(self):
        """ Removes rock from the list """
        self.rocks.remove(self)

    #### UPDATE METHODS ####

    def draw(self, canvas):
        """ Displays the object on the screen with the updated values """
        coords = self.add_vec(self.rotate(self.scale(self.rock_shape[self.shape_id], self.scalar), self.orbit_pos*self.rot_speed), [self.x, self.y])
        if self.fill != "": pg.draw.polygon(canvas, self.fill, coords)
        if self.stroke != "": pg.draw.polygon(canvas, self.stroke, coords, self.stroke_width)

    def update(self, canvas, dt):
        """ Call all the methods that needs constant updates """
        self.dt = dt
        if self.is_moving:  self.move(); self.outside()
        if self.is_visible: self.draw(canvas)




class Spaceship:
    """ PARENT CLASS TO CREATE REGULAR POLYGONS AND ANIMATE THEM """
    def __init__(self, pg, x, y, r, sides):
        self.pg = pg
        self.dt = None
        (self.x, self.y) = (x, y)
        (self.r, self.sides) = (r, sides)
        (self.angle, self.rot) = (0, random.randint(-180, 180))
        self.speed = 0.4 # Initial speed
        self.speed_range = 0.2
        self.steer_range = 1.4
        self.steer = self.speed + self.steer_range
        self.bullet_speed = 2.5
        self.bullet_rounds = 4
        # Style
        self.fill = ""
        self.stroke = "white"
        self.stroke_width = 1
        self.tag = ""
        # Joystick-Controller - Each new class has to have different values
        self.stick = [pg.K_w, pg.K_a, pg.K_s, pg.K_d]
        self.actkey = [pg.K_j, pg.K_k, pg.K_l]
        # Flags
        self.is_moving = True
        self.is_visible = True
        self.is_turning = False
        self.sfx = True
        # SoundFX
        self.shootfx = pg.mixer.Sound("sfx/shoot-short.wav")
        self.shootfx.set_volume(0.4)

    #### GETTERS AND SETTERS ####
    def get_pos(self, adjust_rad=1):
        """ Returns x, y, r but with a adjustable radius parameter,
            used to calculate the inner circle for collisions """
        return (self.x, self.y, self.r*adjust_rad)
    def get_radius(self):
        return self.r
    def get_angle(self):
        return self.rot
    def get_id(self):
        return self.id
    def get_tag(self):
        return self.tag
    def get_buttons(self):
        return (f"Stick: {self.stick}, ActionKeys: {self.actkey}")
    def get_style(self):
        return (self.fill, self.stroke)
    def get_is_moving(self):
        return self.is_moving
    def get_is_visible(self):
        return self.is_moving
    def get_bullet_speed(self):
        return self.bullet_speed
        
    def set_pos(self, x, y):
        (self.x, self.y) = (x, y)
    def set_radius(self, r):
        self.r = r
    def set_sides(self, sides):
        self.sides = sides
    def set_angle(self, angle):
        self.rot = angle
    def set_speed(self, speed):
        self.speed = speed
    def set_steer(self, steer):
        self.steer = steer
    def set_style(self, fill="", stroke=""):
        (self.fill, self.stroke) = (fill, stroke)
    def set_tag(self, tag):
        self.tag = tag
    def set_buttons(self, stick=[], actkey=[]):
        """ STICK: Up, Down, Left, Right
            ACTIONKEY: Any 3 Other Buttons """
        if len(stick) != 4 or len(stick) == []:
            raise ValueError("Stick needs 4 parameters")
        elif len(actkey) != 3 or len(actkey) == []:
            raise ValueError("ActionKeys needs 3 parameters")
        else:
            (self.stick, self.actkey) = (stick, actkey)

    def set_is_moving(self, is_moving=None):
        self.is_moving = is_moving
    def set_is_visible(self, is_visible=None):
        self.is_visible = is_visible
    def set_is_turning(self, is_turning=None):
        self.is_turning = is_turning
    def set_bullet_rounds(self, rounds=0):
        self.bullet_rounds = rounds
    def set_bullet_speed(self, bullet_speed=None):
        self.bullet_speed = bullet_speed
        
        
    ##### BUTTONS HANDLER METHODS #####

    def accelerate(self, k):
        """ This should be automated by the score/points """
        if k == self.stick[0] and self.is_moving:
            self.speed += (self.speed_range * self.dt)
            self.set_steer(self.speed + self.steer_range)

    def brake(self, k):
        """ Tends the value of the speed to zero """
        if k == self.actkey[1] or k == self.stick[2]:
            if self.speed >= 0.4:    self.set_speed(self.speed - self.speed_range)

    def turn(self, k):
        """ Checks Keyboard inputs """
        if k == self.stick[1] and self.is_moving:
            self.is_turning = "L"
        elif k == self.stick[3] and self.is_moving:
            self.is_turning = "R"

    def turning(self):
        """ Constant updated method to turn the spaceship """            
        if self.is_turning == "L" and self.is_moving:
            self.rot -= self.steer * self.dt
        elif self.is_turning == "R" and self.is_moving:
            self.rot += self.steer * self.dt

    def shoot(self, k):
        """ Adds a bullet to the bullets list """
        if (k == self.actkey[0] and len(Bullet.bullets) < self.bullet_rounds):
            b = Bullet(pg, self.x, self.y, self.rot, speed=self.bullet_speed, fill=self.stroke)
            Bullet.bullets.append(b)
            if self.sfx:
                sfxlen = random.randint(250, 1000)
                self.shootfx.play(maxtime=sfxlen)

    def relocate(self, k):
        """ Relocate to a new random position, only if player is outside of the arena """
        if k == self.actkey[2]:
            if (self.x < 0 or self.x > pg.canvas_size[0] or
                self.y < 0 or self.y > pg.canvas_size[1]):
                self.respawn()

    def respawn(self):
        """ Respawn killed player in a random position """
        CW, CH = pg.canvas_size
        rand_angle = random.randint(0, 360)
        self.set_pos(CW//2, CH//2)
        self.set_angle(rand_angle)
    
    def collide_walls(self):
        """ Stops the object when colliding with the wall """
        collision_side = {"left":False, "right":False, "top":False, "bottom":False}

        if self.x < 0+self.r:
            collision_side["left"] = True
        elif self.x > pg.canvas_size[0]-self.r:
            collision_side["right"] = True
        if self.y < 0+self.r:
            collision_side["top"] = True
        elif self.y > pg.canvas_size[1]-self.r:
            collision_side["bottom"] = True

        if collision_side["left"]:
            self.x = 0+self.r
        elif collision_side["right"]:
            self.x = pg.canvas_size[0]-self.r
        if collision_side["top"]:
            self.y = 0+self.r
        elif collision_side["bottom"]:
            self.y = pg.canvas_size[1]-self.r

    def move(self):
        """ Updates the object attributes values """
        self.speed * self.dt
        self.x += self.speed * math.cos(math.radians(self.angle+self.rot))
        self.y += self.speed * math.sin(math.radians(self.angle+self.rot))

    #### UPDATE METHODS ####
 
    def create_coords(self):
        """ Returns the coordinates to create a regular polygon shape """
        coords = [[self.x, self.y]]
        for angle in range(0, 365, 360//self.sides):
            new_x = self.x + math.cos(math.radians(angle+self.rot)) * self.r
            new_y = self.y + math.sin(math.radians(angle+self.rot)) * self.r
            coords.append([new_x, new_y])
        return coords

    def draw(self, screen):
        if self.fill != "": self.pg.draw.polygon(screen, self.fill, self.create_coords())
        if self.stroke != "": self.pg.draw.polygon(screen, self.stroke, self.create_coords(), width=self.stroke_width)        

    def update(self, screen, dt):
        self.dt = dt
        if self.is_visible: self.draw(screen)
        if self.is_turning: self.turning()
        if self.is_moving: self.move()
##        self.collide_walls() # Should only check this if the player is at a certain distance

        



class Bullet:
    bullets = []
    def __init__(self, pg, x, y, angle, speed=2.5, fill="white", stroke=""):
        self.pg = pg
        self.x, self.y = x, y
        self.radius = 2
        self.angle = angle
        self.speed = speed
        self.dt = 0
        # Style
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = 1
        # Flags
        self.is_visible = True 
        self.is_moving = True

    def get_pos(self, adjust_radius=1):
        return (self.x, self.y, self.radius*adjust_radius)
    def get_radius(self, adjust_radius=1):
        return self.radius*adjust_radius
    def get_speed(self):
        return self.speed
    def get_tag(self):
        return self.tag
    def get_is_shooting(self):
        return self.is_shooting
    def get_is_visible(self):
        return self.is_visible
    def get_is_moving(self):
        return self.is_moving
    
    def set_pos(self, x=None, y=None):
        self.x, self.y = x, y
    def set_angle(self, angle=None):
        self.angle = angle
    def set_speed(self, speed=None):
        self.speed = speed
    def set_is_shooting(self, is_shooting=None):
        self.is_shooting = is_shooting
    def set_is_visible(self, is_visible=None):
        self.is_visible = is_visible
    def set_is_moving(self, is_moving=None):
        self.is_moving = is_moving

    def outside(self):
        """ Hide the bullet when is outside of the screen """
        if (self.x+self.radius < 0 or self.x > self.pg.canvas_size[0]+self.radius or
            self.y+self.radius < 0 or self.y > self.pg.canvas_size[1]+self.radius):
            self.kill()
            
    def kill(self):
        self.bullets.remove(self)

    def move(self):
        self.speed * self.dt
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

    def draw(self, screen):
        if self.fill != "": self.pg.draw.circle(screen, self.fill, [self.x, self.y], self.radius)
        if self.stroke != "": self.pg.draw.circle(screen, self.stroke, [self.x, self.y], self.radius, width=self.stroke_width)

    def update(self, screen, dt):
        self.dt = dt
        if self.is_visible: self.draw(screen)
        if self.is_moving: self.move(); self.outside()





class RocksHandler:
    """ Handles the creation of the rocks """
    def __init__(self):
        self.max_rocks = 100
        self.old_len = len(Rock.rocks)
        self.is_creating = True

    def get_max_rocks(self):
        return self.max_rocks
    def get_old_len(self):
        return self.old_len
    def get_is_creating(self):
        return self.is_creating

    def set_old_len(self, current_len=None):
        self.old_len = current_len
    def set_is_creating(self, is_creating=None):
        self.is_creating = is_creating
    
    def add_rocks(self, num_of_rocks):
        """ Creates the initial number of rocks """
        for i in range(num_of_rocks):
            r = Rock(pg)
            Rock.rocks.append(r)
        self.set_old_len(len(Rock.rocks))     
            
    def add_new_rocks(self, current_len):
        """ Creates Rocks for every kill
            until it reaches 100 """
        if current_len <= self.old_len and self.is_creating:
            # Random creation of rocks
            rndm = random.random()
            if rndm >= 0.6:
                Rock.rocks.append(Rock(pg))
                Rock.rocks.append(Rock(pg))
                Rock.rocks.append(Rock(pg))
                Rock.rocks.append(Rock(pg))
            else:
                Rock.rocks.append(Rock(pg))
                Rock.rocks.append(Rock(pg))              
            
            self.old_len = current_len
            
        elif current_len >= self.max_rocks:
            self.is_creating = False
            self.old_len = current_len




class Planet:
    LIFES = 2
    def __init__(self, x, y):
        self.imgs = [pg.image.load(f"imgs/earth_0{i}.png") for i in  range(4)]
        self.img_id = 0
        self.x, self.y = x, y
        self.r = self.imgs[self.img_id].get_width()//2
        self.is_visible = True
##        self.sfx = True

    def get_pos(self, adj_rad=1):
        return [self.x, self.y, self.r*adj_rad]
    def get_img_id(self):
        return self.img_id
    def get_is_visible(self):
        return self.is_visible
    def get_sfx(self):
        return self.sfx

    def set_img_id(self, img_id=0):
        self.img_id = img_id
    def set_is_visible(self, is_visible=None):
        self.is_visible = is_visible
    def set_sfx(self, sfx=None):
        self.sfx = sfx

    def draw(self, canvas):
        if self.is_visible:
            canvas.blit(self.imgs[self.img_id], (self.x-16, self.y-16))


    

class Player(Spaceship):
    SCORE = 0
    HI_SCORE = int(score_to_txt(mode="r"))
    LIFES = 4
    def __init__(self, pg, x, y, r, sides):
        super().__init__(pg, x, y, r, sides)
        self.set_style("grey30", "lightgrey")



class Circle:
    """ Color Picker Circles """
    def __init__(self, pos):
        self.pos = pos
        self.rad = 8
        self.fill = ""
        self.stroke = ""

    def get_pos(self):
        return (self.pos[0], self.pos[1], self.rad)
    def get_style(self):
        return (self.fill, self.stroke)

    def set_style(self, fill="", stroke=""):
        self.fill, self.stroke = fill, stroke

    def draw(self, canvas):
        pg.draw.circle(canvas, self.fill, self.pos, self.rad)
        pg.draw.circle(canvas, self.stroke, self.pos, self.rad, width=1)



class StateMachine:
    """ Parent class to control the states of the game """
    def __init__(self, game):
        self.game = game # Passes the game instance to have access to the Game class
        self.rad = 16

        self.tri_pos = [80, 120]
        self.triangle = Spaceship(pg, self.tri_pos[0], self.tri_pos[1], self.rad, sides=3)
        self.triangle.set_style(self.game.p1.get_style()[0], self.game.p1.get_style()[1])
        self.triangle.set_is_moving(False)
        
        self.pent_pos = [240, 120]
        self.pentagon = Spaceship(pg, self.pent_pos[0], self.pent_pos[1], self.rad, sides=5)
        self.pentagon.set_style(self.game.p1.get_style()[0], self.game.p1.get_style()[1])
        self.pentagon.set_is_moving(False)
        
        self.font = pg.font.SysFont("impact", size=20, bold=False, italic=False)
        self.pause_font = pg.font.SysFont("impact", size=32)
        self.text_color = "lightgrey"
        
        self.pos = [50, 54]
        self.color_picker_circles = [Circle([self.pos[0]*i+36, self.pos[1]]) for i in range(6)]
        self.fill_color = ["grey30", "red4", "darkgreen", "darkgoldenrod4", "blue4", "darkorange4"]
        self.stroke_color = ["lightgrey", "orangered", "green", "yellow", "lightslateblue", "orange"]
        [self.color_picker_circles[i].set_style(self.fill_color[i], self.stroke_color[i]) for i in range(len(self.color_picker_circles))]       

        pg.mixer.music.load("music/song 1.ogg")
        pg.mixer.music.set_volume(0.90)

    def stick_kd(self, kd):
        pass



class MainScreen(StateMachine):
    """ MAIN GAME SCREEN """
    
    def stick_kd(self, kd):
        """ Go To StartGame """
        if kd == pg.K_RETURN:
            self.game.set_state("StartGame")
            pg.mixer.music.play(loops=-1)
    
    def update(self, canvas, dt):
        pg.mouse.set_visible(True)
        pg.mouse.set_cursor(3)
        mx, my, mrad = pg.mouse.get_pos()[0]//SZ, pg.mouse.get_pos()[1]//SZ, 1
        # Render Top Text
        self.text = self.font.render("CHOOSE SPACESHIP!!", True, f"{self.text_color}")
        self.text_rect = self.text.get_rect(center=(160, 12))
        canvas.blit(self.text, self.text_rect)

        # Show Hi_Score
        self.hi_score_txt = self.font.render("HI-SCORE", True, f"{self.text_color}")
        self.hi_score_rect = self.hi_score_txt.get_rect(center=(160, 200))
        canvas.blit(self.hi_score_txt, self.hi_score_rect)
        self.game.scoreboard.render(self.game.canvas, f"{format(Player.HI_SCORE)}", (116, 215))

        # Rotate Spaceships
        self.triangle.update(canvas, dt)
        self.triangle.set_angle(self.triangle.get_angle()+2)
        self.pentagon.update(canvas, dt)
        self.pentagon.set_angle(self.pentagon.get_angle()-2)

        # Choose Spaceship Shape
        if circle_circle(self.triangle.get_pos(), [mx, my, mrad]) and pg.mouse.get_pressed()[0]:
            self.game.set_shape(3)
            self.game.p1.set_style(self.triangle.get_style()[0], self.triangle.get_style()[1])
            self.game.set_state("StartGame")
            pg.mixer.music.play(loops=-1)
        elif circle_circle(self.pentagon.get_pos(), [mx, my, mrad]) and pg.mouse.get_pressed()[0]:
            self.game.set_shape(5)
            self.game.p1.set_style(self.pentagon.get_style()[0], self.pentagon.get_style()[1])
            self.game.set_state("StartGame")
            pg.mixer.music.play(loops=-1)

        # Color Picker
        [circle.draw(canvas) for circle in self.color_picker_circles]
        for c in self.color_picker_circles:
            if circle_circle(c.get_pos(), [mx, my, mrad]) and pg.mouse.get_pressed()[0]:
                self.text_color = c.get_style()[1]
                self.triangle.set_style(c.get_style()[0], c.get_style()[1])
                self.pentagon.set_style(c.get_style()[0], c.get_style()[1])
                self.game.p1.set_style(c.get_style()[0], c.get_style()[1])
                self.game.p1_color = c.get_style()
                self.game.set_font_color(c.get_style()[1])


    
class StartGame(StateMachine):
    """ START GAME OR PLAYING SCREEN """
    
    def stick_kd(self, kd):
        """ Go To PauseGame """
        if kd == pg.K_RETURN:
            self.game.set_state("PauseGame")
            [b.set_is_moving(False) for b in Bullet.bullets if Bullet.bullets != []]        
            [r.set_is_moving(False) for r in Rock.rocks if Rock.rocks != []]
            self.game.p1.set_is_moving(False)
            pg.mixer.music.pause()
            
    def update(self, canvas, dt):
        self.game.set_joystick(True)
        pg.mouse.set_visible(False)
        # Scoreboard
        self.game.scoreboard.render(self.game.canvas, f"{format(Player.SCORE)}", (64, 5))
        self.game.player_life.render(self.game.canvas, f"{Player.LIFES}", (230, 5))
        self.game.planet_life.render(self.game.canvas, f"{Planet.LIFES}", (260, 5))
        # Start Game
        self.game.planet.draw(canvas)
        self.game.p1.update(canvas, dt)
        [b.update(canvas, dt) for b in Bullet.bullets if Bullet.bullets != []]
        [r.update(canvas, dt) for r in Rock.rocks if Rock.rocks != []]
        self.game.collictor(self.game.p1, Rock.rocks, self.game.p1_collide_rock, adj_rad1=0.9)
        self.game.collictor(self.game.planet, Rock.rocks, self.game.rock_collide_planet, adj_rad1=0.98)
        [self.game.collictor(b, Rock.rocks, self.game.bullet_collide_rock, adj_rad2=0.95) for b in Bullet.bullets if Bullet.bullets != []]



class PauseGame(StateMachine):
    """ PAUSE THE GAME """
    
    def stick_kd(self, kd):
        """ Return To StartGame """
        if kd == pg.K_RETURN:
            self.game.set_state("StartGame")
            [b.set_is_moving(True) for b in Bullet.bullets if Bullet.bullets != []]        
            [r.set_is_moving(True) for r in Rock.rocks if Rock.rocks != []]
            self.game.p1.set_is_moving(True)
            pg.mixer.music.unpause()

    def update(self, canvas, dt):
        self.game.set_joystick(False)
        pg.mouse.set_visible(True)
        # Scoreboard
        self.game.scoreboard.render(self.game.canvas, f"{format(Player.SCORE)}", (64, 5))
        self.game.player_life.render(self.game.canvas, f"{Player.LIFES}", (230, 5))
        self.game.planet_life.render(self.game.canvas, f"{Planet.LIFES}", (260, 5))
        # Start Game
        self.game.planet.draw(canvas)
        self.game.p1.update(canvas, dt)
        [b.update(canvas, dt) for b in Bullet.bullets if Bullet.bullets != []]
        [r.update(canvas, dt) for r in Rock.rocks if Rock.rocks != []]

        # Pause Game Text
        self.text = self.pause_font.render("P A U S E", True, f"{self.game.p1.get_style()[1]}")
        self.text_rect = self.text.get_rect(center=(160, 124))
        canvas.blit(self.text, self.text_rect)



class GameOver(StateMachine):
    """ GAME OVER SCREEN """
    
    def stick_kd(self, kd):
        """ Return To MainScreen """
        if kd == pg.K_RETURN:
            self.game.reset(kd)
            self.game.set_state("MainScreen")
    
    def update(self, canvas, dt):
        # Scoreboard
        self.game.scoreboard.render(self.game.canvas, f"{format(Player.SCORE)}", (64, 5))
        self.game.player_life.render(self.game.canvas, f"{Player.LIFES}", (230, 5))
        self.game.planet_life.render(self.game.canvas, f"{Planet.LIFES}", (260, 5))
        # Start Game
        self.game.planet.draw(canvas)
        self.game.p1.update(canvas, dt)
        [r.update(canvas, dt) for r in Rock.rocks if Rock.rocks != []]
        self.game.set_joystick(False)
        # Stop Music
        pg.mixer.music.stop()
        




class Game:
    """ Class to handle the game """
    def __init__(self, canvas, CS):
        self.canvas = canvas
        self.CS = CS # List
        # Planet handler
        self.planet = Planet((CS[0]//2), (CS[1]//2))
        self.planet.set_img_id(0)
        # Player handler
        self.plyr_shape = random.choice([3, 5]) # 3=Triangle 5=Pentagon
        self.p1 = Player(pg, pg.canvas_size[0]//2, pg.canvas_size[1]//2, 8, self.plyr_shape)
        self.p1_color = self.p1.get_style()
        # Rocks handler
        self.rh = RocksHandler()
        self.rh.add_rocks(10)
        # Sounds & Music
        self.explosionfx = pg.mixer.Sound("sfx/explosion-long.wav")
        self.explosionfx.set_volume(0.6)
        self.bonus_sfx_1 = pg.mixer.Sound("sfx/bonus_sfx_1.wav")
        self.bonus_sfx_1.set_volume(0.25)
        self.bonus_sfx_2 = pg.mixer.Sound("sfx/bonus_sfx_2.wav")
        self.bonus_sfx_2.set_volume(0.25)
        # Font & Text
        self.scoreboard = Font(pg, "font/radio_font.png", f"{self.p1.get_style()[1]}")
        self.player_life = Font(pg, "font/radio_font.png", f"{self.p1.get_style()[1]}")
        self.planet_life = Font(pg, "font/radio_font.png", f"{self.p1.get_style()[1]}")
        # Flags & States
        self.sfx = True
        self.joystick = False
        self.state_machine = {"MainScreen": MainScreen(self), "StartGame": StartGame(self),
                              "PauseGame": PauseGame(self), "GameOver": GameOver(self),}
        self.state = self.state_machine["MainScreen"]
        # Bonus Earnings
        self.bullet_bonus_speed = 1995
        self.player_bonus_life = 2706
        self.planet_bonus_life = 4701

    def set_state(self, new_state):
        self.state = self.state_machine[f"{new_state}"]
    def set_shape(self, shape):
        self.p1 = Player(pg, pg.canvas_size[0]//2, pg.canvas_size[1]//2, 8, shape)
        self.plyr_shape = shape
    def set_joystick(self, joystick=False):
        self.joystick = joystick
    def set_font_color(self, font_color):
        self.scoreboard = Font(pg, "font/radio_font.png", f"{font_color}")
        self.player_life = Font(pg, "font/radio_font.png", f"{font_color}")
        self.planet_life = Font(pg, "font/radio_font.png", f"{font_color}")
        
    def reset(self, kd):
        if kd == pg.K_RETURN:
            Rock.rocks.clear()
            Bullet.bullets.clear()
            Player.LIFES = 5
            Player.SCORE = 0
            Planet.LIFES = 2
            self.p1 = Player(pg, pg.canvas_size[0]//2, pg.canvas_size[1]//2, 8, self.plyr_shape)
            self.p1.set_style(self.p1_color[0], self.p1_color[1])
            self.planet = Planet((self.CS[0]//2), (self.CS[1]//2))
            self.planet.set_img_id(0)
            self.rh.add_rocks(10)
            self.sfx = True

    def animate(self, canvas, dt):
        """ Animation Loop """
        self.state.update(canvas, dt)
      
    def stick_kd(self, kd):
        """ Keyboard Keydown Input (This could be its own class) """
        if self.joystick:
            self.p1.accelerate(kd)
            self.p1.brake(kd)
            self.p1.turn(kd)
            self.p1.shoot(kd)
            self.p1.relocate(kd)

        self.state.stick_kd(kd)

    def stick_ku(self, ku):
        """ Keyboard Keyup Input (This could be its own class) """
        if ku in self.p1.stick:
            self.p1.set_is_turning(False)           

    def collictor(self, el, rocks, command, adj_rad1=1, adj_rad2=1):
        """ Collision Detector (This Could be its own class)
            "el" is an instance of a class to check collision with.
            The "command" function returns the collided elements
            as arguments """
        List1 = rocks.copy()
        List1_len = len(List1)
        List1_50 = int(List1_len*0.50)
        
        """ A simple Algorithm to find the objects faster """
        for i in range(0, List1_len, 2):
            if i >= 0 or i <= List1_len:
                if circle_circle(List1[(List1_50)-i].get_pos(adj_rad2), el.get_pos(adj_rad1)):
                    command(el, List1[(List1_50)-i])
                    break
                if circle_circle(List1[(List1_50-1)-i].get_pos(adj_rad2), el.get_pos(adj_rad1)):
                    command(el, List1[(List1_50-1)-i])
                    break
                if circle_circle(List1[(List1_len-1)-i].get_pos(adj_rad2), el.get_pos(adj_rad1)):
                    command(el, List1[(List1_len-1)-i])
                    break
                if circle_circle(List1[(List1_len-2)-i].get_pos(adj_rad2), el.get_pos(adj_rad1)):
                    command(el, List1[(List1_len-2)-i])
                    break
            else:
                break

    def bullet_collide_rock(self, b, r):
        b.kill()
        self.score_counter(r)
        self.reduce_rock_size(r)
        sfxlen = random.randint(100, 300)
        if self.sfx: self.explosionfx.play(maxtime=sfxlen)

    def p1_collide_rock(self, p1, r):
        if self.sfx: self.explosionfx.play()
        if Player.LIFES > 0:
            p1.respawn()
            r.kill()
            self.rh.add_new_rocks(len(Rock.rocks))
            Player.LIFES -= 1
            Player.SCORE += 105
        else:
            p1.set_is_visible(False)
            p1.set_is_moving(False)
            self.sfx = False
            self.set_state("GameOver")

        self.save_hi_score(Player.SCORE)
        
    def rock_collide_planet(self, p, r):
        if self.sfx: self.explosionfx.play()
        if Planet.LIFES > 0:
            r.kill()
            p.set_img_id(p.get_img_id()+1)
            Planet.LIFES -= 1
        else:
            p.set_is_visible(False)
            self.p1.set_is_visible(False)
            self.p1.set_is_moving(False)
            self.sfx = False
            self.set_state("GameOver")

    def reduce_rock_size(self, r):
        """ Reduce rock size and Increase the speed """
        r.set_scalar(r.get_scalar()*0.8)
        r.set_orbit_speed(r.get_orbit_speed()*1.6)
        r.set_center_pull(r.get_center_pull()*1.5)
        if r.get_scalar() < 0.6:
            r.kill()
            self.rh.add_new_rocks(len(Rock.rocks))
            if self.sfx: self.explosionfx.play()

    def score_counter(self, r):
        if r.get_scalar() > 0.8:
            Player.SCORE += int(r.get_scalar()*2)+10
        elif r.get_scalar() > 0.6:
            Player.SCORE += int(r.get_scalar()*4)+20
        else:
            Player.SCORE += int(r.get_scalar()*8)+50

        self.bonus_earnings()
        self.save_hi_score(Player.SCORE)

    def bonus_earnings(self):
        rndm_sfx = random.choice([self.bonus_sfx_1, self.bonus_sfx_2])
        if Player.SCORE >= self.bullet_bonus_speed:
            self.p1.set_bullet_speed(self.p1.get_bullet_speed()*1.02)
            self.bullet_bonus_speed += 1995
        if Player.SCORE >= self.player_bonus_life:
            Player.LIFES += 1
            self.player_bonus_life += 2706
            if self.sfx: rndm_sfx.play()
        if Player.SCORE >= self.planet_bonus_life:
            Planet.LIFES += 1
            self.planet_bonus_life += 4701
            if self.sfx: rndm_sfx.play()
            if  self.planet.get_img_id() > 0:
                self.planet.set_img_id(self.planet.get_img_id()-1)

    def save_hi_score(self, current_score):
        if current_score >= Player.HI_SCORE:
            Player.HI_SCORE = current_score
            score_to_txt(Player.HI_SCORE, mode="w")


#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
            #### #### #### #### FUNCTIONS #### #### #### ####
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####

def format(num):
    if num < 10: return f"000000{num}"
    elif num < 100: return f"00000{num}"
    elif num < 1000: return f"0000{num}"
    elif num < 10000: return f"000{num}"
    elif num < 100000: return f"00{num}"
    elif num < 1000000: return f"0{num}"
    elif num < 10000000: return f"{num}"

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
            #### #### #### #### MAIN #### #### #### ####
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####

def main():
    global SZ
    # Init/FPS
    pg.init()
    clock = pg.time.Clock()
    FPS, fixed_FPS = 45, 60
    prev_time = time.time()
    # Window/Canvas Setup
    CW, CH = 320, 240 
    canvas = pg.Surface([CW, CH])
    WW, WH = int(CW*SZ), int(CH*SZ) 
    screen = pg.display.set_mode((WW, WH))
    pg.canvas_size = [CW, CH]
    pg.display.set_caption('PLANET PROTECTOR')

    #### INSTANCES ####
    game = Game(canvas, [CW, CH])

    stars = pg.Surface((CW, CH))
    for i in range(100):
        pos = [random.randint(0, CW), random.randint(0, CH)]
        pg.draw.line(stars, ("white"), pos, pos)


    #### ANIMATION LOOP ####
    while True:      
        pg.key.set_repeat(1000)
        for event in pg.event.get():
            pg.event.clear()
            if (event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit(); exit();

        #### KEYBOARD/JOYSTICK ####
            if event.type == pg.KEYDOWN:
                keydown = event.key
                game.stick_kd(keydown)
                pg.event.clear()

            elif event.type == pg.KEYUP:
                keyup = event.key
                game.stick_ku(keyup)
                pg.event.clear()
    
        #### DELTA TIME ####
        current_time = time.time()
        dt = current_time - prev_time
        dt *= fixed_FPS
        prev_time = current_time
    
        #### UPDATE SCREEN ####
        canvas.fill('black')
        
        canvas.blit(stars, (0, 0))
        game.animate(canvas, dt)
        
        scaled_canvas = pg.transform.scale(canvas, [WW, WH])
        screen.blit(scaled_canvas, [0, 0])
        pg.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

