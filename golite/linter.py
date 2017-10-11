import os

from SublimeLinter.lint import Linter, util
from SublimeLinter.lint.persist import settings

from . import utils


class Gometalinter(Linter):
    """Provides an interface to gometalinter."""

    defaults = {
        'args': ['--fast', '--aggregate'],
    }

    syntax = ('go')
    cmd = ['gometalinter', '*', '.']
    regex = r'(?:[^:]+):(?P<line>\d+):(?P<col>\d+)?:(?:(?P<warning>warning)|(?P<error>error)):\s*(?P<message>.*)'

    def __init__(self, view, syntax):
        Linter.__init__(self, view, syntax)

        self.linting = False
        self.pre_code = ""

        if not self.env:
            self.env = {}
        self.env.update(utils.get_env())

    def run(self, cmd, code):
        if self.linting and self.pre_code == code:
            return
        self.linting = True
        self.pre_code = code

        result = ''
        try:
            if settings.get('lint_mode') == 'background':
                result = self._live_lint(cmd, code)
            else:
                result = self._on_save_lint(cmd)
        finally:
            self.linting = False
        return result

    def _live_lint(self, cmd, code):
        files = [
            f for f in os.listdir(os.path.dirname(self.filename))
            if f.endswith('.go')
        ]
        return self.tmpdir(cmd, files, code)

    def _on_save_lint(self, cmd):
        filename = os.path.basename(self.filename)
        cmd = cmd + ['-I', filename]
        out = util.communicate(cmd, output_stream=util.STREAM_STDOUT)
        return out or ''
