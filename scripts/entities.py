import pygame


# The PhysicsEntity class is a blueprint for creating objects that represent physical entities in a
# simulation.
class PhysicsEntity:
    def __init__(self, game, entity_type, pos, size):
        """
        The function initializes an entity object with various attributes and sets the initial action to
        "idle".

        :param game: The "game" parameter is a reference to the game object or instance that this entity
        belongs to. It allows the entity to interact with the game world and access game-specific
        functionality
        :param entity_type: The `entity_type` parameter represents the type of entity that this object
        is. It could be a player, an enemy, a projectile, or any other type of entity in the game
        :param pos: The "pos" parameter represents the position of the entity in the game world. It is a
        tuple or list containing the x and y coordinates of the entity's position
        :param size: The "size" parameter represents the size of the entity. It could be the width and
        height of the entity's bounding box or the dimensions of the entity's sprite. The exact
        interpretation of "size" depends on the implementation of the game and the entity's behavior
        """
        self.game = game
        self.type = entity_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

        self.action = ""
        self.animation_offset = (-6, -6)
        self.flip = False
        self.set_action("idle")

        self.last_movement = [0, 0]

    def rect(self):
        """
        The function returns a pygame Rect object with the specified position and size.
        :return: a pygame Rect object.
        """
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        """
        The function sets the action and animation of an object in a game.

        :param action: The "action" parameter is a string that represents the desired action for the
        object
        """
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type][self.action].copy()

    def update(self, tilemap, movement=(0, 0)):
        """
        The `update` function updates the position and velocity of an entity in a tilemap, checks for
        collisions with the tilemap, and updates the animation of the entity.

        :param tilemap: The `tilemap` parameter is an object that represents the game's tilemap. It
        likely contains information about the layout of the game world, such as the positions and
        properties of tiles
        :param movement: The `movement` parameter is a tuple representing the desired movement of the
        entity in the x and y directions. The default value is `(0, 0)`, which means no movement in
        either direction. The `update` method updates the position of the entity based on the movement
        and checks for collisions
        """
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        """
        The `render` function blits the flipped animation image onto a surface at a specified position
        offset.

        :param surf: The `surf` parameter is the surface on which the image will be rendered. It is the
        surface where the image will be blitted (drawn) onto
        :param offset: The `offset` parameter is a tuple that represents the x and y coordinates of the
        offset. It is used to adjust the position of the rendered image on the surface (`surf`). By
        subtracting the offset from the position (`self.pos`) and adding the animation offset
        (`self.animation_offset`), the
        """
        surf.blit(
            pygame.transform.flip(self.animation.img(), self.flip, False),
            [
                self.pos[0] - offset[0] + self.animation_offset[0],
                self.pos[1] - offset[1] + self.animation_offset[1],
            ],
        )


# The Player class is a subclass of the PhysicsEntity class.
class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        """
        The function initializes a player object with a game, position, and size, and sets the air_time
        attribute to 0.

        :param game: The "game" parameter is a reference to the game object that the player belongs to.
        It is used to access and interact with other game elements and functionalities
        :param pos: The "pos" parameter represents the position of the player in the game. It is a tuple
        or list containing the x and y coordinates of the player's position
        :param size: The "size" parameter represents the size of the player object. It could be the
        width and height of the player's sprite or the dimensions of the player's hitbox. The exact
        interpretation of "size" would depend on the implementation of the game
        """
        super().__init__(game, "player", pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_jumps = False

    def jump(self):
        if self.wall_jumps:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -3
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -3
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True

        elif self.jumps:
            self.jumps -= 1
            self.velocity[1] = -4
            self.air_time = 5
            return True

    def update(self, tilemap, movement=(0, 0)):
        """
        The function updates the player's action based on their movement and collision with the tilemap.

        :param tilemap: The `tilemap` parameter is a reference to the game's tilemap. It is used to
        check for collisions and determine the player's position in the game world
        :param movement: The `movement` parameter is a tuple that represents the horizontal and vertical
        movement of the character. The first element of the tuple represents the horizontal movement
        (left or right), and the second element represents the vertical movement (up or down)
        """
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions["down"]:
            self.air_time = 0
            self.jumps = 2

        self.wall_jumps = False

        if (self.collisions["right"] or self.collisions["left"]) and self.air_time > 4:
            self.wall_jumps = True
            self.velocity[1] = min(self.velocity[1], 0.5)

            self.flip = not self.collisions["right"]

        self.set_action("wall_jump")

        if not self.wall_jumps:
            if self.air_time > 4:
                self.set_action("jump")
            elif movement[0] != 0:
                self.set_action("run")
            else:
                self.set_action("idle")

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
