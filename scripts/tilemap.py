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
