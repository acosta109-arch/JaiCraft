from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

block_texture = 'white_cube'

class Voxel(Button):
    def __init__(self, position=(0,0,0), color=color.white):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            textture = block_texture,
            color = color
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                voxel = Voxel(position=self.position + mouse.normal, color=color.green)
            if key == 'right mouse down':
                destroy(self)

for z in range(25):
    for x in range(25):
        voxel = Voxel(position=(x,0,z))

def update():
    if held_keys['escape']:
        application.quit()

player = FirstPersonController()

app.run()