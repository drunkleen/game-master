import pygame

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
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tilemap = {}
        self.offgrid_tiles = []
        self.tile_size = tile_size

        for i in range(10):
            self.tilemap[f"{3 + i};10"] = {
                "type": "grass",
                "variant": 1,
                "pos": (3 + i, 10),
            }

            self.tilemap[f"10;{5 + i}"] = {
                "type": "stone",
                "variant": 1,
                "pos": (10, i + 5),
            }

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

    def render(
        self,
        surf,
    ):
        for tile in self.offgrid_tiles:
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                tile["pos"],
            )

        for location in self.tilemap:
            tile = self.tilemap[location]
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size),
            )
