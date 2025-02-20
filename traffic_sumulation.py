import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROAD_WIDTH = 100
CAR_WIDTH, CAR_HEIGHT = 40, 60
FPS = 60
LIGHT_CYCLE = 5000  # 5 seconds in milliseconds

# Colors
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4-Way Stop Traffic Simulation with Lights")
clock = pygame.time.Clock()

class Car:
    def __init__(self, direction):
        self.direction = direction  # 'N', 'S', 'E', 'W'
        self.speed = 2
        self.waiting = True
        
        # Initial positions based on direction
        if direction == 'N':
            self.x = WIDTH // 2 - CAR_WIDTH // 2
            self.y = HEIGHT - CAR_HEIGHT - 150
            self.color = RED
        elif direction == 'S':
            self.x = WIDTH // 2 - CAR_WIDTH // 2
            self.y = 150
            self.color = BLUE
        elif direction == 'E':
            self.x = 150
            self.y = HEIGHT // 2 - CAR_HEIGHT // 2
            self.color = GREEN
        elif direction == 'W':
            self.x = WIDTH - CAR_WIDTH - 150
            self.y = HEIGHT // 2 - CAR_HEIGHT // 2
            self.color = YELLOW

    def move(self):
        if not self.waiting:
            if self.direction == 'N':
                self.y -= self.speed
            elif self.direction == 'S':
                self.y += self.speed
            elif self.direction == 'E':
                self.x += self.speed
            elif self.direction == 'W':
                self.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, CAR_WIDTH, CAR_HEIGHT))

class TrafficLight:
    def __init__(self):
        self.ns_green = True  # True: N-S green, E-W red; False: E-W green, N-S red
        self.last_change = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_change >= LIGHT_CYCLE:
            self.ns_green = not self.ns_green
            self.last_change = current_time

    def draw(self, surface):
        light_size = 20
        # N-S lights
        ns_color = GREEN if self.ns_green else RED
        ew_color = RED if self.ns_green else GREEN
        
        # North light
        pygame.draw.circle(surface, ns_color, (WIDTH//2 - ROAD_WIDTH//2 - 20, HEIGHT//2 - ROAD_WIDTH//2 - 20), light_size)
        # South light
        pygame.draw.circle(surface, ns_color, (WIDTH//2 + ROAD_WIDTH//2 + 20, HEIGHT//2 + ROAD_WIDTH//2 + 20), light_size)
        # East light
        pygame.draw.circle(surface, ew_color, (WIDTH//2 + ROAD_WIDTH//2 + 20, HEIGHT//2 - ROAD_WIDTH//2 - 20), light_size)
        # West light
        pygame.draw.circle(surface, ew_color, (WIDTH//2 - ROAD_WIDTH//2 - 20, HEIGHT//2 + ROAD_WIDTH//2 + 20), light_size)

def draw_intersection(surface):
    surface.fill(WHITE)
    
    # Draw roads
    pygame.draw.rect(surface, GRAY, (0, HEIGHT//2 - ROAD_WIDTH//2, WIDTH, ROAD_WIDTH))  # Horizontal road
    pygame.draw.rect(surface, GRAY, (WIDTH//2 - ROAD_WIDTH//2, 0, ROAD_WIDTH, HEIGHT))  # Vertical road

def simulate_traffic():
    cars = []
    directions = ['N', 'S', 'E', 'W']
    last_spawn = time.time()
    spawn_interval = 2  # Seconds between car spawns
    traffic_light = TrafficLight()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Spawn new cars
        current_time = time.time()
        if current_time - last_spawn > spawn_interval:
            if random.random() < 0.7:  # 70% chance to spawn a car
                direction = random.choice(directions)
                cars.append(Car(direction))
            last_spawn = current_time
        
        # Update traffic light
        traffic_light.update()
        
        # Handle traffic rules with lights
        for car in cars:
            if car.waiting:
                # Check if car can proceed based on light
                if (car.direction in ['N', 'S'] and traffic_light.ns_green) or \
                   (car.direction in ['E', 'W'] and not traffic_light.ns_green):
                    # Check if intersection is clear
                    can_proceed = True
                    for other_car in cars:
                        if other_car != car and not other_car.waiting:
                            if abs(other_car.x - car.x) < CAR_WIDTH and abs(other_car.y - car.y) < CAR_HEIGHT:
                                can_proceed = False
                                break
                    if can_proceed:
                        car.waiting = False
        
        # Update car positions
        for car in cars[:]:
            car.move()
            # Remove cars that have left the screen
            if (car.x < -CAR_WIDTH or car.x > WIDTH or 
                car.y < -CAR_HEIGHT or car.y > HEIGHT):
                cars.remove(car)
        
        # Draw everything
        draw_intersection(screen)
        traffic_light.draw(screen)
        for car in cars:
            car.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

# Run the simulation
if __name__ == "__main__":
    simulate_traffic()