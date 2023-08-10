import os
import pygame

# from screeninfo import get_monitors


BASE_IMG_PATH = "data/images/"


# def get_monitor_size():
#     for monitor in get_monitors():
#         print(monitor)


def load_image(path) -> str:
    """
    The function `load_image` loads an image from a given path and sets the color key to (0, 0, 0).

    :param path: The `path` parameter is a string that represents the file path of the image that you
    want to load
    :return: an image object.
    """
    # print("\n\n\n", BASE_IMG_PATH + path + "\n\n\n")
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path) -> list:
    """
    The function `load_images` takes a path as input and returns a list of loaded images from that path.

    :param path: The `path` parameter is a string that represents the directory path where the images
    are located
    :return: The function `load_images` returns a list of loaded images.
    """
    return [
        load_image(f"{path}/{img_name}")
        for img_name in sorted(os.listdir(BASE_IMG_PATH + path))
    ]


def load_transparent_image(path) -> str:
    """
    The function `load_transparent_image` loads an image from a given path and sets the color key to
    make the image transparent.

    :param path: The `path` parameter is a string that represents the file path of the image that you
    want to load
    :return: an image object.
    """
    # print("\n\n\n", BASE_IMG_PATH + path + "\n\n\n")
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey((0, 0, 0))
    return img


def load_transparent_images(path) -> list:
    """
    The function `load_transparent_images` loads a list of transparent images from a specified path.

    :param path: The `path` parameter is a string that represents the directory path where the
    transparent images are located
    :return: a list of transparent images that are loaded from the specified path.
    """
    return [
        load_transparent_image(f"{path}/{img_name}")
        for img_name in sorted(os.listdir(BASE_IMG_PATH + path))
    ]


# The Animation class is a blueprint for creating animated objects in Python.
class Animation:
    def __init__(self, images, image_duration=5, loop=True):
        """
        The function initializes an object with a list of images, an image duration, a loop flag, a done
        flag, and a frame counter.

        :param images: The `images` parameter is a list of images that will be displayed or processed in
        some way. Each element in the list represents an image
        :param image_duration: The `image_duration` parameter is the duration (in seconds) for which
        each image should be displayed, defaults to 5 (optional)
        :param loop: The "loop" parameter determines whether the animation should loop or not. If set to
        True, the animation will continue to play in a loop. If set to False, the animation will play
        only once and then stop, defaults to True (optional)
        """
        self.images = images
        self.image_duration = image_duration
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        """
        The function `copy` returns a new instance of the `Animation` class with the same images, image
        duration, and loop value.
        :return: The method is returning an instance of the Animation class.
        """
        return Animation(self.images, self.image_duration, self.loop)

    def update(self):
        """
        The function updates the frame of an animation, taking into account whether the animation should
        loop or not.
        """
        if self.loop:
            self.frame = (self.frame + 1) % (self.image_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.image_duration * len(self.images) - 1)
            if self.frame >= self.image_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        """
        The function returns an image based on the current frame and image duration.
        :return: an image from a list of images based on the current frame and image duration.
        """
        return self.images[int(self.frame / self.image_duration)]
