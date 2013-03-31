import os, sys
src_path = os.path.abspath('../')
sys.path.append(src_path)

import cocos
from cocos.director import director

from utils import *

import time

consts = {
    "window" : {
        "width" : 800,
        "height" : 600, 
        "vsync" : True,
        "resizable" : True
    }
} 

class GameObject(cocos.sprite.Sprite):
    IDLE_STATE = "idle_state"
    NAV_STATE = "nav_state"
    ATTACK_STATE = "attack_state"
    DEATH_STATE = "death_state"

    def __init__(self, img):
        super(GameObject, self).__init__(img)
        self.state = State()
        
        idle_state = State(GameObject.IDLE_STATE)
        idle_state.assign(
                        {
                        "process_func" : self.idle_process_handler,
                        "enter_func" : self.idle_enter_handler,
                        "exit_func": self.idle_exit_handler
                        })

        nav_state = State(GameObject.NAV_STATE)
        nav_state.assign(
                        {"process_func":self.nav_process_handler,
                        "enter_func":self.nav_enter_handler,
                        "exit_func":self.nav_exit_handler
                        })

        attack_state = State(GameObject.ATTACK_STATE)
        attack_state.assign(
                        {"process_func":self.attack_process_handler,
                        "enter_func":self.attack_enter_handler,
                        "exit_func":self.attack_exit_handler})

        death_state = State(GameObject.DEATH_STATE)
        death_state.assign(
                        {"process_func":self.death_process_handler,
                        "enter_func":self.death_enter_handler,
                        "exit_func":self.death_exit_handler})

        self.state.add_state(idle_state)
        self.state.add_state(nav_state)
        self.state.add_state(attack_state)
        self.state.add_state(death_state)

    def process():
        self.state.process()

    def idle_enter_handler(self, current_state):
        print "enter idle state"

    def idle_process_handler(self, current_state):
        print "process idle state"

    def idle_exit_handler(self, current_state):
        print "exit idle state"

    def nav_enter_handler(self, current_state):
        print "enter nav state"

    def nav_process_handler(self, current_state):
        print "process nav state"

    def nav_exit_handler(self, current_state):
        print "exit nav state"

    def attack_enter_handler(self, current_state):
        print "enter attack state"

    def attack_process_handler(self, current_state):
        print "process attack state"

    def attack_exit_handler(self, current_state):
        print "exit nav state"

    def death_enter_handler(self, current_state):
        print "enter death state"

    def death_process_handler(self, current_state):
        print "process death state"

    def death_exit_handler(self, current_state):
        print "exit death state"


class TestGameView(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(TestGameView, self).__init__()

        imgs = {}
        imgs["player"] = pyglet.resource.image('player7.png')
        self.imgs = imgs

        self.fps_sync = FixedStepLoop(self.process, 1.0/30, 1.0/10)
        self.fps_sync2 = FPSSync(30)

        self.schedule(self.process)

    def init_level(self):
        entity = GameObject(self.imgs["player"])
        self.add(entity, 0.4)

    def draw(self):
        print "draw"
        time.sleep(0.07)

    def update(self, T):
        output_str = "update() : dt = %f" %(T)
        print(output_str)

    def process(self, t):
        i = self.fps_sync2.get_frame_count(t)
        print ("sim times %d " %(i))

    def on_key_press(self, k, m):
        print("key pressed")

    def on_key_release(self, k, m):
        print("key released")


if __name__ == "__main__":

    # make a window
    director.init(**consts["window"])
    scene = cocos.scene.Scene()
    scene.add(cocos.layer.ColorLayer(0, 0, 0, 255), z=-1)
    game_view = TestGameView()
    scene.add(game_view, z=0)

    director.run(scene)