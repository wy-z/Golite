import sublime

from .golite.formatter import GoliteFormatCommand, GoliteFormatListener
from .golite.gocode import GocodeListener
from .golite.godef import GoliteGodefCommand
from .golite.installer import GoliteDoctorCommand, GoliteInstallCommand
from .golite.linter import Gometalinter
from .golite.rename import GoliteRenameCommand


def plugin_loaded():
    settings = sublime.load_settings("Golite.sublime-settings")
    if settings.get("auto_update_go_tools", False):
        sublime.run_command("golite_install")
    check_prompt()


def check_prompt():
    settings = sublime.load_settings("Golite.sublime-settings")
    if settings.get("prompted", False):
        return

    # try to install go tools
    sublime.run_command("golite_install")

    # set 'auto_update_go_tools'
    return_code = sublime.yes_no_cancel_dialog(
        "[Golite] Do you want to update go tools automatically?")
    if return_code == sublime.DIALOG_YES:
        settings.set("auto_update_go_tools", True)
    elif return_code == sublime.DIALOG_NO:
        settings.set("auto_update_go_tools", False)

    settings.set("prompted", True)
    sublime.save_settings("Golite.sublime-settings")
