from labs.lab5.bll.Scene import Scene
from labs.lab5.bll.CameraWrapper import Camera
from labs.lab5.bll.FigureWrapper import FigureWrapper
from labs.lab5.bll.Controller import Controller
from labs.lab5.dal.Camera import CameraData
from labs.lab5.ui.Keyboard import KeyboardHandler
from labs.lab5.ui.Mouse import MouseHandler
from labs.lab5.ui.Ascii3DMenu import Ascii3DMenu
from shared.classes.DictJsonDataAccess import DictJsonDataAccess
from config.settings_paths import settings_path_lab5


def camera_create():
    settings = DictJsonDataAccess(settings_path_lab5)
    camera_default_settings = settings.get('camera_default_settings')
    position = camera_default_settings.get("default_position")
    target = camera_default_settings.get("default_target")
    up_vector = camera_default_settings.get("default_up_vector")
    pitch = camera_default_settings.get("default_pitch")
    yaw = camera_default_settings.get("default_yaw")
    fovy = camera_default_settings.get("default_fovy")
    aspect = camera_default_settings.get("default_aspect")
    z_near = camera_default_settings.get("default_z_near")
    z_far = camera_default_settings.get("default_z_far")
    return Camera(CameraData(position, target, up_vector, pitch, yaw, fovy, aspect, z_near, z_far))

def create_scene():
    scene = Scene()
    camera = camera_create()
    scene.set_camera(camera)
    cube = FigureWrapper.create('Cube')
    cube.translate(4, -2, 1)
    cube.set_color("Green")
    pyramid = FigureWrapper.create('Pyramid')
    pyramid.rotate(45, 0, 0)
    pyramid.scale(1.1, 1.5, 0.4)
    pyramid.set_color("Red")
    sphere = FigureWrapper.create('Sphere')
    sphere.translate(-1, 3, 5)
    sphere.set_color('Blue')
    scene.add_figure(cube)
    scene.add_figure(pyramid)
    scene.add_figure(sphere)
    return scene


def set_up(scene, settings_path):
    keyboard_handler = KeyboardHandler()
    mouse_handler = MouseHandler()
    controller = Controller(scene, keyboard_handler, mouse_handler, settings_path)
    return controller


def main(settings_path=settings_path_lab5):
    scene = create_scene()
    controller = set_up(scene, settings_path_lab5)
    menu = Ascii3DMenu(controller)
    menu.show()

if __name__ == '__main__':
    main()
