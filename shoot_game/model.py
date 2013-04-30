import entity
import graphics
import resource


if __name__ == "__main__":

    import cocos.director
    import cocos.layer

    consts = {
        "window" : {
            "width": 800,
            "height": 600,
            "vsync": True,
            "resizable": True
        }
    }

    cocos.director.director.init(**consts["window"])
    scene = graphics.GameScene()
    base_layer = cocos.layer.Layer()

    components = [graphics.SpriteRenderer]
    entity.Entity.define("TestPlayerDef", components)
    player = entity.Entity.create_from_def("TestPlayerDef", "player")

    # Load the resource
    spritesheet_res = resource.load_spritesheet("./asset/male_walkcycle.xml")
    sprite_renderer = entity.EntityRegistry.get_current().get_component(player, graphics.SpriteRenderer)
    sprite_renderer.create_layer(spritesheet_res, 0)
    sprite_renderer.renderable_object.position = (100, 100)
    base_layer.add(player)

    scene.add(base_layer, z=-1)
    scene.add_game_entity(player)

    cocos.director.director.run(scene)