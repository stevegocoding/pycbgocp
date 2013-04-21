import cocos.layer
import cocos.batch
import component
import resource
import utils

resource.SpriteSheetResource.register_factory("imageatlas")
resource.SpriteSheetResource.register_factory("animation")


class SpriteSheetLayer(object):

    def __init__(self, renderer, resource, order_idx):
        self._name = "default_layer"
        self._renderer = renderer
        self._sprite_sheet = resource
        self._order_index = order_idx
        self._is_hidden = False

    def get_frames_count(self, state):
        if self._sprite_sheet is not None:
            return self._sprite_sheet.get_frames_count(state)
        else:
            return 0

    def get_frame_image(self, state, frame):
        if self._sprite_sheet is not None:
            frame_img = self._sprite_sheet.get_frame_image(state, frame)
            return frame_img
        else:
            return None

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self.name = value

    @property
    def order_indxe(self):
        return self._order_index

    @property
    def is_hidden(self):
        return self._is_hidden


class SpriteRenderer(component.Component):

    def __init__(self):
        self._current_state = "default"
        self._frame_index = 0
        self._max_frames = 0
        self._sprites_batch = cocos.batch.BactchNode()
        self._sprites = []
        self._layers = []
        self._layers_render = []
        self._loop = False
        self._animation_percent = 0
        self._aabb = cocos.rect.Rect()

    def create_layer(self, resource, order_index):
        layer = SpriteSheetLayer(self, resource, order_index)
        self._layers.append(layer)
        self.sort_layers()

    def reset_frame_data(self):
        for sprite in self._sprites:
            self._sprites_batch.remove(sprite)

        self._sprites = []
        self._max_frames = 0

    def reset_animation(self):
        self._frame_index = 0
        self._animation_percent = 0

    def update_frame(self, animation_ticks):
        self.reset_frame_data()
        self._max_frames = self.get_animation_frames_count()
        ticks = animation_ticks
        while ticks > 0:
            ticks -= 1
            self._frame_index += 1
            if self._frame_index >= self._max_frames:
                if self._loop is not True:
                    self._frame_index = self._max_frames - 1
                else:
                    self._frame_index = 0
                self._animation_percent = 100

        # Update the animation percentage
        percent = (self._frame_index / self._max_frames) * 100 if self._max_frames > 1 else 100
        if percent > self._animation_percent:
            self._animation_percent = percent

        # Build the array of images to draw in current state
        for layer in self._layers:
            if layer.is_hidden is not True:
                frame_img = layer.get_frame_image(self.current_state, self.current_frame)
                if frame_img is not None:
                    self._layers_render.append(layer)
                    sprite = cocos.sprite.Sprite(frame_img)
                    self._sprites.append(sprite)
                    self._sprites_batch.add(sprite)

    def render_frame(self):
        pass

    def sort_layers(self):
        if len(self._layers) > 1:
            self._layers.sort(key=lambda x: x.order_index)

    def get_animation_frames_count(self):
        max_frames = 0

        for layer in self._layers:
            if layer.is_hidden is not True:
                total_frames = layer.get_frames_count(self.current_state)

                if max_frames < total_frames:
                    max_frames = total_frames

        return max_frames

    def set_position(self, (x, y)):
        self.renderable_object.position = (x, y)

    @property
    def current_state(self):
        return self._current_state

    @property
    def current_frame(self):
        return self._frame_index

    @property
    def max_frames(self):
        return self._max_frames

    @property
    def renderable_object(self):
        return self._sprites_batch


class GameLayer(cocos.layer.Layer):
    def __init__(self):
        cocos.layer.Layer.__init__(self)
        self._fps_sync = utils.FPSSync(30)

        self.scheduled(self.process)

    def process(self, dt):
        self._fps_sync.update(dt)

    def visit(self):
        ticks = self._fps_sync.get_frame_count()
        if ticks <= 0:
            return 0

        cocos.layer.Layer.visit(self)