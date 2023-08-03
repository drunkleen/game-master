import pygame

BASE_IMG_PATH = "data/images/"


def load_image(path):
    # print("\n\n\n", BASE_IMG_PATH + path + "\n\n\n")
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img
