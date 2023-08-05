import os
import pygame

# from screeninfo import get_monitors


BASE_IMG_PATH = "data/images/"


# def get_monitor_size():
#     for monitor in get_monitors():
#         print(monitor)


def load_image(path) -> str:
    # print("\n\n\n", BASE_IMG_PATH + path + "\n\n\n")
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path) -> list:
    return [
        load_image(f"{path}/{img_name}")
        for img_name in sorted(os.listdir(BASE_IMG_PATH + path))
    ]


class Animation:
    def __init__(self, images, image_duration=5, loop=True):
        self.images = images
        self.image_duration = image_duration
        self.loop = loop
        self.done = False
        self.frame = 0
