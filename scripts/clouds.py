import random


class Cloud:
    def __init__(self, pos, img, speed, depth):
        """
        The function initializes an object with position, image, speed, and depth attributes.

        :param pos: The pos parameter is a list that represents the position of an object. It contains
        two elements, the x-coordinate and the y-coordinate of the object's position
        :param img: The `img` parameter is used to store the image associated with the object. It can be
        an image file path or an image object, depending on how it is used in the code
        :param speed: The speed parameter represents the speed at which the object will move. It can be
        a positive or negative value, indicating the direction and magnitude of the movement
        :param depth: The depth parameter represents the layering or stacking order of the object. It
        determines how objects are rendered on the screen, with objects with higher depth values
        appearing on top of objects with lower depth values
        """
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        """
        The function updates the position of an object by adding its speed to its current position.
        """
        self.pos[0] += self.speed

    def render(self, surf, offset=(0, 0)):
        """
        The `render` function takes a surface and an offset, and blits an image onto the surface at a
        position calculated based on the offset and the depth of the image.

        :param surf: The `surf` parameter is the surface on which the image will be rendered. It is the
        surface object that represents the display or a portion of it
        :param offset: The `offset` parameter is a tuple representing the x and y offsets for rendering
        the image. It is used to determine the position of the image on the surface (`surf`). The image
        will be rendered at `self.pos[0] - offset[0] * self.depth` on the x-axis
        """
        render_pos = (
            self.pos[0] - offset[0] * self.depth,
            self.pos[1] - offset[1] * self.depth,
        )
        surf.blit(
            self.img,
            (
                render_pos[0] % (surf.get_width() + self.img.get_width())
                - self.img.get_width(),
                render_pos[1] % (surf.get_height() + self.img.get_height())
                - self.img.get_height(),
            ),
        )


# The Clouds class is a blueprint for creating cloud objects.
class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds = []

        for i in range(count):
            self.clouds.append(
                Cloud(
                    (random.random() * 99999, random.random() * 99999),
                    random.choice(cloud_images),
                    random.random() * 0.06 + 0.13,
                    random.random() * 0.6 + 0.2,
                )
            )
            self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        """
        The function updates each cloud in a list of clouds.
        """
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset=(0, 0)):
        """
        The render function takes a surface and an offset as parameters and renders each cloud object
        onto the surface with the given offset.

        :param surf: The `surf` parameter is the surface object on which the clouds will be rendered. It
        is typically a pygame surface or any other surface object that supports rendering
        :param offset: The offset parameter is a tuple that specifies the x and y coordinates to offset
        the rendering of the clouds on the surface. This can be used to adjust the position of the
        clouds on the surface
        """
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)
