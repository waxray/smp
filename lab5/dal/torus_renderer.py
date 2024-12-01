from math import sin, cos

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
