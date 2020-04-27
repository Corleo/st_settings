import os
import json
import sublime
import sublime_plugin


class PromptRecentProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.recent_workspaces = self.get_recent_workspaces()
        self.existing_workspaces = self.get_existing_workspaces()
        self.existing_workspaces.insert(0, "Browse To Open Project")

        self.window.show_quick_panel(
            items=[w.replace(os.getenv('HOME'), '~') for w in self.existing_workspaces],
            on_select=self.on_done,
        )

    def on_done(self, index):
        if index == -1:
            return
        elif index == 0:
            self.window.run_command('prompt_open_project_or_workspace')
        else:
            self.window.run_command(
                'open_recent_project_or_workspace',
                {'index': self.recent_workspaces.index(self.existing_workspaces[index])}
            )

    def get_existing_workspaces(self):
        return [w for w in self.recent_workspaces if os.path.isfile(w)]

    def get_recent_workspaces(self):
        try:
            return self.load_session() \
                .get('workspaces') \
                .get('recent_workspaces') or []
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
