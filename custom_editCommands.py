import os
import sublime
import sublime_plugin


class EditCommandsCommand(sublime_plugin.WindowCommand):
    def run(self):
        st_path = sublime.packages_path()
        file = os.path.join(st_path, "User", "Default.sublime-commands")
        view = self.window.open_file(file)

        if not view.is_loading():
            view.run_command("move_to", {"to": "eof"})


class EditCommandsListener(sublime_plugin.ViewEventListener):
    def on_load(self):
        sublime.set_timeout(
            lambda: self.view.run_command("move_to", {"to": "eof"}),
            20,
        )
