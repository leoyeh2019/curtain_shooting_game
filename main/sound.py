import pygame
from os import path

pygame.init()
pygame.mixer.init()

music_dir = path.join(path.dirname(__file__), "music")

bullet_SE_list = []


for i in range(1, 4):
    SE = pygame.mixer.Sound(path.join(music_dir, 'se_bullet_{}.wav'.format(i)))
    SE.set_volume(0.1)
    bullet_SE_list.append(SE)