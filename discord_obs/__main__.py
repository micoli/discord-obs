import os
import logging
import pprint
import colored_traceback
import gi

from discord_obs.configuration import OBSWS_BLANK_SCENE_NAME
from discord_obs.discord import set_discord_webcam
from discord_obs.obs import Obs

gi.require_version("Gtk", "3.0")
# pylint: disable=wrong-import-position,wrong-import-order
from gi.repository import Gtk


colored_traceback.add_hook(always=True)
pp = pprint.PrettyPrinter(indent=4)
logging.basicConfig(level=logging.INFO)
ICON_PATH = os.path.dirname(os.path.dirname(__file__))


class App:
    def __init__(self):
        self.obs = Obs()
        self.indicator = None
        self.tray = None
        self.menu = None
        self.make_menu()
        self.scene_menu_items = {}
        self.make_sys_tray_icon(self.menu)
        self.update_scenes_list()
        Gtk.main()

    def make_sys_tray_icon(self, menu):
        try:
            gi.require_version('AppIndicator3', '0.1')
            # pylint: disable=import-outside-toplevel
            from gi.repository import AppIndicator3
            self.indicator = AppIndicator3.Indicator.new(
                "antenna-off",
                ICON_PATH + "/antenna-off.svg",
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS
            )

            self.indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
            self.indicator.set_menu(menu)
        except (ImportError, ValueError) as exception:
            logging.info("Falling back to Systray : %s", exception)
            self.tray = Gtk.StatusIcon.new_from_icon_name(ICON_PATH + "/antenna-off.png")
            self.tray.connect('popup-menu', self.show_menu)
            self.tray.set_visible(False)
        finally:
            if self.indicator is not None:
                # pylint: disable=import-outside-toplevel
                from gi.repository import AppIndicator3
                self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            elif self.tray is not None:
                self.tray.set_visible(True)

    def show_menu(self, obj, button, time):
        self.menu.show_all()
        self.menu.popup(None, None, Gtk.StatusIcon.position_menu, obj, button, time)

    def make_menu(self):
        self.menu = Gtk.Menu()
        close_opt = Gtk.MenuItem.new_with_label("Close")
        self.menu.append(close_opt)
        close_opt.connect("activate", lambda _a: Gtk.main_quit())
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu.show_all()

    def update_scenes_list(self):
        for scene in self.obs.get_scenes_list():
            self.scene_menu_items[scene] = Gtk.MenuItem.new_with_label(scene)
            self.scene_menu_items[scene].connect("activate", lambda _a: self.set_scene(_a.get_label()))
            self.menu.append(self.scene_menu_items[scene])
        self.menu.show_all()

    def set_scene(self, scene):
        self.obs.change_scene(scene)
        if scene == OBSWS_BLANK_SCENE_NAME:
            set_discord_webcam(False)
            self.indicator.set_icon(ICON_PATH + "/antenna-off.svg")
            return
        set_discord_webcam(True)
        self.indicator.set_icon(ICON_PATH + "/antenna-on.svg")

def entrypoint() -> None:
    App()
