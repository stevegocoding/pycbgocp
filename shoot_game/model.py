import entity


class PlayerEntity(entity.EntityRecord):
    def __init__(self, name, entity_registry):
        entity.EntityRecord.__init__(self, name, entity_registry)

        self._renderer = self.get_


    def visit(self):
        self.process()
        self.render()

    def process(self):
        pass

    def render(self):
        pass