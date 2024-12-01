from labs.lab5.ui.display import Display
from labs.lab5.dal.torus_renderer import TorusRenderer
from labs.lab5.ui.game_controller import GameController

def main():
    # Ініціалізація компонентів
    display = Display(700, 700, 20, 20, 20)
    renderer = TorusRenderer(display)
    game = GameController(display, renderer)
    # Запуск програми
    game.run()
