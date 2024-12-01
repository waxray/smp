import pygame

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
