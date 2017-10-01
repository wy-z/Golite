import os
import subprocess

import golangconfig
import sublime
import sublime_plugin

from . import utils


class GoliteFormatCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return self.view.match_selector(0, "source.go")

    def run(self, edit):
        settings = sublime.load_settings("Golite.sublime-settings")
        code = self.view.substr(sublime.Region(0, self.view.size()))
        try:
            self.view.set_read_only(True)

            formatter = settings.get("formatter", [])
            formatted = False
            if formatter in ["goimports", "both"]:
                try:
                    code = self.fromat("goimports", code, edit)
                    formatted = True
                except Exception as e:
                    print(
                        "[golite] failed to format '%s' with 'goimports':\n%s"
                        % (self.view.file_name(), e))
            if not formatted and formatter in ["gofmt", "both"]:
                args = []
                if settings.get("gofmt_simplified", False):
                    args = ["-s"]
                code = self.fromat("gofmt", code, edit, args)
        except Exception:
            self.view.set_read_only(False)
            raise
        finally:
            self.view.set_read_only(False)

    def fromat(self, formatter, code, edit, args=[]):
        """fromat

        Run formatter and modify the buffer if needed

        Arguments:
            formatter {string}       -- "gofmt" or "goimports"
            code      {string}       -- origin code
            edit      {sublime.Edit} -- sublime edit instance

        Keyword Arguments:
            args {list} -- [description] (default: {[]})

        Returns:
            string -- formatted code

        Raises:
            RuntimeError -- raise runtimeError when processing failed
        """
        formatter_path, _ = golangconfig.subprocess_info(
            formatter, ['GOPATH'], view=self.view)

        args.insert(0, formatter_path)
        proc = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=os.environ.copy(),
            startupinfo=utils.get_startupinfo(),
            shell=True)
        out, err = proc.communicate(input=code.encode("utf-8"))
        if proc.returncode != 0:
            raise RuntimeError(err.decode('utf-8'))

        out_str = ""
        if out is not None and out != b'':
            out_str = out.decode('utf-8')
            if code != out_str:
                region = sublime.Region(0, self.view.size())
                self.view.set_read_only(False)
                self.view.replace(edit, region, out_str)
        return out_str


class GoliteFormatListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if not view.match_selector(0, "source.go"):
            return

        settings = sublime.load_settings("Golite.sublime-settings")
        if not settings.get("format_on_save"):
            return
        view.run_command('golite_format')
