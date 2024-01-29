##################################################################################
# Author: Eshan Roy <eshan@snigdhaos.org>
# URL : https://eshan.snigdhaos.org
# Lead Maintainer & Developer @ Snigdha OS
##################################################################################


from ast import literal_eval
import functions as fn

def get_startups(name):
    try:
        with open(fn.autostart + name + ".desktop", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
        state = True
    except:
        return True
    
    if fn.check_content("Hidden=", fn.autostart + name + ".desktop"):
        try:
            pos = fn.get_position(lines, "Hidden=")
            state = lines[pos].split("=")[1].strip()
            # cap
            state = state.capitalize()
            state = not literal_eval
            return state
        except Exception as e:
            print(e)
            return True
    else:
        return state


def add_autostart(self, name, com, cmnt):
    lists= list(fn.listdir(fn.home + "/.config/autostart"))
    if not name + ".desktop" in lists:
        content = ("[Desktop Entry]\n\
                   Encoding=UTF-8\n\
                   Version=1.0\n\
                   Name="
                   + name
                   + "\n\
                    Exec="
                    + com
                    + "\n\
                        TryExec="
                        + com
                        + "\n\
                            StartupNotify=false\n\
                                X-GNOME-Autostart-enabled=true\n\
                                    Terminal=false\n\
                                        Hidden=false\n")
        with open(fn.home + "/.config/autostart" + name + ".desktop", "w", encoding="utf-8") as f:
            f.write(content)
            f.close()
        self.add_row(name) #needed