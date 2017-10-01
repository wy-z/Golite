# fork from github.com/nsf/gocode
# Copyright (C) 2010 nsf <no.smile.face@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import subprocess

import golangconfig
import sublime
import sublime_plugin

from . import utils


# go to balanced pair, e.g.:
# ((abc(def)))
# ^
# \--------->^
#
# returns -1 on failure
def skip_to_balanced_pair(str, i, open, close):
    count = 1
    i += 1
    while i < len(str):
        if str[i] == open:
            count += 1
        elif str[i] == close:
            count -= 1

        if count == 0:
            break
        i += 1
    if i >= len(str):
        return -1
    return i


# split balanced parens string using comma as separator
# e.g.: "ab, (1, 2), cd" -> ["ab", "(1, 2)", "cd"]
# filters out empty strings
def split_balanced(s):
    out = []
    i = 0
    beg = 0
    while i < len(s):
        if s[i] == ',':
            out.append(s[beg:i].strip())
            beg = i + 1
            i += 1
        elif s[i] == '(':
            i = skip_to_balanced_pair(s, i, "(", ")")
            if i == -1:
                i = len(s)
        else:
            i += 1

    out.append(s[beg:i].strip())
    return list(filter(bool, out))


def extract_arguments_and_returns(sig):
    sig = sig.strip()
    if not sig.startswith("func"):
        return [], []

    # find first pair of parens, these are arguments
    beg = sig.find("(")
    if beg == -1:
        return [], []
    end = skip_to_balanced_pair(sig, beg, "(", ")")
    if end == -1:
        return [], []
    args = split_balanced(sig[beg + 1:end])

    # find the rest of the string, these are returns
    sig = sig[end + 1:].strip()
    sig = sig[1:-1] if sig.startswith("(") and sig.endswith(")") else sig
    returns = split_balanced(sig)

    return args, returns


# takes gocode's candidate and returns sublime's hint and subj
def hint_and_subj(cls, name, type):
    subj = name
    if cls == "func":
        hint = cls + " " + name
        args, returns = extract_arguments_and_returns(type)
        if returns:
            hint += "\t" + ", ".join(returns)
        if args:
            sargs = []
            for i, a in enumerate(args):
                ea = a.replace("{", "\\{").replace("}", "\\}")
                sargs.append("${{{0}:{1}}}".format(i + 1, ea))
            subj += "(" + ", ".join(sargs) + ")"
        else:
            subj += "()"
    else:
        hint = cls + " " + name + "\t" + type
    return hint, subj


class GocodeListener(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        loc = locations[0]
        if not view.match_selector(loc, "source.go"):
            return
        settings = sublime.load_settings("Golite.sublime-settings")
        if not settings.get("gocode_enabled", True):
            return
        gocode_path, _ = golangconfig.subprocess_info(
            "gocode", ['GOPATH'], view=view)

        src = view.substr(sublime.Region(0, view.size()))
        filename = view.file_name()
        cloc = "c{0}".format(loc)
        proc = subprocess.Popen(
            [gocode_path, "-f=csv", "autocomplete", filename, cloc],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            env=os.environ.copy(),
            startupinfo=utils.get_startupinfo())
        out = proc.communicate(src.encode())[0].decode()

        result = []
        for line in filter(bool, out.split("\n")):
            arg = line.split(",,")
            hint, subj = hint_and_subj(*arg)
            result.append([hint, subj])

        completion_flag = 0
        if settings.get("gocode_inhibit_word_completions", True):
            completion_flag |= sublime.INHIBIT_WORD_COMPLETIONS
        if settings.get("gocode_inhibit_explicit_completions", False):
            completion_flag |= sublime.INHIBIT_EXPLICIT_COMPLETIONS
        return (result, completion_flag)
