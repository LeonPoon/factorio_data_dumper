

import os
from os import path
from .files import Filesystem


class DifficultyLevel(object):
    pass


class Difficulty(object):
    expensive = None

    def __init__(self):
        self.normal = DifficultyLevel()


class RecipeDifficulty(Difficulty):
    pass


class TechnologyDifficulty(Difficulty):
    pass


class DifficultySettings(object):
    def __init__(self):
        self.recipe_difficulty = RecipeDifficulty()
        self.technology_difficulty = TechnologyDifficulty()


class FactorioDefines(object):
    def __init__(self):
        self.difficulty_settings = DifficultySettings()
        self.direction = {'north': 'NORTH', 'east': 'E', 'south': 'SOUTH', 'west': 'W'}


class Factorio(object):
    def __init__(self):
        self.defines = FactorioDefines()

    def setup_lua(self, runtime):
        runtime.eval('function(d) defines = d end')(self.defines)


class DataFilesystem(Filesystem):
    def __init__(self, data_path=None):
        super(DataFilesystem, self).__init__(data_path
                                             or ('%s/.steam/steam/steamapps/common/Factorio/data' % os.environ['HOME']))


class Mod(object):
    def __init__(self, fs, mod_name):
        self.mod_name = mod_name
        self.fs = fs

    def get_lua_modules(self):
        return []


class ModsContext(object):
    def __init__(self):
        pass


class ModEvaluator(object):

    def __init__(self, mods, mod):
        self.mods = mods
        self.mod = mod

    def get_lua_searches(self):
        return [self.mod.fs.path
                , path.join(self.mod.fs.path, self.mod.mod_name)
                , path.join(self.mod.fs.path, self.mod.mod_name, 'lualib')
                ]

    def get_lua_modules(self):
        return self.mod.get_lua_modules() + ['%s/data' % self.mod.mod_name] + (
            ['%s/data-update' % self.mod.mod_name] if path.exists(path.join(self.mod.fs.path,
                                                                            self.mod.mod_name, 'data-update.lua'))
            else []
        )


class BaseMod(Mod):
    def __init__(self, data):
        super(BaseMod, self).__init__(data, 'base')


class CoreMod(Mod):
    def __init__(self, data):
        super(CoreMod, self).__init__(data, 'core')

    def get_lua_modules(self):
        return ['lualib/dataloader']
