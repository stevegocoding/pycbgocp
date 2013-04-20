import cocos
from cocos.director import director

from utils import FPSSync
from entity import Entity
from component import Component

class ShootGameView(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(GemsGameView, self).__init__()

        imgs = {}
        imgs["player"] = pyglet.resource.image('player7.png')
        self.imgs = imgs

        self.fps_sync = FPSSync(30)

        self.schedule(self.process)

    def draw(self):
        print "draw"
        time.sleep(0.07)

    def process(self, t):
        i = self.fps_sync.get_frame_count(t)
        print ("sim times %d " %(i))

    def on_key_press(self, k, m):
        print("key pressed")

    def on_key_release(self, k, m):
        print("key released")

