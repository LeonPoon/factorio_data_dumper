

import json
from .lua import Lua
from .factorio import DataFilesystem, BaseMod, CoreMod, ModEvaluator, ModsContext, Factorio


fact = Factorio()

lua = Lua(fact.setup_lua)

data = DataFilesystem()
mods = ModsContext()


for mod in (
    CoreMod(data),
    BaseMod(data)
):
    lua.evaluate(ModEvaluator(mods, mod))


print(json.dumps(lua.dump_global('data'), separators=(',', ':')))
