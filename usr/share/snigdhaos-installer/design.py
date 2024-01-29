import functions as fn

def install_themes(self):
    if self.adapta_gtk_theme.get_active():
        fn.install_snigdhaos_package(self, "adapta-gtk-theme")
    if self.arc_darkest_theme_git.get_active():
        fn.install_snigdhaos_package(self, "arc-darkest-theme-git")
    if self.arc_gtk_theme.get_active():
        fn.install_snigdhaos_package(self, "arc-darkest-theme-git")
    if self.ayu_theme.get_active():
        fn.install_snigdhaos_package(self, "arc-darkest-theme-git")
    if self.breeze.get_active():
        fn.install_snigdhaos_package(self, "arc-darkest-theme-git")
    if self.dracula_gtk_theme.get_active():
        fn.install_snigdhaos_package(self, "arc-darkest-theme-git")
    if self.fluent_gtk_theme.get_active():
        fn.install_snigdhaos_package(self, "arc-darkest-theme-git")
    if self.arc_gtk_theme.get_active():
        fn.install_snigdhaos_package(self, "arc-darkest-theme-git")
## ==> need update