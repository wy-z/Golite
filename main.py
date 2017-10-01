import sublime
import golangconfig

from .golite.formatter import GoliteFormatCommand, GoliteFormatListener
from .golite.gocode import GocodeListener
from .golite.godef import GoliteGodefCommand
from .golite.installer import GoliteInstallCommand
from .golite.linter import Gometalinter


def plugin_loaded():
    golite_check()
    settings = sublime.load_settings("Golite.sublime-settings")
    if settings.get("auto_update_go_tools", False):
        sublime.run_command("golite_install")


def golite_check():
    settings = sublime.load_settings("Golite.sublime-settings")
    if settings.get("prompted", False):
        return

    # check go env
    try:
        golangconfig.subprocess_info(
            'go', ["GOPATH", "GOAP"], window=sublime.active_window())
    except Exception as e:
        prompt(e)

    # check sublimeLinter
    try:
        import SublimeLinter
    except ImportError as e:
        msg = "SublimeLinter is required for code linting"
        prompt(e)

    # try to install go
    sublime.run_command("golite_install")

    # set 'auto_update_go_tools'
    return_code = sublime.yes_no_cancel_dialog(
        "[Golite] Do you want to auto update go tools.")
    if return_code == sublime.DIALOG_YES:
        settings.set("auto_update_go_tools", True)
    else:
        settings.set("auto_update_go_tools", False)

    settings.set("prompted", True)
    sublime.save_settings("Golite.sublime-settings")


def prompt(err_msg):
    if sublime.ok_cancel_dialog("[Golite] %s." % err_msg,
                                'Open Documentation'):
        sublime.run_command('open_url',
                            {'url': 'https://github.com/wy-z/Golite'})
