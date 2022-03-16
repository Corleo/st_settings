import os
import re
import sublime
import sublime_plugin


class OpenFileInPathCommand(sublime_plugin.WindowCommand):
    """Opens file in path present at the current cursor position.
    """

    FILE_PATTERN = re.compile(r"""
            ^([^:]*)     # file path
            (?:\:(\d+))? # line number if given
            (?:\:(\d+))? # column number if given
        """, re.VERBOSE)

    FTP_PATTERN = re.compile(r"""
            ^(s?ftp:)  # protocol
            (?:/+)     # ignore
            ([^:]*)    # file path
            (?:\:\d+)? # ignore line number if given
            (?:\:\d+)? # ignore column number if given
        """, re.VERBOSE)

    def run(self):
        view = self.window.active_view()
        view.run_command("split_selection_into_lines")
        view.run_command("expand_selection_to_whitespace")

        for region in view.sel():
            selected = view.substr(region)
            self.open_file(selected)

    def open_file(self, file):
        file = str(file).replace('~', os.getenv('HOME'))
        filepath, row, col = self.FILE_PATTERN.match(file).groups()

        if os.path.isfile(filepath):
            row = 0 if row is None else row
            col = 0 if col is None else col
            file = f'{filepath}:{row}:{col}'

            self.window.open_file(file, sublime.ENCODED_POSITION)

        elif file.startswith(('ftp:/', 'sftp:/')):
            ftp_protocol, filepath = self.FTP_PATTERN.match(file).groups()

            uid = os.getuid()
            file = f'/run/user/{uid}/gvfs/{ftp_protocol}host={filepath}'

            if os.path.isfile(file):
                self.window.open_file(file)
            else:
                self.print_error_msg(file)

        else:
            self.print_error_msg(file)

    def print_error_msg(self, file):
        print(f'OpenFileInPath error: Invalid file path: {file}')
