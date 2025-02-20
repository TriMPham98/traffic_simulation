import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROAD_WIDTH = 100
CAR_WIDTH, CAR_HEIGHT = 40, 60
LANE_WIDTH = ROAD_WIDTH // 2
FPS = 60

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
                self.y -= self.speed if self.lane == 'in' else -self.speed
            elif self.direction == 'S':
                self.y += self.speed if self.lane == 'in' else -self.speed
            elif self.direction == 'E':
                self.x += self.speed if self.lane == 'in' else -self.speed
            elif self.direction == 'W':
                self.x -= self.speed if self.lane == 'in' else -self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, CAR_WIDTH, CAR_HEIGHT))

    def at_intersection(self):
        if self.lane == 'in':
            if self.direction == 'N' and self.y <= HEIGHT // 2 + ROAD_WIDTH // 2:
                return True
            elif self.direction == 'S' and self.y >= HEIGHT // 2 - ROAD_WIDTH // 2:
                return True
            elif self.direction == 'E' and self.x >= WIDTH // 2 - ROAD_WIDTH // 2:
                return True
            elif self.direction == 'W' and self.x <= WIDTH // 2 + ROAD_WIDTH // 2:
                return True
        return False

class TrafficLight:
    def __init__(self):
        self.state = 0  # 0: N-S green, 1: N-S yellow, 2: E-W green, 3: E-W yellow
        self.last_change = pygame.time.get_ticks()
        self.phase_durations = [4000, 1000, 4000, 1000]  # ms

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_change
        if elapsed >= self.phase_durations[self.state]:
            self.state = (self.state + 1) % 4
            self.last_change = current_time

    def draw(self, surface):
        light_size = 20
        if self.state == 0:  # N-S green
            ns_color, ew_color = GREEN, RED
        elif self.state == 1:  # N-S yellow
            ns_color, ew_color = YELLOW, RED
        elif self.state == 2:  # E-W green
            ns_color, ew_color = RED, GREEN
        else:  # E-W yellow
            ns_color, ew_color = RED, YELLOW
        
        # North and South lights
        pygame.draw.circle(surface, ns_color, (WIDTH // 2 - ROAD_WIDTH // 2 - 20, HEIGHT // 2 - ROAD_WIDTH // 2 - 20), light_size)
        pygame.draw.circle(surface, ns_color, (WIDTH // 2 + ROAD_WIDTH // 2 + 20, HEIGHT // 2 + ROAD_WIDTH // 2 + 20), light_size)
        pygame.draw.circle(surface, ns_color, (WIDTH // 2 + ROAD_WIDTH // 2 + 20, HEIGHT // 2 - ROAD_WIDTH // 2 - 20), light_size)
        pygame.draw.circle(surface, ns_color, (WIDTH // 2 - ROAD_WIDTH // 2 - 20, HEIGHT // 2 + ROAD_WIDTH // 2 + 20), light_size)
        # East and West lights
        pygame.draw.circle(surface, ew_color, (WIDTH // 2 + ROAD_WIDTH // 2 + 20, HEIGHT // 2 + ROAD_WIDTH // 2 + 20), light_size)
        pygame.draw.circle(surface, ew_color, (WIDTH // 2 - ROAD_WIDTH // 2 - 20, HEIGHT // 2 - ROAD_WIDTH // 2 - 20), light_size)
        pygame.draw.circle(surface, ew_color, (WIDTH // 2 - ROAD_WIDTH // 2 - 20, HEIGHT // 2 + ROAD_WIDTH // 2 + 20), light_size)
        pygame.draw.circle(surface, ew_color, (WIDTH // 2 + ROAD_WIDTH // 2 + 20, HEIGHT // 2 - ROAD_WIDTH // 2 - 20), light_size)

def draw_intersection(surface):
    surface.fill(WHITE)
    pygame.draw.rect(surface, GRAY, (0, HEIGHT // 2 - ROAD_WIDTH // 2, WIDTH, ROAD_WIDTH))  # Horizontal road
    pygame.draw.rect(surface, GRAY, (WIDTH // 2 - ROAD_WIDTH // 2, 0, ROAD_WIDTH, HEIGHT))  # Vertical road
    pygame.draw.line(surface, WHITE, (WIDTH // 2, HEIGHT // 2 - ROAD_WIDTH // 2), (WIDTH // 2, HEIGHT // 2 + ROAD_WIDTH // 2), 2)
    pygame.draw.line(surface, WHITE, (WIDTH // 2 - ROAD_WIDTH // 2, HEIGHT // 2), (WIDTH // 2 + ROAD_WIDTH // 2, HEIGHT // 2), 2)

def simulate_traffic():
    cars = []
    directions = ['N', 'S', 'E', 'W']
    lanes = ['in', 'out']
    last_spawn = pygame.time.get_ticks()
    spawn_interval = 2000  # 2 seconds in ms
    traffic_light = TrafficLight()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Spawn new cars
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn > spawn_interval:
            if random.random() < 0.7:
                direction = random.choice(directions)
                lane = random.choice(lanes)
                cars.append(Car(direction, lane))
            last_spawn = current_time
        
        # Update traffic light
        traffic_light.update()
        
        # Handle traffic rules
        for car in cars:
            if car.lane == 'in':
                if car.at_intersection():
                    # Check traffic light state
                    if (car.direction in ['N', 'S'] and traffic_light.state != 0) or \
                       (car.direction in ['E', 'W'] and traffic_light.state != 2):
                        car.waiting = True  # Light is not green, so wait
                    else:
                        # Light is green, check for collision
                        can_proceed = True
                        for other_car in cars:
                            if other_car != car and not other_car.waiting:
                                if abs(other_car.x - car.x) < CAR_WIDTH and abs(other_car.y - car.y) < CAR_HEIGHT:
                                    can_proceed = False
                                    break
                        car.waiting = not can_proceed  # Wait if collision, proceed if clear
                else:
                    # Not at intersection, so move towards it
                    car.waiting = False
            # 'out' cars keep waiting = False (set at initialization, no need to change)
        
        # Update car positions
        for car in cars[:]:
            car.move()
            if car.x < -CAR_WIDTH or car.x > WIDTH or car.y < -CAR_HEIGHT or car.y > HEIGHT:
                cars.remove(car)
        
        # Draw everything
        draw_intersection(screen)
        traffic_light.draw(screen)
        for car in cars:
            car.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    simulate_traffic()