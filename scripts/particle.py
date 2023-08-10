# The Particle class is a blueprint for creating particle objects.
class Particle:
    def __init__(self, game, particle_type, pos, velocity=[0, 0], frame=0):
        """
        The function initializes a particle object with specified attributes.

        :param game: The "game" parameter is an instance of the game class that the particle belongs to.
        It is used to access game assets and perform game-related operations
        :param particle_type: The `particle_type` parameter represents the type of particle. It is used
        to determine the animation for the particle
        :param pos: The "pos" parameter represents the position of the particle in the game world. It is
        a list containing the x and y coordinates of the particle's position
        :param velocity: The velocity parameter is a list representing the initial velocity of the
        particle in the x and y directions. The default value is [0, 0], which means the particle starts
        with no initial velocity
        :param frame: The "frame" parameter is used to specify the initial frame of the particle
        animation. It determines which frame of the animation will be displayed when the particle is
        first created, defaults to 0 (optional)
        """
        self.game = game
        self.type = particle_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.frame = frame
        self.animation = self.game.assets[f"particle/{particle_type}"].copy()

    def update(self):
        """
        The function updates the position and animation of an object and returns a boolean value
        indicating if the animation is done.
        :return: the value of the variable "kill".
        """
        kill = bool(self.animation.done)

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animation.update()

        return kill

    def render(self, surf, offset=(0, 0)):
        """
        The `render` function takes a surface and an offset as parameters, and blits the animation image
        onto the surface at a position calculated based on the object's position and the offset.

        :param surf: The `surf` parameter is the surface on which the image will be rendered. It is the
        surface where the image will be blitted onto
        :param offset: The `offset` parameter is a tuple that represents the x and y offsets for
        positioning the image on the surface (`surf`). It is used to adjust the position of the image
        relative to the surface. By default, the offset is set to (0, 0), which means the image will be
        """
        img = self.animation.img()
        surf.blit(
            self.animation.img(),
            (
                self.pos[0] - offset[0] - img.get_width() // 2,
                self.pos[1] - offset[1] - img.get_width() // 2,
            ),
        )
