import events3d
import mh
import gui3d
import random
from typing import List
from lib import camera
import mhmain
import sys
from .humanstate import HumanState
from .randomizationsettings import RandomizationSettings
from . import mh2opengl

import sys, os

ROOT_PATH = os.path.dirname(sys.modules['__main__'].__file__)
sys.path.append(os.path.join(ROOT_PATH, "plugins"))
print("sys.path", sys.path)
sides = {
    "FRONT": [0, 0, 0],
    "BACK": [0, 180, 0],
    "LEFT": [0, -90, 0],
    "RIGHT": [0, 90, 0],
    "TOP": [90, 0, 0],
    "BOTTOM": [-90, 0, 0],
}


class Sides:
    FRONT = [0, 0, 0]
    BACK = [0, 180, 0]
    LEFT = [0, -90, 0]
    RIGHT = [0, 90, 0]
    TOP = [90, 0, 0]
    BOTTOM = [-90, 0, 0]


class ModelFormats:
    MHM = "MHM"
    OBJ = "OBJ"
    DAE = "DAE"
    FBX = "FBX"
    MHX = "MHX"
    MHX2 = "MHX2"


class ImageFormat:
    PNG = "png"


class BodyHandler:

    def __init__(self, settings: RandomizationSettings = None):
        self._set_globals()
        self.settings: RandomizationSettings = settings
        self.human_state: HumanState = HumanState()
        self.mhapi: gui3d.app.mhapi = gui3d.app.mhapi
        self.actual_side: List[int] = Sides.FRONT
        self.set_side(self.actual_side)

    def set_settings(self, settings: RandomizationSettings = None):
        self.settings: RandomizationSettings = settings

    def randomize(self):
        self.human_state: HumanState = HumanState(self.settings)

    def _set_globals(self):
        self._global_orbital_camera: camera.OrbitalCamera = globals()["mh"].OrbitalCamera
        self._global_app: mhmain.MHApplication = globals()["mh"].G.app

    def set_side(self, side: List[int]):
        if len(side) != 3:
            raise ValueError("Argument must contain exactly 3 values")

        # self._background.setSelectedSideCheckbox(side)
        self._global_app.axisView(side)
        self.actual_side = side
        # self._global_orbital_camera.translation

    def render(self, settings: dict, filename: str, render_format: str = ImageFormat.PNG):
        mh2opengl.Render(settings, filename + ".png", 'PNG')

    def produce(self, filename: str, model_format: str = ModelFormats.MHM):
        # format = self.randomizationSettings.getValue("output", "fileformat")

        if model_format == "MHM":
            path = self.mhapi.locations.getUserHomePath("models")
            if not os.path.exists(path):
                os.makedirs(path)
            filename = filename + ".mhm"
            self.human_state.human.save(os.path.join(path, filename))

        if model_format == "OBJ":
            self.mhapi.exports.exportAsOBJ(filename + ".obj")
        if model_format == "DAE":
            self.mhapi.exports.exportAsDAE(filename + ".dae")
        if model_format == "FBX":
            self.mhapi.exports.exportAsFBX(filename + ".fbx")
        if model_format == "MHX2" or model_format == "MHX":
            self.mhapi.exports.exportAsMHX2(filename + ".mhx2")

    def add_rotation(self, dx: int, dy: int, dz: int):
        self.actual_side = [self.actual_side[0] + dx,
                            self.actual_side[1] + dy,
                            self.actual_side[2] + dz]

    def apply_random_angle(self, side: str):
        if (side == "front"):
            f_dx: int = int(self.settings.getValue("render", "frontDx"))
            f_dy: int = int(self.settings.getValue("render", "frontDy"))
            f_dz: int = int(self.settings.getValue("render", "frontDz"))

            self.add_rotation(random.randrange(-f_dx, f_dx),
                              random.randrange(0, f_dy),
                              random.randrange(-f_dz, f_dz))
            self.set_side(self.actual_side)

        if side == "side":
            s_dx = int(self.settings.getValue("render", "sideDx"))
            s_dy = int(self.settings.getValue("render", "sideDy"))
            s_dz = int(self.settings.getValue("render", "sideDz"))

            print(s_dx, s_dy, s_dz)
            self.add_rotation(random.randrange(-s_dx, s_dx),
                              random.randrange(0, s_dy),
                              random.randrange(-s_dz, s_dz))
