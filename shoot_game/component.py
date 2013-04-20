
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
    _components_registry = dict()

    def __init__(self):
        """
        The entity that this component is currently attached on
        """
        self.owner = None
        self._previous_owner = None

        self.on_component_attached = None
        self.on_component_detached = None

    def draw(self):
        pass

    def process(self):
        pass

    def on_attached(self, state_event_args):
        if self.on_component_attached is not None:
            self.on_component_attached(state_event_args)

    def on_detached(self, state_event_args):
        if self.on_component_dettached is not None:
            self.on_component_dettached(state_event_args)

    def need_sync(self):
        """
        The component is considered out-of-sync if it is not attached
        to any entity
        """
        return self.owner is None or self.owner.has_component(self)

    @property
    def owner(self):
        return self.__getattr__("owner")

    @owner.setter
    def owner(self, value):
        require_sync = (self._previous_owner is not None and 
                        self._previous_owner.has_component(self))

        if require_sync:
            raise Exception("Component has to be synchronized before further\
                            changes can happen")
        else:
            if self.owner is None or self.owner != value:
                self.__setattr__("_previous_owner", self.owner)
                self.__setattr__("owner", value)

                state_change_event = \
                    ComponentStateEventArgs(self.owner, self._previous_owner)

                if self.owner is not None:
                    self.on_attached(state_change_event)
                else:
                    self.on_dettached(state_change_event)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __getattr__(self, name):
        return self.__dict__[name]

    @classmethod
    def create(cls, component_cls):
        return component_cls()

    @classmethod
    def register(cls, component_cls):
        if Component.is_registered(component_cls) is not True:
            Component._components_registry[Component._allocated_id] = component_cls
            Component._allocated_id += 1

    @classmethod
    def is_registered(cls, component_cls):
        return component_cls in Component._components_registry.values()

    def __str__(self):
        output_str = "{0} : {1}".format(type(self).__name__, "*" if self.need_sync else "")
        return output_str