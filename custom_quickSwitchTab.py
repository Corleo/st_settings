import os
import sublime_plugin


class QuickSwitchTabCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_quick_panel(
            items=self.get_the_names_of_views(),
            selected_index=self.get_active_view_index(),
            on_select=self.focus_view_on_select,
        )

    def get_the_names_of_views(self):
        return [
            os.path.basename(v.file_name()) for v in
            self.window.views_in_group(self.window.active_group())
        ]

    def get_active_view_index(self):
        return self.window.views_in_group(
            self.window.active_group()
        ).index(
            self.window.active_view()
        )

    def focus_view_on_select(self, index):
        if index >= 0:
            self.window.focus_view(
                self.window.views_in_group(
                    self.window.active_group()
                )[index]
            )
