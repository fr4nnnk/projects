import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double Pendulum")

clock = pygame.time.Clock()

# Origin
origin = (WIDTH // 2, 200)

# Pendulum parameters
g = 1000  # Increased for pixel physics

L1 = 200
L2 = 200
m1 = 20
m2 = 20

theta1 = math.pi / 2
theta2 = math.pi / 2

omega1 = 0
omega2 = 0

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Physics ---

    num1 = -g * (2*m1 + m2) * math.sin(theta1)
    num2 = -m2 * g * math.sin(theta1 - 2*theta2)
    num3 = -2 * math.sin(theta1 - theta2) * m2
    num4 = omega2**2 * L2 + omega1**2 * L1 * math.cos(theta1 - theta2)
    den = L1 * (2*m1 + m2 - m2 * math.cos(2*theta1 - 2*theta2))

    alpha1 = (num1 + num2 + num3 * num4) / den

    num1 = 2 * math.sin(theta1 - theta2)
    num2 = omega1**2 * L1 * (m1 + m2)
    num3 = g * (m1 + m2) * math.cos(theta1)
    num4 = omega2**2 * L2 * m2 * math.cos(theta1 - theta2)
    den = L2 * (2*m1 + m2 - m2 * math.cos(2*theta1 - 2*theta2))

    alpha2 = (num1 * (num2 + num3 + num4)) / den

    omega1 += alpha1 * dt
    omega2 += alpha2 * dt

    theta1 += omega1 * dt
    theta2 += omega2 * dt

    # --- Convert to Cartesian ---
    x1 = origin[0] + L1 * math.sin(theta1)
    y1 = origin[1] + L1 * math.cos(theta1)

    x2 = x1 + L2 * math.sin(theta2)
    y2 = y1 + L2 * math.cos(theta2)

    # --- Draw ---
    screen.fill((20, 20, 20))

    pygame.draw.line(screen, (255, 255, 255), origin, (x1, y1), 2)
    pygame.draw.circle(screen, (255, 0, 0), (int(x1), int(y1)), m1)

    pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 2)
    pygame.draw.circle(screen, (0, 150, 255), (int(x2), int(y2)), m2)

    pygame.display.flip()

pygame.quit()
