import os
import re
import sublime
import sublime_plugin


class OpenFileInPathCommand(sublime_plugin.WindowCommand):
    """Opens file in path present at the current cursor position.
    """

    FILE_PATTERN = re.compile(r"""
            ^([^:]*)     # file path
            (?:\:(\d+))? # line if given
            (?:\:(\d+))? # column if given
        """, re.VERBOSE)

    def run(self):
        view = self.window.active_view()
        view.run_command("split_selection_into_lines")
        view.run_command("expand_selection_to_whitespace")

        for region in view.sel():
            selected = view.substr(region)
            self.open_file(selected)

    def open_file(self, file):
        file = file.replace('~', os.getenv('HOME'))
        filepath, row, col = self.FILE_PATTERN.match(file).groups()

        if os.path.isfile(filepath):
            row = 0 if row is None else row
            col = 0 if col is None else col
            file = f'{filepath}:{row}:{col}'

            self.window.open_file(file, sublime.ENCODED_POSITION)
        else:
            print(f'OpenFileInPath error: A string fornecida não é um caminho de arquivo válido: {file}')
