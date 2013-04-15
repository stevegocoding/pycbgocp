import os, sys
src_path = os.path.abspath('../')
sys.path.append(src_path)

from entity import EntityDefinition
from entity import Entity
from entity import EntityRecord
from entity import EntityRecordStore
from entity import EntityRegistry

from component import Component


class HealthComponent(Component):
    pass


class ShootComponent(Component):
    pass


class SpawnComponent(Component):
    pass

if __name__ == "__main__":
    player_comps = [HealthComponent, ShootComponent]
    monster_comps = [HealthComponent, SpawnComponent]
    Entity.define("Player", player_comps)
    Entity.define("Monster", monster_comps)

    player_entity = Entity.create_from_def("Player", "You")
    monster_entity = Entity.create_from_def("Monster", "boos1")

    print str(player_entity)
    print str(monster_entity)

    player_cps = EntityRegistry.get_current().get_components(player_entity)

    print player_cps