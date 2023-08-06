import pygame
import json

NEIGHBOR_OFFSETS = [
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (0, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]
PHYSICS_TILES = {"grass", "stone"}


class TileMap:
    def __init__(self, game, tile_size=32):
        self.game = game
        self.tilemap = {}
        self.offgrid_tiles = []
        self.tile_size = tile_size

    def tiles_around(self, pos) -> list:
        tiles = []
        tile_location = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_location = (
                f"{tile_location[0] + offset[0]};{tile_location[1] + offset[1]}"
            )
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])
        return tiles

    def save(self, path):
        with open(path, "w") as f:
            json.dump(
                {
                    "tilemap": self.tilemap,
                    "tile_size": self.tile_size,
                    "offgrid": self.offgrid_tiles,
                },
                f,
            )

    def physics_rects_around(self, pos) -> list:
        return [
            pygame.Rect(
                tile["pos"][0] * self.tile_size,
                tile["pos"][1] * self.tile_size,
                self.tile_size,
                self.tile_size,
            )
            for tile in self.tiles_around(pos)
            if tile["type"] in PHYSICS_TILES
        ]

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]),
            )

        for x in range(
            offset[0] // self.tile_size,
            (offset[0] + surf.get_width()) // self.tile_size + 1,
        ):
            for y in range(
                offset[1] // self.tile_size,
                (offset[1] + surf.get_height()) // self.tile_size + 1,
            ):
                loc = f"{x};{y}"
                if loc in self.tilemap:
                    tile = self.tilemap[loc]

                    surf.blit(
                        self.game.assets[tile["type"]][tile["variant"]],
                        (
                            tile["pos"][0] * self.tile_size - offset[0],
                            tile["pos"][1] * self.tile_size - offset[1],
                        ),
                    )
