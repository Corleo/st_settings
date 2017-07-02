import sublime, sublime_plugin


class PromptIndentTabSizeCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Tab size:", "", self.on_done, None, None)
        pass

    def on_done(self, text):
        try:
            size = int(text)
            if size < 1:
                raise ValueError

            if self.window.active_view():
                self.window.active_view().run_command("indent_tab_size", {"size": size})

        except ValueError:
            print("ValueError: tab indentation size must be an integer greater than 1.")


class IndentTabSizeCommand(sublime_plugin.TextCommand):
    def run(self, edit, size):
        self.view.substr(sublime.Region(0, self.view.size()))
        self.view.run_command("unexpand_tabs",  { "set_translate_tabs": False })
        self.view.run_command("set_setting",    { "setting": "tab_size", "value": size })
        self.view.run_command("expand_tabs",    { "set_translate_tabs": True })
