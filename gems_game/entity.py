
class EntityDefinition(object):

    def __init__(self):
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

    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self.name


class EntityRecordStore(object):

    def __init__(self):
        """
        { entity_record : {component_type : component_cls} }
        """
        self.records = dict()

    def add(self, entity_rec, component):
        """
        Attach a specific component to an entity
        """
        if component is not None:
            old_owner = component.owner
            if old_owner is not None:
                if old_owner != entity_rec:
                    pass

    def remove(self, entity_rec, component):
        """
        Dettaches the specified component from an entity.
        Returns "True" if it was successfull.
        """
        if entity_rec is None or component is None:
            return False

        if component.owner is not None and component.owner != entity_rec:
            return False

        



    def get_components(self, entity_rec):
        components = dict()

        if entity_rec in self.records:
            components = self.records[entity_rec]

        return components

class Entity(object):

    def __init__(self):
        self.component_map = dict()

    def attach_component(sefl, component):
        pass

    def detach_component(self, name):
        pass

class GemsBoard(Entity):
    '''
    The gems' borard defines the coordinate system for all the gems
    in this board. It contains the a group of cells that represents 
    a position in the board, in each cell, there could be any type of
    game elements such as gems, glasses or some blockers that cannot
    be eliminated.
    '''

    def __init__(self):
        self.cells = list()


class Cell(Entity):
    '''The cell is unit in a board.'''

    def __init__(self, board):
        self.board = board
        self.x = 0
        self.y = 0
        self.elements = list()


class Gem(Entity):

    def __init__(self, type_id, image):
        self.state = State()
        self.grid_pos_x = 0
        self.grid_pos_y = 0