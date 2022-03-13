import os
import sublime
import sublime_plugin


class EditCommandsCommand(sublime_plugin.WindowCommand):
    def run(self):
        st_path = sublime.packages_path()
        file = os.path.join(st_path, "User", "Default.sublime-commands")
        view = self.window.open_file(file)


class EditCommandsListener(sublime_plugin.ViewEventListener):
    def on_load_async(self):
        file_name = self.view.file_name()

        if isinstance(file_name, str) and file_name.endswith('Packages/User/Default.sublime-commands'):
            self.view.run_command("move_to", {"to": "eof"})
