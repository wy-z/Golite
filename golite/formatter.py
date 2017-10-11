import os
import subprocess
import tempfile

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

            mode = settings.get("format_mode", "both")
            formatted = False
            if mode in ["goimports", "both"]:
                try:
                    self.fromat("goimports", code, edit)
                    formatted = True
                except Exception as e:
                    print(
                        "[golite] failed to format '%s' with 'goimports':\n%s"
                        % (self.view.file_name(), e))
            if not formatted and mode in ["gofmt", "both"]:
                args = []
                if settings.get("gofmt_simplified", False):
                    args = ["-s"]
                self.fromat("gofmt", code, edit, args)
        except Exception:
            self.view.set_read_only(False)
            raise
        finally:
            self.view.set_read_only(False)

    def fromat(self, formatter, code, edit, args=None):
        """fromat

        Run formatter and modify the buffer if needed

        Arguments:
            formatter {string}       -- "gofmt" or "goimports"
            code      {string}       -- origin code
            edit      {sublime.Edit} -- sublime edit instance

        Keyword Arguments:
            args {list} -- [description] (default: {None})

        Returns:
            string -- formatted code

        Raises:
            RuntimeError -- raise runtimeError when processing failed
        """
        if args is None:
            args = []

        with tempfile.NamedTemporaryFile(
                dir=os.path.dirname(self.view.file_name())) as tmp:
            tmp.write(code.encode("utf-8"))
            tmp.flush()
            file = tmp.name

            args.insert(0, formatter)
            args.append(file)
            proc = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=utils.get_env(),
                startupinfo=utils.get_startupinfo())
            out, err = proc.communicate()
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
