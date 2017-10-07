import subprocess

import sublime
import sublime_plugin

from . import utils


class GoliteRenameCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return self.view.match_selector(0, "source.go")

    def run(self, edit):
        self.view.window().show_input_panel("New name:", "", self.rename_async,
                                            None, None)

    def rename_async(self, name):
        sublime.set_timeout_async(lambda: self.rename(name), 0)

    def rename(self, name):
        """rename

        The gorename command performs precise type-safe renaming of identifiers
        in Go source code.
        """
        view = self.view
        filename = view.file_name()

        select = view.sel()[0]
        select_before = sublime.Region(0, select.begin())
        string_before = view.substr(select_before)
        offset = len(string_before.encode("utf-8"))

        args = [
            "gorename", "-offset", "{file}:#{offset}".format(
                file=filename, offset=offset), "-to", name
        ]
        utils.show_golite_panel(self.view.window(), "renaming ...")

        proc = subprocess.Popen(
            args + ["-d"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=utils.get_env(),
            startupinfo=utils.get_startupinfo())
        out, _ = proc.communicate()
        buf_out = out

        proc = subprocess.Popen(
            args + ["-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=utils.get_env(),
            startupinfo=utils.get_startupinfo())
        out, _ = proc.communicate()
        if proc.returncode != 0:
            print("[golite] failed to rename '%s':\n%s" %
                  (name, out.decode("utf-8")))
            buf_out = out

        utils.close_golite_panel(self.view.window())
        buf_name = "Rename Result"
        buf = self.view.window().new_file()
        buf.set_name(buf_name)
        buf.set_scratch(True)
        buf.set_syntax_file("Packages/Diff/Diff.sublime-syntax")
        buf.settings().set("result_file_regex", "^\t(.*\.go)$")
        buf.run_command("select_all")
        buf.run_command("right_delete")
        buf.run_command('append', {'characters': buf_out.decode("utf-8")})
        buf.set_read_only(True)
