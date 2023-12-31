import pygame
import sys
import contextlib
from utils import load_image, load_images, load_transparent_images, Animation
from tilemap import TileMap

RENDER_SCALE = 2.0


class LevelEditor:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 1920, 1010
        self.FPS = 60

        pygame.display.set_caption("Level Editor")

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.display = pygame.Surface((self.WIDTH / 2, self.HEIGHT / 2))

        self.clock = pygame.time.Clock()

        self.assets = {
            "decor": load_transparent_images("tiles/decor"),
            "grass": load_images("tiles/grass"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
        }

        self.movement = [False, False, False, False]

        self.tilemap = TileMap(self, tile_size=32)

        with contextlib.suppress(FileNotFoundError):
            self.tilemap.load("map.json")

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        self.clicking = False
        self.right_clicking = False
        self.shift_down = False

        self.ongrid = True

    def run(self):
        """
        The above function is a game loop that handles user input, updates the game state, and renders
        the game screen.
        """
        # sourcery skip: merge-else-if-into-elif, swap-nested-ifs, switch
        while True:
            self.display.fill((22, 22, 22))
            # self.display.blit(self.assets["background"], (0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 3
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 3

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][
                self.tile_variant
            ].copy()
            current_tile_img.set_alpha(100)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] / RENDER_SCALE, mouse_pos[1] / RENDER_SCALE)
            tile_pos = (
                int((mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size),
                int((mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size),
            )

            if self.ongrid:
                self.display.blit(
                    current_tile_img,
                    (
                        tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                        tile_pos[1] * self.tilemap.tile_size - self.scroll[1],
                    ),
                )
            else:
                self.display.blit(current_tile_img, mouse_pos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[f"{tile_pos[0]};{tile_pos[1]}"] = {
                    "type": self.tile_list[self.tile_group],
                    "variant": self.tile_variant,
                    "pos": tile_pos,
                }

            if self.right_clicking:
                tile_location = f"{tile_pos[0]};{tile_pos[1]}"
                if tile_location in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_location]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_image = self.assets[tile["type"]][tile["variant"]]
                    tile_r = pygame.Rect(
                        tile["pos"][0] - self.scroll[0],
                        tile["pos"][1] - self.scroll[1],
                        tile_image.get_width(),
                        tile_image.get_height(),
                    )
                    if tile_r.collidepoint(mouse_pos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (10, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append(
                                {
                                    "type": self.tile_list[self.tile_group],
                                    "variant": self.tile_variant,
                                    "pos": (
                                        mouse_pos[0] + self.scroll[0],
                                        mouse_pos[1] + self.scroll[1],
                                    ),
                                }
                            )

                    elif event.button == 3:
                        self.right_clicking = True

                    if self.shift_down:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(
                                self.assets[self.tile_list[self.tile_group]]
                            )
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(
                                self.assets[self.tile_list[self.tile_group]]
                            )
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(
                                self.tile_list
                            )
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(
                                self.tile_list
                            )
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    elif event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        self.movement[0] = True
                    if event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.movement[1] = True
                    if event.key in (pygame.K_w, pygame.K_UP):
                        self.movement[2] = True
                    if event.key in (pygame.K_s, pygame.K_DOWN):
                        self.movement[3] = True

                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid

                    if event.key == pygame.K_t:
                        self.tilemap.autotile()

                    if event.key == pygame.K_o:
                        self.tilemap.save("map.json")

                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                        self.shift_down = True

                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        self.movement[0] = False
                    if event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.movement[1] = False
                    if event.key in (pygame.K_w, pygame.K_UP):
                        self.movement[2] = False
                    if event.key in (pygame.K_s, pygame.K_DOWN):
                        self.movement[3] = False

                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                        self.shift_down = False

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )

            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    LevelEditor().run()
