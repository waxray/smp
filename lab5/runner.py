from shared.interfaces.runner_interface import RunnerInterface
from labs.lab5.main import main

class Runner(RunnerInterface):
    @staticmethod
    def run():
        main()

if __name__ == '__main__':
    Runner().run()