import os

from SublimeLinter.lint import Linter, util

from . import utils


class Gometalinter(Linter):
    """Provides an interface to gometalinter."""

    defaults = {
        'args': ['--fast', '--aggregate'],
    }
    syntax = ('go')
    cmd = ['gometalinter', '*']
    regex = r'(?:[^:]+):(?P<line>\d+):(?P<col>\d+)?:(?:(?P<warning>warning)|(?P<error>error)):\s*(?P<message>.*)'

    def __init__(self, view, syntax):
        Linter.__init__(self, view, syntax)

        if not self.env:
            self.env = {}
        self.env.update(utils.get_env())

    def run(self, cmd, code):
        new_cmd = cmd + [
            os.path.dirname(self.filename), '-I',
            os.path.basename(self.filename)
        ]
        result = util.communicate(
            new_cmd, output_stream=util.STREAM_STDOUT, env=self.env)
        return result
