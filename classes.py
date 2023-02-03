from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QWidget
import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('../API_Yandex_maps/image', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    # if colorkey is not None:
    #     image = image.convert()
    #     if colorkey == -1:
    #         colorkey = image.get_at((0, 0))
    #     image.set_colorkey(colorkey)
    # else:
    #     image = image.convert_alpha()

    return image



class Check_box(pygame.sprite.Sprite):
    image_checked = load_image("checked.png")
    image_not_checked = load_image("not_checked.png")
    ischecked = False

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Check_box.image_not_checked
        self.rect = self.image.get_rect()
        self.rect.x = 450 - 25
        self.rect.y = 550 - 25

    def update(self, *args):
        x, y = args[0]
        if self.rect.x < x < self.rect.x + 20 and self.rect.y < y < self.rect.y + 20:
            Check_box.ischecked = not Check_box.ischecked
            self.image = Check_box.image_checked if Check_box.ischecked else Check_box.image_not_checked
