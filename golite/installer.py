import subprocess

import sublime
import sublime_plugin
import golangconfig


class GoliteInstallCommand(sublime_plugin.ApplicationCommand):
    """GoliteInstallCommand

    Install dependencies

    Extends:
        sublime_plugin.ApplicationCommand
    """
    go_tools = {
        "gocode": "github.com/nsf/gocode",
        "guru": "golang.org/x/tools/cmd/guru",
        "goimports": "golang.org/x/tools/cmd/goimports",
        "godef": "github.com/rogpeppe/godef",
        "gometalinter": "github.com/alecthomas/gometalinter",
    }

    def run(self):
        sublime.set_timeout_async(self.install_go_tools, 0)

    def install_go_tools(self):
        settings = sublime.load_settings("Golite.sublime-settings")
        auto_update = settings.get("auto_update_go_tools", False)

        print("[golite] start installing go tools: [%s]" %
              ','.join(self.go_tools.keys()))
        for tool in self.go_tools:
            args = ["go", "get", self.go_tools[tool]]
            if auto_update:
                args.insert(2, "-u")
            self.run_cmd(args, timeout=60)

            if tool == "gometalinter":
                args = ["gometalinter", "--install"]
                if auto_update:
                    args.append("--update")
                self.run_cmd(args, timeout=300)
        print("[golite] go tools installed")

    def run_cmd(self, args, timeout=60):
        print("[golite] running '%s'" % ' '.join(args))
        subprocess.check_call(args, timeout=timeout)
