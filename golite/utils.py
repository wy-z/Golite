import os
import subprocess

import shellenv
import sublime


def get_env():
    _, env = shellenv.get_env()
    return env


def get_startupinfo():
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return startupinfo


def which(command):
    try:
        exec_path = subprocess.check_output(["which", command], env=get_env())
    except subprocess.CalledProcessError as e:
        raise EnvironmentError(e)
    return exec_path


def prompt(message):
    if sublime.ok_cancel_dialog(message, 'Open Documentation'):
        sublime.run_command('open_url',
                            {'url': 'https://github.com/wy-z/Golite'})
