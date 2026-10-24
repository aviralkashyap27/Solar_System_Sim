import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800,800
WIN = pygame.display.set_mode((0,0),pygame.NOFRAME)
pygame.display.set_caption("Solar System Simulator")

WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (0,0,255)
DARK_GREY = (169,169,169)
ORANGE = (255,165,0)
RED = (255,0,0)

FONT_P = pygame.font.SysFont("comicsans", 19)
FONT_D = pygame.font.SysFont("comicsans", 12)
#Sun and Planets:
class Planet:
    AU = (1.496e+8)*1000 #1 au in meters
    G = 6.67430e-11 #m3 kg-1 s-2
    SCALE = 250/AU #1 AU is 100 pixels
    TIMESTEP = 3600*24

    def __init__(self,name,x,y,radius,color,mass):
        self.zoom = 1
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.x_vel = 0
        self.y_vel = 0

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH 
        y = self.y * self.SCALE + HEIGHT /2
        pygame.draw.circle(win, self.color,(x,y),self.radius)

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH 
                y = y * self.SCALE + HEIGHT /2
                
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        

        if not self.sun:
            distance_text = FONT_D.render(f"{round(self.distance_to_sun/self.AU,1)}AU",1,DARK_GREY)
            win.blit(distance_text,(x-distance_text.get_width()*1.4,y))

            Planet_text = FONT_P.render(f"{self.name}",1,WHITE)
            win.blit(Planet_text,(x-Planet_text.get_width()/6,y))
        

    def attraction(self, other):
        other_x , other_y = other.x, other.y

        distance_x = other_x - self.x
        distance_y = other_y - self.y

        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun :
            self.distance_to_sun = distance

        Force = (self.G*self.mass*other.mass) / (distance**2)
        
        theta = math.atan2(distance_y,distance_x)
        force_x = math.cos(theta)*Force
        force_y = math.sin(theta)*Force
        return force_x,force_y

    def update_position(self,planets):
        total_fx = total_fy = 0

        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx /self.mass * self.TIMESTEP
        self.y_vel += total_fy /self.mass * self.TIMESTEP

        self.x += self.x_vel*self.TIMESTEP
        self.y += self.y_vel*self.TIMESTEP

        self.orbit.append((self.x,self.y))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.pause_game()

        if keys[pygame.K_ESCAPE]:
            quit()

    def pause_game(self):
        global run 
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                    if event.key == pygame.K_ESCAPE:
                        is_paused = False
                        run = False


                if event.type == pygame.QUIT:
                    is_paused = False
                    run = False

          
        
                
def main():
    run = True
    clock = pygame.time.Clock()
    
    SUN_MASS = 1.989e30
    MERCURY_MASS = 3.301e23
    VENUS_MASS   = 4.867e24
    EARTH_MASS   = 5.972e24
    MARS_MASS    = 6.417e23
    JUPITER_MASS = 1.898e27
    SATURN_MASS  = 5.683e26
    URANUS_MASS  = 8.681e25
    NEPTUNE_MASS = 1.024e26

    MERCURY_VEL = 47.36e3
    VENUS_VEL   = 35.02e3
    EARTH_VEL   = 29.78e3
    MARS_VEL    = 24.07e3
    JUPITER_VEL = 13.07e3
    SATURN_VEL  = 9.69e3
    URANUS_VEL  = 6.81e3
    NEPTUNE_VEL = 5.43e3

    sun = Planet("SUN",0,0,20,YELLOW,SUN_MASS)
    sun.sun = True

    earth = Planet("Earth",-1*Planet.AU,0,4,BLUE,EARTH_MASS)
    earth.y_vel = EARTH_VEL

    mercury = Planet("Mercury",-0.387*Planet.AU,0,2,DARK_GREY,MERCURY_MASS)
    mercury.y_vel = MERCURY_VEL

    venus = Planet("Venus",-0.723 * Planet.AU,0,4,ORANGE,VENUS_MASS)
    venus.y_vel = VENUS_VEL

    mars = Planet("Mars",-1.524 * Planet.AU,0,2.5,RED,MARS_MASS)
    mars.y_vel = MARS_VEL

    jupiter = Planet("Jupiter",-5.203 * Planet.AU, 0, 1, RED, JUPITER_MASS)
    jupiter.y_vel = JUPITER_VEL

    saturn = Planet("Saturn",-9.537 * Planet.AU, 0, 1, YELLOW,SATURN_MASS)
    saturn.y_vel = SATURN_VEL

    uranus = Planet("Uranus",-19.191 * Planet.AU, 0, 1, WHITE, URANUS_MASS)
    uranus.y_vel = URANUS_VEL

    neptune = Planet("Neptune",-30.07 * Planet.AU, 0, 1, BLUE, NEPTUNE_MASS)
    neptune.y_vel = NEPTUNE_VEL

    planets = [sun,earth,mercury,venus,mars,jupiter,saturn,uranus,neptune]

    
    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    pygame.quit()

main()
