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


def add_autostart(self, name, content, comment, toexec):
    lists = list(fn.listdir(fn.home + "/.config/autostart"))
    if not name + ".desktop" in lists:
        content = (
            "[Desktop Entry]\n\
                Encoding=UTF-8\n\
                    Version=1.0\n\
                        Type=Application\n\
                            Name="
                            + name
                            + "\n\
                                Comment="
                                + comment
                                + "\n\
                                    Exec="
                                    + toexec
                                    + "\n\
                                        TryExec="
                                        + toexec
                                        + "\n\
                                            StartupNotify=false\n\
                                                X-Gnome-Autostart-enabled=true\n\
                                                    Terminal=false\n\
                                                        Hidden=false\n"
        )
        with open(fn.home + "/.config/autostart/" + name + ".desktop", "w", encoding="utf-8") as f:
            f.write(content)
            f.close()
        self.add_row(name)
        