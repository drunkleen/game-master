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


def load_transparent_image(path) -> str:
    # print("\n\n\n", BASE_IMG_PATH + path + "\n\n\n")
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey((0, 0, 0))
    return img


def load_transparent_images(path) -> list:
    return [
        load_transparent_image(f"{path}/{img_name}")
        for img_name in sorted(os.listdir(BASE_IMG_PATH + path))
    ]


class Animation:
    def __init__(self, images, image_duration=5, loop=True):
        self.images = images
        self.image_duration = image_duration
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.image_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.image_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1 , self.image_duration * len(self.images) - 1)
            if self.frame >= self.image_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.image_duration)]
    