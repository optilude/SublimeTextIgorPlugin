import subprocess

import sublime
import sublime_plugin

COMMAND = "/usr/local/bin/igor"

class IgorReaperCommand(sublime_plugin.EventListener):
    """On save of Python files, reap for mr.igor
    """

    def on_post_save(self, view):
        if not 'python' in view.settings().get('syntax').lower():
            return

        filename = view.file_name()
        igor_cmd = '%s --reap "%s"' % (COMMAND, filename,)
        out = subprocess.Popen(igor_cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).communicate()
        if out[1]:
            sublime.error_message(out[1].decode('utf-8'))
        else:
            sublime.status_message("Reaped")

class IgorReplaceCommand(sublime_plugin.TextCommand):
    """Replace the contents of the current buffer with the outputs
    of mr.igor
    """

    def run(self, edit):
        if not 'python' in self.view.settings().get('syntax').lower():
            return

        filename = self.view.file_name()
        igor_cmd = '%s --print "%s"' % (COMMAND, filename,)

        self.view.run_command('save')

        out = subprocess.Popen(igor_cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).communicate()
        
        if out[1]:
            sublime.error_message(out[1].decode('utf-8'))
        else:
            if out[0]:
                out = ''.join(out[0])
                out = out.replace('%s:' % filename, '')
                replacement = out.strip()

                region = sublime.Region(0, self.view.size())
                self.view.replace(edit, region, replacement)
                sublime.status_message("Updated")