
class ComponentSyncTriggerPred(object):
    
    def __init__(self, component_cls):
        self.cp_cls = component_cls

    def __call__(self, component):
        if component is not None:
            return isinstance(component, self.cp_cls)
        else:
            return False


class Component(object):

    _allocated_id = 0
    _components_registry = dict(); 

    def __init__(self):
        """
        The entity that this component is currently attached on
        """
        self.owner = None

    def draw(self):
        pass

    def process(self):
        pass

    def on_attached(self, params):
        pass

    def on_removed(self, params):
        pass

    def need_sync(self):
        """
        The component is considered out-of-sync if it is not attached
        to any entity
        """
        return self.owner is None or self.owner.has_component(self)

    @property
    def owner(self):
        return self.owner

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