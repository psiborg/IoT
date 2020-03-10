# ========================================================================
# sprites.py
#
# Description: Sprites for the 8x8 LED matrix on the Sense HAT.
#
# Author: Jim Ing
# Date: 2020-02-22
# ========================================================================

class Sprites:
    def __init__(self):
        # Basic color palette
        W = (255, 255, 255) # White
        R = (255, 0, 0)     # Red
        G = (0, 255, 0)     # Green
        B = (0, 0, 255)     # Blue
        C = (0, 255, 255)   # Cyan
        M = (255, 0, 255)   # Magenta
        Y = (255, 255, 0)   # Yellow
        K = (0, 0, 0)       # Black

        self.blank = [
            K, K, K, K, K, K, K, K,
            K, K, K, K, K, K, K, K,
            K, K, K, K, K, K, K, K,
            K, K, K, K, K, K, K, K,
            K, K, K, K, K, K, K, K,
            K, K, K, K, K, K, K, K,
            K, K, K, K, K, K, K, K,
            K, K, K, K, K, K, K, K
        ]

        self.arrowUp = [
            K, K, K, W, W, K, K, K,
            K, K, W, W, W, W, K, K,
            K, W, W, W, W, W, W, K,
            W, W, W, W, W, W, W, W,
            K, K, W, W, W, W, K, K,
            K, K, W, W, W, W, K, K,
            K, K, W, W, W, W, K, K,
            K, K, W, W, W, W, K, K
        ]

        self.noentry = [
            K, K, R, R, R, R, K, K,
            K, R, R, R, R, R, R, K,
            R, R, R, R, R, R, R, R,
            R, W, W, W, W, W, W, R,
            R, W, W, W, W, W, W, R,
            R, R, R, R, R, R, R, R,
            K, R, R, R, R, R, R, K,
            K, K, R, R, R, R, K, K
        ]

        self.raspberry = [
            K, G, G, K, K, G, G, K,
            K, K, G, G, G, G, K, K,
            K, K, R, R, R, R, K, K,
            K, R, R, R, R, R, R, K,
            R, R, R, R, R, R, R, R,
            R, R, R, R, R, R, R, R,
            K, R, R, R, R, R, R, K,
            K, K, R, R, R, R, K, K
        ]

        self.smiley = [
            K, K, Y, Y, Y, Y, K, K,
            K, Y, Y, Y, Y, Y, Y, K,
            Y, Y, K, Y, Y, K, Y, Y,
            Y, Y, Y, Y, Y, Y, Y, Y,
            Y, Y, Y, Y, Y, Y, Y, Y,
            Y, Y, K, Y, Y, K, Y, Y,
            K, Y, Y, K, K, Y, Y, K,
            K, K, Y, Y, Y, Y, K, K
        ]

        # Pacman Ghosts

        self.blinky = [
            K, K, K, R, R, K, K, K,
            K, R, R, R, R, R, R, K,
            R, W, W, R, W, W, R, R,
            R, W, K, R, W, K, R, R,
            R, R, R, R, R, R, R, R,
            R, R, R, R, R, R, R, R,
            R, R, R, R, R, R, R, R,
            K, R, K, R, K, R, K, R
        ]

        self.pinky = [
            K, K, K, M, M, K, K, K,
            K, M, M, M, M, M, M, K,
            M, W, W, M, W, W, M, M,
            M, W, K, M, W, K, M, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
            K, M, K, M, K, M, K, M
        ]

        self.inky = [
            K, K, K, C, C, K, K, K,
            K, C, C, C, C, C, C, K,
            C, W, W, C, W, W, C, C,
            C, W, K, C, W, K, C, C,
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            K, C, K, C, K, C, K, C
        ]

        self.clyde = [
            K, K, K, Y, Y, K, K, K,
            K, Y, Y, Y, Y, Y, Y, K,
            Y, W, W, Y, W, W, Y, Y,
            Y, W, K, Y, W, K, Y, Y,
            Y, Y, Y, Y, Y, Y, Y, Y,
            Y, Y, Y, Y, Y, Y, Y, Y,
            Y, Y, Y, Y, Y, Y, Y, Y,
            K, Y, K, Y, K, Y, K, Y
        ]

        self.ghosts = [
            self.blinky,
            self.pinky,
            self.inky,
            self.clyde
        ]
