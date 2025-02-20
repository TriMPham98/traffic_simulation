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

# Colors
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4-Way Stop Traffic Simulation")
clock = pygame.time.Clock()

class Car:
    def __init__(self, direction):
        self.direction = direction  # 'N', 'S', 'E', 'W'
        self.speed = 2
        self.arrival_time = time.time()
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

def draw_intersection(surface):
    surface.fill(WHITE)
    
    # Draw roads
    pygame.draw.rect(surface, GRAY, (0, HEIGHT//2 - ROAD_WIDTH//2, WIDTH, ROAD_WIDTH))  # Horizontal road
    pygame.draw.rect(surface, GRAY, (WIDTH//2 - ROAD_WIDTH//2, 0, ROAD_WIDTH, HEIGHT))  # Vertical road
    
    # Draw stop lines
    line_thickness = 5
    pygame.draw.rect(surface, WHITE, (WIDTH//2 - ROAD_WIDTH//2 - 50, HEIGHT//2 - line_thickness//2, 50, line_thickness))  # Left
    pygame.draw.rect(surface, WHITE, (WIDTH//2 + ROAD_WIDTH//2, HEIGHT//2 - line_thickness//2, 50, line_thickness))      # Right
    pygame.draw.rect(surface, WHITE, (WIDTH//2 - line_thickness//2, HEIGHT//2 - ROAD_WIDTH//2 - 50, line_thickness, 50))  # Top
    pygame.draw.rect(surface, WHITE, (WIDTH//2 - line_thickness//2, HEIGHT//2 + ROAD_WIDTH//2, line_thickness, 50))      # Bottom

def simulate_traffic():
    cars = []
    directions = ['N', 'S', 'E', 'W']
    last_spawn = time.time()
    spawn_interval = 2  # Seconds between car spawns
    
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
        
        # Handle traffic rules
        if cars:
            # Find earliest arrival time among waiting cars
            waiting_cars = [car for car in cars if car.waiting]
            if waiting_cars:
                earliest_car = min(waiting_cars, key=lambda x: x.arrival_time)
                # Check if it's safe to proceed (no cars in intersection from other directions)
                can_proceed = True
                for car in cars:
                    if car != earliest_car and not car.waiting:
                        if (earliest_car.direction in ['N', 'S'] and car.direction in ['E', 'W']) or \
                           (earliest_car.direction in ['E', 'W'] and car.direction in ['N', 'S']):
                            can_proceed = False
                            break
                if can_proceed:
                    earliest_car.waiting = False
        
        # Update car positions
        for car in cars[:]:
            car.move()
            # Remove cars that have left the screen
            if (car.x < -CAR_WIDTH or car.x > WIDTH or 
                car.y < -CAR_HEIGHT or car.y > HEIGHT):
                cars.remove(car)
        
        # Draw everything
        draw_intersection(screen)
        for car in cars:
            car.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

# Run the simulation
if __name__ == "__main__":
    simulate_traffic()