import uuid

class EntityDefinition(object):
    def __init__(self):
        # Definitions is like: {def_name : list of component_cls}
        self.definitions = dict();

    def define(self, def_name, component_cls_lst):
        if def_name is not None and component_cls_lst is not None:
            self.definitions[def_name] = component_cls_lst;

    def undefine(self, def_name):
        if def_name in self.definitions:
            del self.definitions[def_name]

    def make(self, def_name, entity_rec):
        if def_name in self.definitions:
            component_cls_lst = self.definitions[def_name]
            for component_cls in component_cls_lst:
                if Component.is_registered(component_cls):
                    entity_rec.attach_component(Component.create(component_cls))
            return entity_rec


class EntityRecord(object):

    def __init__(self, name, entity_registry):
        self.name = name
        # components map : {name : component}
        self.components = dict()

        # Entity Registry
        self.entity_registry = entity_registry

    @property
    def name(self):
        return self.name

    def has_component(self, component):
        if component is not None:
            return component in self.components.values()

    def need_sync(self):
        """
        The entity is considered out-of-sync when it is not registered
        in a registery, and/or has no name
        """
        return (self.name is None or 
                self.entity_registry is None or
                not self.entity_registry.contains(self))

    def synchronize(self):
        if self.entity_registry is not None:
            if self.entity_registry.contains(self):
                self.entity_registry.enter(self)

    def add(self, component):
        if self.entity_registry is not None:
            self.entity_registry.add(self, component)


    def __str__(self):
        output_str = ""
        comps_dict = self.entity_registry.get_components(self)
        if comps_dict is not None and len(comps_dict) > 0:
            comps = comps_dict.values()
            s_lst = []
            for cp in comps:
                s = "{0},".format(str(cp))
                s_lst.append(s)

        return "".join(s_lst)


class Entity(object):

    # Entity Definitions {def_name : list_of_component_classes}
    _definitions = EntityDefinition()

    def create(name, entity_registry):
        entity_rec = EntityRecord(name, registery)

        entity_rec.synchronize()

        return entity_rec

    def create(components):
        return Entity.create(Entity.get_guid(), components)

    def create(name, components):
        return Entity.create(name, EntityRegistry.get_current(), components)

    def create(name, entity_registry, components):
        entity_rec = Entity.create(name, entity_registry)

        for cp in components:
            entity_rec.add(cp)

        return entity_rec

    def define(def_name, component_classes):
        _definitions.define(def_name, component_classes)

    def undefine(def_name):
        _definitions.undefine(def_name)

    def get_guid():
        return str(uuid.uuid())


class EntityRecordStore(object):
    def __init__(self):
        # { entity_record : {component_cls : component} }
        self.records = dict()

        # List of components need to be synced
        self._desynced_components = list()

        # Dictionary of the triggers and handlers
        # _triggers is a dictionary like {trigger_pred : event_handler}
        self._triggers = dict()

        # Handlers
        self.on_entity_entered = None
        self.on_entity_removed = None

    def enter(self, entity_rec):
        """
        Register an entity with no components
        """
        self.add(entity_rec, None)

    def drop(self, entity_rec):
        """
        Unregister an entity and returns 'True' if it was successfully
        dropped. 
        """
        if entity_rec is None:
            return False

        entity_dropped = False
        comps_dict = get_components(entity_rec)
        if comps_dict is not None and len(comps_dict) > 0:
            cp_instances = comps_dict.values()

            # Remove the components first
            for cp in cp_instances:
                self.remove(entity_rec, cp)

        # Remove the entity
        del records[entity_rec]
        entity_dropped = True

        self.on_removed(EntityEventArgs(entity_rec))

        return entity_dropped

    def add(self, entity_rec, component):
        """
        Attach a specific component to an entity
        """
        entity_registered = True
        component_attached = False

        # If there is an entity and not this one, remove it first
        if component is not None:
            old_owner = component.owner
            if old_owner is not None:
                if old_owner != entity_rec:
                    self.remove(old_owner, component)

        comps_dict = get_components(entity_rec)
        if comps_dict is None:
            comps_dict = dict()
            entity_registered = False
            self.records[entity_rec] = comps_dict
        
        if component is not None:
            cp_cls = type(component)
            if not entity_registered or cp_cls not in comps_dict:
                comps_dict[cp_cls] = component

                if component.owner is None or component.owner != entity_rec:
                    component.owner = entity_rec

                self.prepare_components_for_sync(component)

                component_attached = True

        if not entity_registered:
            self.on_entered(EntityEventArgs(entity_rec))

        return component_attached

    def remove(self, entity_rec, component):
        """
        Dettaches the specified component from an entity.
        Returns "True" if it was successfull.
        """
        if entity_rec is None or component is None:
            return False

        if component.owner is not None and component.owner != entity_rec:
            return False

        comp_removed = False
        comps_dict = get_components(entity_rec)
        if comps_dict is not None and len(comps_dict) > 0:
            comp_cls = type(component)

            if comp_cls in comps_dict:
                del comps_dict[comp_cls]
                comp_removed = True
        
        if component.owner is not None:
            component.owner = None

        self.prepare_components_for_sync(component)

        return comp_removed

    def on_entered(self, sync_event_args):
        if self.on_entity_entered is not None:
            self.on_entity_entered(sync_event_args)

    def on_removed(self, sync_event_args):
        if self.on_entity_removed is not None:
            self.on_entity_removed(sync_event_args)

    def get_components(self, entity_rec):
        components = dict()

        if entity_rec in self.records:
            components = self.records[entity_rec]

        return components

    def set_trigger(self, predicate, handler):
        self._triggers[predicate] = handler

    def clear_trigger(self, predicate):
        if predicate in self._triggers:
            del self._triggers

    def prepare_components_for_sync(self, component):
        """
        """
        if component not in self._desynced_components:
            self._desynced_components.append(component)

    def synchronize(self):
        if len(self._desynced_components) > 0:
            for trigger_pred in self._triggers.keys():
                comps = []
                for cp in self._desynced_components:
                    if trigger_pred(cp):
                        comps.append(cp)

                if len(comps) > 0:
                    self._triggers[trigger_pred](ComponentSyncEventArgs(comps))

            self._desynced_components.clear()

    def contains(self, entity_rec):
        return entity_rec in self.records


class EntityRegistry(object):

    _default_registry = EntityRecordStore()
    _active_registry = _default_registry

    def get_current():
        return _active_registry


class GemsBoard(object):
    '''
    The gems' borard defines the coordinate system for all the gems
    in this board. It contains the a group of cells that represents 
    a position in the board, in each cell, there could be any type of
    game elements such as gems, glasses or some blockers that cannot
    be eliminated.
    '''

    def __init__(self):
        self.cells = list()


class Cell(object):
    '''The cell is unit in a board.'''

    def __init__(self, board):
        self.board = board
        self.x = 0
        self.y = 0
        self.elements = list()


class Gem(object):

    def __init__(self, type_id, image):
        self.state = State()
        self.grid_pos_x = 0
        self.grid_pos_y = 0