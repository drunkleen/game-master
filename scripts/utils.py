import os
import pygame

BASE_IMG_PATH = "data/images/"


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
