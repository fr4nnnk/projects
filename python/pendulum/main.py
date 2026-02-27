import pygame
import math

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pendulum")

clock = pygame.time.Clock()

# Pendulum parameters
origin = (WIDTH // 2, 100)  # Pivot point
length = 300                # Length of string (pixels)
#g = 9.81                    # Gravity
g = 1000
theta = math.pi / 4         # Initial angle (45 degrees)
omega = 0                   # Angular velocity
dt = 0.02                   # Time step

running = True
while running:
    clock.tick(60)  # 60 FPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Physics (small angle approximation)
    #alpha = -(g / length) * theta  # Angular acceleration
    alpwha = -(g / length) * math.sin(theta)
    omega += alpha * dt
    theta += omega * dt

    # Convert polar to Cartesian
    x = origin[0] + length * math.sin(theta)
    y = origin[1] + length * math.cos(theta)

    # Draw
    screen.fill((30, 30, 30))
    
    pygame.draw.line(screen, (255, 255, 255), origin, (x, y), 2)
    pygame.draw.circle(screen, (200, 0, 0), (int(x), int(y)), 20)
    
    pygame.display.flip()

pygame.quit()
