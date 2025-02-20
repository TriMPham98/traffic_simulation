import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROAD_WIDTH = 100
CAR_WIDTH, CAR_HEIGHT = 40, 60
LANE_WIDTH = ROAD_WIDTH // 2
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
pygame.display.set_caption("4-Way Intersection with Two-Way Traffic and Lights")
clock = pygame.time.Clock()

class Car:
    def __init__(self, direction, lane):
        self.direction = direction  # 'N', 'S', 'E', 'W'
        self.lane = lane  # 'in' (approaching), 'out' (leaving)
        self.speed = 2
        self.waiting = True if lane == 'in' else False  # Outgoing cars don't wait
        
        # Initial positions based on direction and lane
        if direction == 'N':
            self.x = WIDTH // 2 - LANE_WIDTH // 2 - CAR_WIDTH // 2 if lane == 'in' else WIDTH // 2 + LANE_WIDTH // 2 - CAR_WIDTH // 2
            self.y = HEIGHT - CAR_HEIGHT - 150 if lane == 'in' else 150
            self.color = RED
        elif direction == 'S':
            self.x = WIDTH // 2 + LANE_WIDTH // 2 - CAR_WIDTH // 2 if lane == 'in' else WIDTH // 2 - LANE_WIDTH // 2 - CAR_WIDTH // 2
            self.y = 150 if lane == 'in' else HEIGHT - CAR_HEIGHT - 150
            self.color = BLUE
        elif direction == 'E':
            self.x = 150 if lane == 'in' else WIDTH - CAR_WIDTH - 150
            self.y = HEIGHT // 2 - LANE_WIDTH // 2 - CAR_HEIGHT // 2 if lane == 'in' else HEIGHT // 2 + LANE_WIDTH // 2 - CAR_HEIGHT // 2
            self.color = GREEN
        elif direction == 'W':
            self.x = WIDTH - CAR_WIDTH - 150 if lane == 'in' else 150
            self.y = HEIGHT // 2 + LANE_WIDTH // 2 - CAR_HEIGHT // 2 if lane == 'in' else HEIGHT // 2 - LANE_WIDTH // 2 - CAR_HEIGHT // 2
            self.color = YELLOW

    def move(self):
        if not self.waiting:
            if self.direction == 'N':
                if self.lane == 'in':
                    self.y -= self.speed
                else:
                    self.y += self.speed
            elif self.direction == 'S':
                if self.lane == 'in':
                    self.y += self.speed
                else:
                    self.y -= self.speed
            elif self.direction == 'E':
                if self.lane == 'in':
                    self.x += self.speed
                else:
                    self.x -= self.speed
            elif self.direction == 'W':
                if self.lane == 'in':
                    self.x -= self.speed
                else:
                    self.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, CAR_WIDTH, CAR_HEIGHT))

    def at_intersection(self):
        # Check if car is near the intersection
        if self.lane == 'in':
            if self.direction == 'N' and self.y <= HEIGHT//2 + ROAD_WIDTH//2:
                return True
            elif self.direction == 'S' and self.y >= HEIGHT//2 - ROAD_WIDTH//2:
                return True
            elif self.direction == 'E' and self.x >= WIDTH//2 - ROAD_WIDTH//2:
                return True
            elif self.direction == 'W' and self.x <= WIDTH//2 + ROAD_WIDTH//2:
                return True
        return False

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
        ns_color = GREEN if self.ns_green else RED
        ew_color = RED if self.ns_green else GREEN
        
        # North lights (left for incoming, right for outgoing)
        pygame.draw.circle(surface, ns_color, (WIDTH//2 - ROAD_WIDTH//2 - 20, HEIGHT//2 - ROAD_WIDTH//2 - 20), light_size)
        pygame.draw.circle(surface, ns_color, (WIDTH//2 + ROAD_WIDTH//2 + 20, HEIGHT//2 + ROAD_WIDTH//2 + 20), light_size)
        # South lights
        pygame.draw.circle(surface, ns_color, (WIDTH//2 + ROAD_WIDTH//2 + 20, HEIGHT//2 - ROAD_WIDTH//2 - 20), light_size)
        pygame.draw.circle(surface, ns_color, (WIDTH//2 - ROAD_WIDTH//2 - 20, HEIGHT//2 + ROAD_WIDTH//2 + 20), light_size)
        # East lights
        pygame.draw.circle(surface, ew_color, (WIDTH//2 + ROAD_WIDTH//2 + 20, HEIGHT//2 + ROAD_WIDTH//2 + 20), light_size)
        pygame.draw.circle(surface, ew_color, (WIDTH//2 - ROAD_WIDTH//2 - 20, HEIGHT//2 - ROAD_WIDTH//2 - 20), light_size)
        # West lights
        pygame.draw.circle(surface, ew_color, (WIDTH//2 - ROAD_WIDTH//2 - 20, HEIGHT//2 + ROAD_WIDTH//2 + 20), light_size)
        pygame.draw.circle(surface, ew_color, (WIDTH//2 + ROAD_WIDTH//2 + 20, HEIGHT//2 - ROAD_WIDTH//2 - 20), light_size)

def draw_intersection(surface):
    surface.fill(WHITE)
    
    # Draw roads
    pygame.draw.rect(surface, GRAY, (0, HEIGHT//2 - ROAD_WIDTH//2, WIDTH, ROAD_WIDTH))  # Horizontal road
    pygame.draw.rect(surface, GRAY, (WIDTH//2 - ROAD_WIDTH//2, 0, ROAD_WIDTH, HEIGHT))  # Vertical road
    
    # Draw lane lines
    pygame.draw.line(surface, WHITE, (WIDTH//2, HEIGHT//2 - ROAD_WIDTH//2), (WIDTH//2, HEIGHT//2 + ROAD_WIDTH//2), 2)
    pygame.draw.line(surface, WHITE, (WIDTH//2 - ROAD_WIDTH//2, HEIGHT//2), (WIDTH//2 + ROAD_WIDTH//2, HEIGHT//2), 2)

def simulate_traffic():
    cars = []
    directions = ['N', 'S', 'E', 'W']
    lanes = ['in', 'out']
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
                lane = random.choice(lanes)
                cars.append(Car(direction, lane))
            last_spawn = current_time
        
        # Update traffic light
        traffic_light.update()
        
        # Handle traffic rules with lights
        for car in cars:
            if car.lane == 'in':  # Only incoming cars respect lights
                if car.at_intersection():
                    # Check light state
                    if (car.direction in ['N', 'S'] and not traffic_light.ns_green) or \
                       (car.direction in ['E', 'W'] and traffic_light.ns_green):
                        car.waiting = True
                    else:
                        # Check for collisions
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