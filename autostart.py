# Author : Eshan Roy <eshan@snigdhaos.org>

from ast import literal_eval
import functions as fn

def get_startup(name):
    try:
        with open(fn.autostart + name + ".desktop", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
        state = True
    except:
        return False
    
    if fn.check_content("Hidden=", fn.autostart + name + ".desktop"):
        try:
            position = fn.get_position(lines, "Hidden=")
            state = lines[position].split("=")[1].strip()
            state = state.capitalize()
            state = not literal_eval(state)
            return state
        except Exception as e:
            print(e)
            return True
    else:
        return state
    
