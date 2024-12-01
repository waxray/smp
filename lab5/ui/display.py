import pygame
import colorsys

class Display:
    def __init__(self, width, height, pixel_width, pixel_height, font_size):
        self.resolution = self.width, self.height = width, height
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.screen_width = self.width // pixel_width
        self.screen_height = self.height // pixel_height
        self.screen_size = self.screen_width * self.screen_height
        self.font_size = font_size
        self.hue = 0

        pygame.init()
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption("Torus Simulation")
        self.font = pygame.font.SysFont('Arial', font_size, bold=True)
        self.clock = pygame.time.Clock()

    def hsv2rgb(self, h, s, v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

    def draw_char(self, char, x, y):
        text = self.font.render(str(char), True, self.hsv2rgb(self.hue, 1, 1))
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)

    def clear(self):
        self.screen.fill((0, 0, 0))

    def update(self):
        pygame.display.update()

    def increment_hue(self, amount):
        self.hue = (self.hue + amount) % 1
