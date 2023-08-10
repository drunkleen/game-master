import pygame
import sys
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, load_transparent_images, Animation
from scripts.tilemap import TileMap
from scripts.clouds import Clouds
from scripts.particle import Particle
import random
import math


class Game:
    def __init__(self):
        """
        This function initializes various attributes and objects for a game.
        """
        pygame.init()

        self.WIDTH, self.HEIGHT = 1920, 1010
        self.FPS = 60

        pygame.display.set_caption("Game Master")

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.display = pygame.Surface((self.WIDTH / 2, self.HEIGHT / 2))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            "decor": load_transparent_images("tiles/decor"),
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
                "wall_jump": Animation(load_images("entities/player/wall_jump")),
            },
            "particle/leaf": Animation(
                load_images("particles/leaf"), image_duration=20, loop=False
            ),
        }

        self.clouds = Clouds(self.assets["clouds"], count=16)

        self.player = Player(self, (50, 50), (16, 30))

        self.tilemap = TileMap(self, tile_size=32)

        self.tilemap.load("map.json")

        self.leaf_spawners = []
        self.leaf_spawners.extend(
            pygame.Rect(4 + tree["pos"][0], 4 + tree["pos"][1], 23, 13)
            for tree in self.tilemap.extract([("large_decor", 2)], keep=True)
        )

        self.particles = []

        self.scroll = [0, 0]

    def run(self):
        """
        The `run` function is responsible for running the game loop, updating the display, handling
        player input, and rendering game objects.
        """
        while True:
            self.display.fill((22, 39, 112))
            self.display.blit(self.assets["background"], (0, 0))

            self.scroll[0] += (
                self.player.rect().centerx
                - self.display.get_width() / 2
                - self.scroll[0]
            ) / 30
            self.scroll[1] += (
                self.player.rect().centery
                - ((self.display.get_height() / 2) + (self.display.get_height() / 8))
                - self.scroll[1]
            ) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (
                        rect.x + random.random() * rect.width,
                        rect.y + random.random() * rect.height,
                    )
                    self.particles.append(
                        Particle(
                            self,
                            "leaf",
                            pos,
                            velocity=[-0.1, 0.3],
                            frame=random.randint(0, 20),
                        )
                    )

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == "leaf":
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        self.movement[0] = True
                    if event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.movement[1] = True
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        self.player.jump()

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
