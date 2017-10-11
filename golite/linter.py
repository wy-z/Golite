from SublimeLinter.lint import Linter

from . import utils


class Gometalinter(Linter):
    """Provides an interface to gometalinter."""

    defaults = {
        'args': ['--fast'],
    }
    syntax = ('go')
    cmd = ['gometalinter', '*', '@']
    regex = r'(?:[^:]+):(?P<line>\d+):(?P<col>\d+)?:(?:(?P<warning>warning)|(?P<error>error)):\s*(?P<message>.*)'

    def __init__(self, view, syntax):
        Linter.__init__(self, view, syntax)

        if not self.env:
            self.env = {}
        self.env.update(utils.get_env())
