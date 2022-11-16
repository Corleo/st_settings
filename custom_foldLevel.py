import sublime, sublime_plugin


class PromptFoldLevelCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Fold level #:", "", self.on_done, None, None)
        pass

    def on_done(self, text):
        try:
            level = int(text)
            if level < 0:
                raise ValueError

            if self.window.active_view():
                self.window.active_view().run_command("fold_level", {"level": level})

        except ValueError:
            print("ValueError: level must be a positive integer.")


class FoldLevelCommand(sublime_plugin.TextCommand):
    def run(self, edit, level):
        self.view.substr(sublime.Region(0, self.view.size()))
        self.view.run_command("unfold_all")

        if level > 0:
            self.view.run_command("fold_by_level", {"level": level})
