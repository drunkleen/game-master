import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1920, 1010
FPS = 60


pygame.display.set_caption("Gay Master")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(FPS)
