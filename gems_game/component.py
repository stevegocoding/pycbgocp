
class Component(object):

    _allocated_id = 0
    _components_registry = dict(); 

    def __init__(self):
        pass

    def draw(self):
        pass

    def process(self):
        pass

    def on_attached(self, params):
        pass

    def on_removed(self, params):
        pass

    def create(component_cls):
        return component_cls()

    def regiter(component_cls):
        if Component.is_registered(component_cls) is not True:
            _components_registry[_allocated_id] = component_cls
            _allocated_id += 1

    def is_registered(component_cls):
        return component_cls in _components_registry.values()

class RenderComponent(Component):
    '''Rendering component for all game objects'''

    def __init__(self, entity, x, y, sprite):

        self.x = x
        self.y = y
        self.sprite = sprite
        self.owner = entity