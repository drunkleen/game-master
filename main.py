import pygame
import sys
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, load_transparent_images, Animation
from scripts.tilemap import TileMap
from scripts.clouds import Clouds


class Game:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 1920, 1010
        self.FPS = 60

        pygame.display.set_caption("Game Master")

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.display = pygame.Surface((self.WIDTH / 2, self.HEIGHT / 2))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            "decor": load_images("tiles/decor"),
            "grass": load_images("tiles/grass"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
            "background": load_image("background.png"),
            "clouds": load_images("clouds"),
            "player_stand": load_image("entities/player.png"),
            "player": {
                "idle": Animation(
                    load_transparent_images("entities/player/idle"), image_duration=6
                ),
                "jump": Animation(load_images("entities/player/jump")),
                "run": Animation(load_images("entities/player/run"), image_duration=4),
                "slide": Animation(load_images("entities/player/slide")),
                "wall_slide": Animation(load_images("entities/player/wall_slide")),
            },
        }

        self.clouds = Clouds(self.assets["clouds"], count=16)

        self.player = Player(self, (50, 50), (16, 30))

        self.tilemap = TileMap(self, tile_size=32)

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.display.fill((39, 98, 131))

            self.scroll[0] += (
                self.player.rect().centerx
                - self.display.get_width() / 2
                - self.scroll[0]
            ) / 30
            self.scroll[1] += (
                self.player.rect().centery
                - self.display.get_height() / 2
                - self.scroll[1]
            ) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        self.movement[0] = True
                    if event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.movement[1] = True
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.player.velocity[1] = -3

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
