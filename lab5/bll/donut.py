import os
import pygame
from math import sin, cos
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


class TorusRenderer:
    def __init__(self, display):
        self.display = display
        self.A = 0
        self.B = 0
        self.R1 = 10
        self.R2 = 40
        self.K2 = 400
        self.K1 = self.display.screen_height * self.K2 * 3 / (8 * (self.R1 + self.R2))
        self.chars = ".,-~:;=!*#$@"

    def calculate_frame(self):
        output = [' '] * self.display.screen_size
        zbuffer = [0] * self.display.screen_size

        theta_spacing = max(2, int(1000 / ((self.display.screen_width + self.display.screen_height) / 2)))
        phi_spacing = max(2, int(100 / ((self.display.screen_width + self.display.screen_height) / 2)))

        for theta in range(0, 628, theta_spacing):
            for phi in range(0, 628, phi_spacing):
                cosA, sinA = cos(self.A), sin(self.A)
                cosB, sinB = cos(self.B), sin(self.B)
                costheta, sintheta = cos(theta), sin(theta)
                cosphi, sinphi = cos(phi), sin(phi)

                circlex = self.R2 + self.R1 * costheta
                circley = self.R1 * sintheta

                x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
                y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
                z = self.K2 + cosA * circlex * sinphi + circley * sinA

                if z == 0:
                    continue
                ooz = 1 / z

                xp = int(self.display.width / 2 / self.display.pixel_width + self.K1 * ooz * x)
                yp = int(self.display.height / 2 / self.display.pixel_height - self.K1 * ooz * y)

                if 0 <= xp < self.display.screen_width and 0 <= yp < self.display.screen_height:
                    position = xp + self.display.screen_width * yp
                    L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (
                        cosA * sintheta - costheta * sinA * sinphi)

                    if ooz > zbuffer[position]:
                        zbuffer[position] = ooz
                        luminance_index = int(L * 8)
                        output[position] = self.chars[max(0, luminance_index)]

        return output

    def rotate(self, dA, dB):
        self.A += dA
        self.B += dB


class GameController:
    def __init__(self, display, renderer):
        self.display = display
        self.renderer = renderer
        self.running = True
        self.paused = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.renderer.rotate(-0.05, 0)
        if keys[pygame.K_DOWN]:
            self.renderer.rotate(0.05, 0)
        if keys[pygame.K_LEFT]:
            self.renderer.rotate(0, -0.05)
        if keys[pygame.K_RIGHT]:
            self.renderer.rotate(0, 0.05)
        if keys[pygame.K_c]:
            self.display.increment_hue(0.01)

    def run(self):
        while self.running:
            self.display.clock.tick(60)
            self.handle_events()
            self.handle_input()

            if not self.paused:
                self.display.clear()
                frame = self.renderer.calculate_frame()

                x_pixel, y_pixel, k = 0, 0, 0
                for i in range(self.display.screen_height):
                    y_pixel += self.display.pixel_height
                    for j in range(self.display.screen_width):
                        x_pixel += self.display.pixel_width
                        self.display.draw_char(frame[k], x_pixel, y_pixel)
                        k += 1
                    x_pixel = 0

                self.display.update()


if __name__ == "__main__":
    display = Display(700, 700, 20, 20, 20)
    renderer = TorusRenderer(display)
    game = GameController(display, renderer)
    game.run()
