import subprocess

import sublime
import sublime_plugin

from . import utils

go_tools = {
    "gocode": "github.com/nsf/gocode",
    "guru": "golang.org/x/tools/cmd/guru",
    "goimports": "golang.org/x/tools/cmd/goimports",
    "godef": "github.com/rogpeppe/godef",
    "gometalinter": "github.com/alecthomas/gometalinter",
}


class GoliteInstallCommand(sublime_plugin.ApplicationCommand):
    """GoliteInstallCommand

    Install dependencies

    Extends:
        sublime_plugin.ApplicationCommand
    """

    def run(self):
        sublime.set_timeout_async(self.install_go_tools, 0)

    def install_go_tools(self):
        settings = sublime.load_settings("Golite.sublime-settings")
        auto_update = settings.get("auto_update_go_tools", False)

        print("[golite] start installing go tools: [%s]" %
              ','.join(go_tools.keys()))
        try:
            for tool in go_tools:
                args = ["go", "get", go_tools[tool]]
                if auto_update:
                    args.insert(2, "-u")
                self.run_cmd(args, timeout=60)

                if tool == "gometalinter":
                    args = ["gometalinter", "--install"]
                    if auto_update:
                        args.append("--update")
                    self.run_cmd(args, timeout=300)
        except Exception as e:
            if sublime.ok_cancel_dialog(
                    "[Golite] Failed to install go tools\n%s" % e,
                    'Open Documentation'):
                sublime.run_command('open_url',
                                    {'url': 'https://github.com/wy-z/Golite'})
        print("[golite] go tools installed")

    def run_cmd(self, args, timeout=60):
        print("[golite] running '%s'" % ' '.join(args))
        subprocess.check_call(args, timeout=timeout)


class GoliteDoctorCommand(sublime_plugin.ApplicationCommand):
    """GoliteDoctorCommand

    Audits installation for common issues

    Extends:
        sublime_plugin.ApplicationCommand
    """

    def run(self):
        self.doctor()

    def doctor(self):
        msgs = []

        # check golang
        msg = "[%s] Golang installed"
        installed = True
        try:
            utils.executable_path("go", window=sublime.active_window())
        except EnvironmentError:
            installed = False
        msgs.append(msg % ("x" if installed else "  "))

        # check all go tools have been installed
        msg = "[%s] Go tools installed"
        installed = True
        for tool in go_tools.keys():
            try:
                utils.executable_path("go", window=sublime.active_window())
            except EnvironmentError:
                installed = False
                break
        msgs.append(msg % ("x" if installed else "  "))

        # check sublimelinter
        msg = "[%s] Sublimelinter installed"
        installed = True
        try:
            import SublimeLinter.lint
        except ImportError:
            installed = False
        msgs.append(msg % ("x" if installed else "  "))

        if sublime.ok_cancel_dialog("%s" % '\n'.join(msgs),
                                    'Open Documentation'):
            sublime.run_command('open_url',
                                {'url': 'https://github.com/wy-z/Golite'})
