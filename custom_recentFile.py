import os
import json
import sublime
import sublime_plugin


class PromptRecentFileCommand(sublime_plugin.WindowCommand):
    def run(self, index):
        self.home = os.path.expandvars('$HOME')
        opened_files = [v.file_name() for v in self.window.views()]

        # reload session file
        # how to reload it???
        st_path = os.path.dirname(sublime.packages_path())
        session_path = os.path.join(st_path, "Local", "Auto save Session.sublime_session")
        if not os.path.exists(session_path):
            session_path = os.path.join(st_path, "Local", "Session.sublime_session")

        # get recent closed files list
        self.closed_files = [[
            'Clear recent files',
            'Highlight this option to close preview file'
        ]]

        for file in json.load(open(session_path))['windows'][0]['file_history'][:15]:
            if file not in opened_files:
                name = os.path.basename(file)
                path = file.replace(self.home, '~')
                self.closed_files.append([name, path])

        self.window.show_quick_panel(
            self.closed_files,
            self.on_done,
            0,
            index,
            self.preview_on_select
        )

    def on_done(self, index):
        this_view = self.window.active_view()

        if index == -1:
            return

        elif index == 0:
            if this_view not in self.window.views():
                self.close_preview()

            return self.window.run_command("clear_recent_files")

        elif this_view:
            self.window.open_file(self.closed_files[index][1])
            # print('Openning file', self.closed_files[index][1])

    def preview_on_select(self, index):
        if index == -1:
            # keeps the preview file open even with the prompt closed
            return

        elif index == 0:
            self.close_preview()

        elif self.window.active_view():
            self.window.open_file(self.closed_files[index][1], sublime.TRANSIENT)

    def close_preview(self):
        this_view = self.window.active_view()

        if this_view not in self.window.views():
            # print('Closing preview file', this_view.file_name().replace(self.home, '~'))
            self.window.run_command("close_file")
