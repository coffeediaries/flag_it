from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import random 

app = Ursina()
random.seed(0)
Entity.default_shader = lit_with_shadows_shader

ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-0.5, speed=8, position = (-28,0,25))
player.collider = MeshCollider(player, Vec3(0,1,0), Vec3(1,2,1))

flag = Entity(model='cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.red)
count = 0
shootables_parent = Entity(model = 'flag (1).glb')
mouse.traverse_target = shootables_parent

def input(key): # options for maps
    if key == '1':
        ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))
        #map 1
        wall = Entity(model='cube', origin_y=-.5, texture='brick', texture_scale=(1,2),
                x=0,
                z=30,
                scale_x = 65,
                scale_y = 50,
                Collision = 'box',
                color=color.hsv(0, 0, random.uniform(.9, 1))
                )
        wall = Entity(model='cube', origin_y=-.5, texture='brick', texture_scale=(1,2),
                x=30,
                z=0,
                scale_z = 65,
                scale_y = 50,
                Collision = 'box',
                color=color.hsv(0, 0, random.uniform(.9, 1))
                )
        wall = Entity(model='cube', origin_y=-.5, texture='brick', texture_scale=(1,2),
                x=-30,
                z=0,
                scale_z = 65,
                scale_y = 50,
                Collision = 'box',
                color=color.hsv(0, 0, random.uniform(.9, 1))
                )
        wall = Entity(model='cube', origin_y=-.5, texture='brick', texture_scale=(1,2),
                x=0,
                z=-30,
                scale_x = 65,
                scale_y = 50,
                Collision = 'box',
                color=color.hsv(0, 0, random.uniform(.9, 1))
                )
        z3 = []
        def maze_generator():
            global z3
            x1 = []
            z1 = []
            for i in range(10):
                if i % 2 == 0:
                    s = random.randint(-25,-20)
                else:
                    s = random.randint(25,30)
                p = random.randint(-25, -5)
                while (p % 5 != 0) and (p not in z1):
                    p = random.randint(-25, -5)
                z1.append(p)
                Entity(
                    model='cube',
                    origin_y=-.5,
                    texture='brick',
                    texture_scale=(1, 2),
                    x=s,
                    z=z1[i],
                    scale_x=45,
                    scale_y=50,
                    color=color.hsv(0, 0, random.uniform(.9, 1))
                )
            z2 = []
            for i in range(10):
                if i % 2 == 0:
                    s = random.randint(-25,-20)
                else:
                    s = random.randint(25,30)
                p = random.randint(5, 25)
                while (p % 5 != 0) and (p not in z2):
                    p = random.randint(5, 25)
                z2.append(p)
                Entity(
                    model='cube',
                    origin_y=-.5,
                    texture='brick',
                    texture_scale=(1, 2),
                    x=s,
                    z=z2[i],
                    scale_x=45,
                    scale_y=50,
                    color=color.hsv(0, 0, random.uniform(.9, 1))
                )
            z3 = x1 + z1
        map = maze_generator()
        # Flag()
        for i in range(10):
            enemies = Flag(position = (random.randint(-30,30),0,random.randint(-30,30)))
    elif key == '2': # map 2
        ground = Entity(model='plane', collider='box', scale=100, texture='grass', texture_scale=(4,4))
        model = Entity(model = "Ingenious Bojo-Elzing.glb", positio=(0,0,0), Collider = 'mesh')
        # Flag()
        for i in range(10):
            enemies = Flag(position = (random.randint(-30,30),0,random.randint(-30,30)))
def update():
    if held_keys['left mouse']:
        capture()

def capture(): # capturing a flag 
    if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
        mouse.hovered_entity.hp -= 5

from ursina.prefabs.health_bar import HealthBar

class Flag(Entity): # healthbar of flag
    def __init__(self, **kwargs):
        super().__init__(parent = shootables_parent, model='cube', origin_y=-.5, color=color.light_gray, collider='box', **kwargs)
        self.health_bar = Entity(parent = self, y=1.2, model='cube', color=color.red, world_scale=(1.5,.1,.1))
        self.max_hp = 100
        self.hp = self.max_hp
        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)
        self.look_at_2d(player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 30, ignore=(self,))
    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        global count
        self._hp = value
        if count == 10:  # if 10 flags turn red
            t = Text("You Win!", position=(0, 0))  # Display "You Win!" text
        if value <= 0:
            self.color = color.red
            count += 1
            return
        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1
def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled
        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        flag.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position
        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)

sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

app.run()
