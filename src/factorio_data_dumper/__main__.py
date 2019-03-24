

import json
from .lua import Lua
from .factorio import DataFilesystem, BaseMod, CoreMod, ModEvaluator, ModsContext, Factorio


fact = Factorio()

lua = Lua(fact.setup_lua)

data = DataFilesystem()
mods = ModsContext()


mods = (
    CoreMod(data),
    BaseMod(data)
)

for mod in mods:
    lua.evaluate(ModEvaluator(mods, mod))


if __name__ == '__main__':
    print(json.dumps(lua.dump_global('data'), separators=(',', ':')))
