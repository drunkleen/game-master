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

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}
AUTOTILE_TYPES = {"grass", "stone"}


# The TileMap class represents a map made up of tiles.
class TileMap:
    def __init__(self, game, tile_size=32):
        """
        The function initializes a class instance with a game object, a tilemap dictionary, a list of
        offgrid tiles, and a tile size.

        :param game: The "game" parameter is a reference to the game object that this tilemap belongs
        to. It is used to access and modify the game state and to interact with other game objects
        :param tile_size: The `tile_size` parameter is the size of each tile in pixels. It determines
        the width and height of each tile on the game map, defaults to 32 (optional)
        """
        self.game = game
        self.tilemap = {}
        self.offgrid_tiles = []
        self.tile_size = tile_size

    def tiles_around(self, pos) -> list:
        """
        The function "tiles_around" takes a position and returns a list of tiles surrounding that
        position.

        :param pos: The `pos` parameter represents the position of a tile on a grid. It is a tuple
        containing the x and y coordinates of the tile
        :return: a list of tiles.
        """
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
        """
        The function saves the tilemap, tile size, and offgrid tiles to a JSON file at the specified
        path.

        :param path: The `path` parameter is the file path where you want to save the data. It should be
        a string representing the file path, including the file name and extension. For example,
        "data.json" or "C:/Users/username/data.json"
        """
        with open(path, "w") as f:
            json.dump(
                {
                    "tilemap": self.tilemap,
                    "tile_size": self.tile_size,
                    "offgrid": self.offgrid_tiles,
                },
                f,
            )

    def load(self, path):
        with open(path, "r") as f:
            map_data = json.load(f)
            self.tilemap = map_data["tilemap"]
            self.tile_size = map_data["tile_size"]
            self.offgrid_tiles = map_data["offgrid"]

    def physics_rects_around(self, pos) -> list:
        """
        The function returns a list of pygame.Rect objects representing the physics tiles around a given
        position.

        :param pos: The `pos` parameter represents the position of a tile on a grid
        :return: a list of pygame.Rect objects.
        """
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

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [
                (1, 0),
                (-1, 0),
                (0, -1),
                (0, 1),
            ]:
                check_loc = f"{tile['pos'][0] + shift[0]};{tile['pos'][1] + shift[1]}"

                if (
                    check_loc in self.tilemap
                    and self.tilemap[check_loc]["type"] == tile["type"]
                ):
                    neighbors.add(shift)

            neighbors = tuple(sorted(neighbors))
            if (tile["type"] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile["variant"] = AUTOTILE_MAP[neighbors]

    def render(self, surf, offset=(0, 0)):
        """
        The `render` function takes a surface and an offset, and blits the appropriate tiles onto the
        surface based on the tilemap and offgrid_tiles.

        :param surf: The "surf" parameter is the surface object on which the tiles will be rendered. It
        is the surface where the tiles will be drawn onto
        :param offset: The `offset` parameter is a tuple that represents the x and y coordinates of the
        top-left corner of the portion of the surface (`surf`) that should be rendered. It is used to
        determine which tiles should be rendered based on their position relative to the offset
        """
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
