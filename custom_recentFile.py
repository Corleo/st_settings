import os
import json
import sublime
import sublime_plugin
import itertools


class PromptRecentFileCommand(sublime_plugin.WindowCommand):
    def run(self, index):
        self.existing_closed_files = self.get_existing_closed_files()
        self.existing_closed_files.insert(0, [
            'Clear recent files',
            'Highlight this option to close the preview file'
        ])

        self.window.show_quick_panel(
            items=self.existing_closed_files,
            selected_index=index,
            on_select=self.open_file_on_selected,
            on_highlight=self.preview_on_highlighted
        )

    def get_existing_closed_files(self):
        opened_files = [v.file_name() for v in self.window.views()]

        return list(itertools.islice((
            [os.path.basename(f), f.replace(os.getenv('HOME'), '~')]
            for f in self.get_closed_files()
            if os.path.isfile(f) and f not in opened_files
        ), 15))

    def get_closed_files(self):
        try:
            return self.load_session() \
                .get('windows')[0] \
                .get('file_history') or []
        except Exception:
            return []

    def load_session(self):
        st_path = os.path.dirname(sublime.packages_path())
        session_file = os.path.join(st_path, "Local", "Auto Save Session.sublime_session")

        if not os.path.isfile(session_file):
            session_file = os.path.join(st_path, "Local", "Session.sublime_session")

            if not os.path.isfile(session_file):
                return None

        return json.load(open(session_file))

    def open_file_on_selected(self, index):
        if index == -1:
            return

        elif index == 0:
            self.window.run_command("clear_recent_files")

        elif self.window.active_view():
            self.window.open_file(self.existing_closed_files[index][1])

        else:
            return

    def preview_on_highlighted(self, index):
        if index == -1:
            # keeps preview file open even with the prompt closed
            return

        elif index == 0:
            self.close_preview()

        elif self.window.active_view():
            self.window.open_file(self.existing_closed_files[index][1], sublime.TRANSIENT)

        else:
            return

    def close_preview(self):
        if self.window.active_view() not in self.window.views_in_group(self.window.active_group()):
            self.window.run_command("close_file")
