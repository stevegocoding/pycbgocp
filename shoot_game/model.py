import cocos

from entity import EntityRecord
from component import Component

class SceneComponent(Component):

    def __init__(self):
        self._sprite = cocos.sprite.Sprite(None)


class InputComponent(Component):

    def __init__(self):
        pass

class SpawnComponent(Component):

    def __init__(self):
        pass

class ZombieAIComponent(Component):
    def __init__(self):
        pass


class PlayerEntity(EntityRecord):

    def __init__(self):
        pass

    def shoot(self):
        pass

    def move(self):
        pass

class GameWorld(EntityRecord):

    def __init__(self):
        pass

class ZombieEntity(EntityRecord):

    def __init__(self):
        pass


class BulletEntity(EntityRecord):

    def __init__(self):
        pass