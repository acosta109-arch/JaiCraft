from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time

app = Ursina()

Sky()

# BLOQUES DISPONIBLES POR URSINA
block_textures = {
    1: 'white_cube',
    2: 'brick',
    3: 'grass',
}

# BLOQUES DISPONIBLES DE MI PARTE
block_colors = {
    4: color.gray,
    5: color.brown,
    6: color.blue,
    7: color.green,
    8: color.red,
    9: color.yellow,
}

current_block = 1
is_flying = False
last_space_press = 0


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=None, color=color.white):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            texture=texture if texture else 'white_cube',
            color=color
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if current_block <= 3:
                    voxel = Voxel(position=self.position + mouse.normal, texture=block_textures[current_block])
                else:
                    voxel = Voxel(position=self.position + mouse.normal, color=block_colors[current_block])
            if key == 'right mouse down':
                destroy(self)


def start_game():
    menu.enabled = False
    game.enabled = True


def quit_game():
    application.quit()


menu = Entity(parent=camera.ui, model='quad', scale=(2, 2), color=color.brown, texture='white_cube', enabled=True)

start_button = Button(parent=menu, text='Iniciar Juego', scale=(0.3, 0.1), position=(0, 0.1), color=color.gray,
                      on_click=start_game)
quit_button = Button(parent=menu, text='Salir', scale=(0.3, 0.1), position=(0, -0.1), color=color.gray,
                     on_click=quit_game)

buttons = [start_button, quit_button]
current_button_index = 0

buttons[current_button_index].color = color.black

game = Entity(enabled=False)
for z in range(40):
    for x in range(40):
        voxel = Voxel(position=(x, 0, z), texture='grass')


def create_tree(x, z):
    for i in range(3):
        Voxel(position=(x, i + 1, z), texture='brick')
    for i in range(3):
        for j in range(3):
            Voxel(position=(x - 1 + i, 4, z - 1 + j), texture='white_cube')


create_tree(5, 5)
create_tree(15, 15)

player = FirstPersonController()

block_icons = []
total_blocks = 9
spacing = 0.12

for i in range(1, total_blocks + 1):
    x_position = (i - (total_blocks / 2)) * spacing
    if i <= 3:
        icon = Button(
            parent=camera.ui,
            model='cube',
            texture=block_textures[i],
            scale=(0.1, 0.1),
            position=(x_position, -0.45),
            color=color.green if i == current_block else color.white
        )
    else:
        icon = Button(
            parent=camera.ui,
            model='cube',
            scale=(0.1, 0.1),
            position=(x_position, -0.45),
            color=block_colors[i] if i != current_block else color.green
        )
    block_icons.append(icon)


def update_hotbar():
    for i, icon in enumerate(block_icons, 1):
        icon.color = color.green if i == current_block else color.white


def update():
    global current_block, is_flying, last_space_press, current_button_index

    # SELECIONAR LOS BLOQUES DEL 1 AL 9
    for i in range(1, 10):
        if held_keys[str(i)]:
            current_block = i
            update_hotbar()

    if held_keys['space'] and time.time() - last_space_press < 0.3:
        is_flying = not is_flying
    else:
        player.jump()
    last_space_press = time.time()

    if is_flying:
        if held_keys['space']:
            player.y += 4 * time.dt
        if held_keys['shift']:
            player.y -= 4 * time.dt
    else:
        if held_keys['shift']:
            player.y -= 4 * time.dt

    if player.y < -10:
        player.position = (player.x, 10, player.z)

    if held_keys['escape']:
        application.quit()


    if held_keys['down arrow']:
        buttons[current_button_index].color = color.gray
        current_button_index = (current_button_index + 1) % len(buttons)
        buttons[current_button_index].color = color.green
        time.sleep(0.1)

    if held_keys['up arrow']:
        buttons[current_button_index].color = color.gray
        current_button_index = (current_button_index - 1) % len(buttons)
        buttons[current_button_index].color = color.green
        time.sleep(0.1)

    if held_keys['enter']:
        buttons[current_button_index].on_click()
        time.sleep(0.1)


app.run()
