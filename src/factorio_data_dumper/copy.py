

import os
import json


def copy(lua_data, data_fs, base_path="factorio"):
    os.makedirs(base_path, exist_ok=True)
    with open(os.path.join(base_path, 'factorio.json'), 'w') as f:
        json.dump(lua_data, f, separators=(',', ':'))
    copy_img(lua_data, data_fs, base_path)


def copy_img(lua_data, data_fs, base_path):
    for k, v in lua_data.items():
        if k in ('filename', 'icon') and isinstance(v, str) and v.startswith('__'):
            m, v = v.split('/', maxsplit=1)
            if m in ('__base__', '__core__'):
                sp = os.path.join(data_fs.path, m.replace('_', ''), v)
                tp = os.path.join(base_path, m, v)
                os.makedirs(os.path.dirname(tp), exist_ok=True)
                try:
                    with open(sp, 'rb') as s:
                        with open(tp, 'wb') as t:
                            t.write(s.read())
                except FileNotFoundError:
                    pass
        elif isinstance(v, dict):
            copy_img(v, data_fs, base_path)


if __name__ == '__main__':
    from .__main__ import lua, data
    copy(lua.dump_global('data'), data)
