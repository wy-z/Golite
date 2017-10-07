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
    "gorename": "golang.org/x/tools/cmd/gorename",
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
        update_tools = settings.get("install_cmd_update_go_tools", False)

        print("[golite] start installing go tools: [%s]" %
              ','.join(go_tools.keys()))
        try:
            for tool in go_tools:
                args = ["go", "get", go_tools[tool]]
                if update_tools:
                    args.insert(2, "-u")
                self.run_cmd(args, timeout=60)

                if tool == "gometalinter":
                    args = ["gometalinter", "--install"]
                    if update_tools:
                        args.append("--update")
                    self.run_cmd(args, timeout=300)
        except Exception as e:
            utils.prompt("[Golite] Failed to install go tools.\n%s" % e)
            raise e
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
            utils.which("go")
        except EnvironmentError:
            installed = False
        msgs.append(msg % ("x" if installed else "  "))

        # check all go tools have been installed
        msg = "[%s] Go tools installed"
        installed = True
        for tool in go_tools.keys():
            try:
                utils.which(tool)
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

        utils.prompt('\n'.join(msgs))
