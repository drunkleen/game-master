import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 1920, 1010
        self.FPS = 60

        pygame.display.set_caption("Gay Master")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.img = pygame.image.load("data/images/clouds/cloud_1.png")
        self.img.set_colorkey((0, 0, 0))
        self.img_position = [150, 400]

        self.movement = [False, False]

        self.collision_area = pygame.Rect(50, 50, 300, 50)

    def run(self):
        while True:
            self.screen.fill((14, 119, 148))

            img_r = pygame.Rect(*self.img_position, *self.img.get_size())

            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                pygame.draw.rect(self.screen, (0, 50, 255), self.collision_area)

            self.img_position[1] += self.movement[1] - self.movement[0]
            self.screen.blit(self.img, self.img_position)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        self.movement[0] = True
                    if event.key in (pygame.K_s, pygame.K_DOWN):
                        self.movement[1] = True

                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        self.movement[0] = False
                    if event.key in (pygame.K_s, pygame.K_DOWN):
                        self.movement[1] = False

            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    Game().run()
