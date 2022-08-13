# Moses Merugu
# CPSC 386-03
# 2022-05-09
# mmeru@csu.fullerton.edu
# @mmeru
#
# Lab 04-00
#
# Bounce with pygame!
#
"""Demonstrate how to use sprite sheets to \
    perform some simple animations in PyGame."""

import os.path
import pygame

# Adapted aliens.py in pygame/examples
# https://github.com/pygame/pygame/blob/main/examples/aliens.py


class Explosion(pygame.sprite.Sprite):
    """Play an explosion sprite."""

    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'data')
    # Feel free to use a different explosion. It needs to be an animated
    # GIF or a sprite sheet.
    image_path = os.path.join(data_dir, 'explosion1.gif')

    defaultlife = 12
    animcycle = 3
    images = []

    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        try:
            surface = pygame.image.load(Explosion.image_path)
        except pygame.error as pygame_error:
            raise SystemExit(
                f'Could not load image "{Explosion.image_path}" \
                    {pygame.get_error()}'
            ) from pygame_error
        img = surface.convert()
        if not Explosion.images:
            Explosion.images = [img, pygame.transform.flip(img, 1, 1)]
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.center)
        self.life = Explosion.defaultlife

    def update(self):
        """Update the animation."""
        self.life = self.life - 1
        self.image = self.images[self.life // Explosion.animcycle % 2]
        if self.life <= 0:
            self.kill()
