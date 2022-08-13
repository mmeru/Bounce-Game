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
"""Game objects to create PyGame based games."""

import os
import sys
import pygame
from game import rgbcolors
from game.scene import (
    EmptyPressAnyKeyScene,
    BlinkingTitle,
    BouncingBallsScene,
    SplashScene,
)


def display_info():
    """Print out information about the display driver and video information."""
    print(f'The display is using the "{pygame.display.get_driver()}" driver.')
    print('Video Info:')
    print(pygame.display.Info())


class VideoGame:
    """Base class for creating PyGame games."""

    def __init__(
        self,
        window_width=800,
        window_height=800,
        window_title='My Awesome Game',
    ):
        """Initialize a new game with the given window size and \
            window title."""
        pygame.init()
        self._window_size = (window_width, window_height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._window_size)
        self._title = window_title
        pygame.display.set_caption(self._title)
        self._game_is_over = False
        if not pygame.font:
            print("Warning, fonts disabled")
        if not pygame.mixer:
            print("Warning, sound disabled")
        self._scene_graph = []

    @property
    def scene_graph(self):
        """Return the scene graph representing all the scenes in the game."""
        return self._scene_graph

    def build_scene_graph(self):
        """Build the scene graph for the game."""
        self._scene_graph.append(
            EmptyPressAnyKeyScene(self._screen, rgbcolors.orange)
        )

    def run(self):
        """Run the game; the main game loop."""
        while not self._game_is_over:
            for scene in self.scene_graph:
                scene.start_scene()
                while scene.is_valid():
                    self._clock.tick(scene.frame_rate())
                    for event in pygame.event.get():
                        scene.process_event(event)
                    scene.update_scene()
                    scene.draw()
                    scene.render_updates()
                    pygame.display.update()
                scene.end_scene()
            self._game_is_over = True
        pygame.quit()
        sys.exit(0)


class BounceDemo(VideoGame):
    """Bouncing balls demo."""

    def __init__(self, num_balls):
        """Init the bouncing balls demo."""
        super().__init__(window_title='Bouncing Balls')
        self._main_dir = os.path.split(os.path.abspath(__file__))[0]
        self._data_dir = os.path.join(self._main_dir, 'data')
        print(f"Our main directory is {self._main_dir}")
        print(f"Our data directory is {self._data_dir}")
        self._num_balls = num_balls

    def build_scene_graph(self):
        """Bouncing balls scene graph."""
        # Feel free to change the soundtrack and to use different
        # soundtracks for the different scenes.
        soundtrack = os.path.join(
            self._data_dir, '09 - Warm Rays, Good Waves.mp3'
        )
        credits_string = 'Sound Effects: Monkey.aiff and \
            Boing.aiff from Mac OS 7. \
            Soundtrack: Jack Pearcy, "Warm Rays, Good Waves", \
                Deep Lake Records. \
                Images: explosion1.gif from Pygame. \
                    \nSkeleton code provided by Michael Shafae. \
                    \nCompleted by Moses Merugu. \nCPSC 386.'
        self._scene_graph = [
            BlinkingTitle(
                self._screen,
                self._title,
                rgbcolors.green,
                72,
                rgbcolors.yellow,
                soundtrack,
            ),
            BouncingBallsScene(
                self._num_balls, self._screen, rgbcolors.black, 60, soundtrack
            ),
            SplashScene(self._screen, credits_string, soundtrack),
        ]

    def run(self):
        """Run the bouncing balls pygame demo."""
        super().run()
