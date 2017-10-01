import json
import os
import subprocess

import golangconfig
import sublime
import sublime_plugin

from . import utils


class GoliteGodefCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return self.view.match_selector(0, "source.go")

    def run(self, edit):
        self.godef()

    def godef(self):
        """godef

        both-mode: use godef to find definition first,
        if not found, use guru to find again.
        """
        settings = sublime.load_settings("Golite.sublime-settings")
        view = self.view
        filename = view.file_name()

        select = view.sel()[0]
        select_before = sublime.Region(0, select.begin())
        string_before = view.substr(select_before)
        offset = len(string_before.encode("utf-8"))

        position = ""
        mode = settings.get("godef_mode", "both")
        if mode in ["godef", "both"]:
            try:
                godef_path, _ = golangconfig.subprocess_info(
                    "godef", [], view=self.view)
                args = [godef_path, "-f", filename, "-o", str(offset)]

                proc = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=os.environ.copy(),
                    startupinfo=utils.get_startupinfo())
                out, err = proc.communicate()
                if proc.returncode != 0:
                    raise RuntimeError(err.decode("utf-8"))
                else:
                    position = out.decode("utf-8").strip()
            except Exception as e:
                print("[golite] failed to go to definition with 'godef':\n%s" %
                      e)
        if position == "" and mode in ["guru", "both"]:
            guru_path, _ = golangconfig.subprocess_info(
                "guru", [], view=self.view)
            args = [
                guru_path, "-json", 'definition', filename + ":#" + str(offset)
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
            else:
                position = json.loads(out.decode("utf-8").strip()).get(
                    "objpos", "")

        if position == "":
            raise RuntimeError(
                "[golite] failed to go to definition: invalid selection")

        self.view.window().open_file(position, sublime.ENCODED_POSITION)
