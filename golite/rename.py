import os
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

        rename_path = utils.executable_path("gorename", view=self.view)
        args = [
            rename_path, "-offset", "{file}:#{offset}".format(
                file=filename, offset=offset), "-to", name, "-v"
        ]
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=os.environ.copy(),
            startupinfo=utils.get_startupinfo())
        out, err = proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(err.decode("utf-8"))

        panel = self.view.window().create_output_panel('golite_rename')
        panel.set_scratch(True)
        # TODO: gorename isn't emitting line numbers, so to get clickable
        # referenced we'd need to process each line to append ':N' to make the
        # sublime regex work properly (line number is a required capture group).
        panel.settings().set("result_file_regex", "^\t(.*\.go)$")
        panel.run_command("select_all")
        panel.run_command("right_delete")
        panel.run_command('append', {'characters': err})
        self.view.window().run_command("show_panel",
                                       {"panel": "output.golite_rename"})
