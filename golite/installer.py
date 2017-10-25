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
        sublime.set_timeout_async(self.install_sublime_linter, 0)
        sublime.set_timeout_async(self.install_go_tools, 0)

    def install_sublime_linter(self):
        from package_control.package_manager import PackageManager
        manager = PackageManager()
        manager.install_package("SublimeLinter")

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
            utils.prompt(
                "Golite\n\n"
                "Failed to install go tools, please view the console for more "
                "details.")
            raise e
        print("[golite] go tools installed")

    def run_cmd(self, args, timeout=60):
        print("[golite] running '%s'" % ' '.join(args))
        subprocess.check_call(args, timeout=timeout, env=utils.get_env())


class GoliteDoctorCommand(sublime_plugin.ApplicationCommand):
    """GoliteDoctorCommand

    Audit installation for common issues

    Extends:
        sublime_plugin.ApplicationCommand
    """

    def run(self):
        self.doctor()

    def doctor(self):
        msg_tmpl = ("[%s] Golang installed\n"
                    "[%s] Go tools installed\n"
                    "[%s] Sublimelinter installed")

        # check golang
        go_installed = True
        try:
            utils.which("go")
        except EnvironmentError:
            go_installed = False

        # check go tools
        go_tools_installed = True
        for tool in go_tools.keys():
            try:
                utils.which(tool)
            except EnvironmentError:
                go_tools_installed = False
                break

        # check sublimelinter
        sublime_linter_installed = True
        try:
            import SublimeLinter.lint
        except ImportError:
            sublime_linter_installed = False

        msg = msg_tmpl % tuple([
            "√" if b else "×"
            for b in
            [go_installed, go_tools_installed, sublime_linter_installed]
        ])
        utils.prompt(msg)
