import rumps
import requests
import os
import json

class Light(object):

    def __init__(self, base_url, device_id):
        self.base_url = base_url
        self.device_id = device_id

    def on(self):
        self.set_level(255)

    def off(self):
        self.set_level(0)

    def full(self):
        self.set_level(99)

    def set_level(self, level):
        requests.get("%s/devices[%d].instances[0].commandClasses[0x26].Set(%d)" % (
            self.base_url, self.device_id, level), timeout=0.4)


class AllOfTheLights(rumps.App):

    def __init__(self, config_path):
        self.base_url = ""
        self.lights = {}
        self.scenes = {}
        self.config_path = self.expand_path(config_path)
        self.config = self.load_config(self.config_path)
        self.configure()

    def activate_scene(self, scene_id):
        if not scene_id in self.scenes:
            rumps.alert(title="No such scene.", message="Looks like that scene is missing!", ok=None, cancel="Abort")
        for light_name, value in self.scenes[scene_id].iteritems():
            if light_name.startswith('__'):
                continue
            self.lights[light_name].set_level(value)

    @rumps.clicked("Edit Config...")
    def edit_config(self, _):
        # use bash to load editor with ~/.allthelights.json
        os.system("bash -c \"$EDITOR {config_path}\"".format(config_path=self.config_path))

    def configure(self):
        menus = []

        # configure base_url
        self.base_url = self.config["base_url"]

        # configure lights
        for name, device_id in self.config["lights"].iteritems():
            self.lights[name] = Light(self.base_url, device_id)

        def scene_activator(self, scene_id):
            def activate(_):
                self.activate_scene(scene_id)
            return activate

        # configure scenes
        for scene in self.config["scenes"]:
            if not '__scenes__' in scene:
                # non-submenu
                scene_name = scene['__name__']
                scene_id = scene_name
                menus.append(scene_name)
                # add handler for click
                self.scenes[scene_id] = scene
                rumps.clicked(scene_name)(scene_activator(self, scene_id))
            else:
                for subscene in scene['__scenes__']:
                    # submenu
                    scene_name = scene['__name__']
                    subscene_name = subscene['__name__']
                    scene_id = "%s__%s" % (scene_name, subscene_name)

                    if scene_name in menus:
                        menus[menus.index(scene_name)] = [scene_name, [subscene_name]]
                    else:
                        added = False
                        for menu in menus:
                            if isinstance(menu, list) and menu[0] == scene_name:
                                menu[1].append(subscene_name)
                                added = True
                        if not added:
                            menus.append([scene_name, [subscene_name]])
                        
                    # add click handler
                    self.scenes[scene_id] = subscene
                    rumps.clicked(scene['__name__'], subscene['__name__'])(scene_activator(self, scene_id))

        menus.append(rumps.separator)
        menus.append(rumps.MenuItem("Edit Config...", key='e'))

        # activate the app
        super(AllOfTheLights, self).__init__(type(self).__name__, menu=menus, 
            quit_button=rumps.MenuItem('Quit', key='q'))
        self.icon = 'icon.png'

    def expand_path(self, basepath):
        basepath = os.path.normpath(basepath)
        basepath = os.path.expanduser(basepath)
        basepath = os.path.expandvars(basepath)
        return basepath

    def load_config(self, path):
        config = {}
        # load the JSON config file
        try:
            fh = open(path, 'r')
            json_data = fh.read()
            config = json.loads(json_data)
            fh.close()
        except Exception, e:
            rumps.alert(title="Config Error", message=str(e), ok="Okie :)", cancel=None)
            os.exit(1)

        return config


if __name__ == '__main__':
    AllOfTheLights("~/.allofthelights.json").run()
