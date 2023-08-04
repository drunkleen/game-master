import pygame
import sys
from scripts.entities import PhysicsEntiry
from scripts.utils import load_image, load_images
from scripts.tilemap import TileMap


class Game:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 1920, 1010
        self.FPS = 60

        pygame.display.set_caption("Gay Master")

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.display = pygame.Surface((self.WIDTH / 4, self.HEIGHT / 4))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            "decor": load_images("tiles/decor"),
            "grass": load_images("tiles/grass"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
            "player": load_image("entities/player.png"),
        }

        self.player = PhysicsEntiry(self, "player", (50, 50), (8, 15))

        self.tilemap = TileMap(self, tile_size=16)

    def run(self):
        while True:
            self.display.fill((14, 119, 148))

            self.tilemap.render(self.display)

            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        self.movement[0] = True
                    if event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.movement[1] = True

                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        self.movement[0] = False
                    if event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.movement[1] = False

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )

            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    Game().run()