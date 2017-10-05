import os
import subprocess

import golangconfig


def get_startupinfo():
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return startupinfo


def executable_path(executable_name, view=None, window=None):
    exec_path, _ = golangconfig.executable_path(
        executable_name, view=view, window=window)
    if not exec_path:
        raise EnvironmentError("command '%s' not found" % exec_path)
    return exec_path
