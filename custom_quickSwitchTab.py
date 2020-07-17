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
        files = [
            [os.path.basename(v.file_name()), os.path.dirname(v.file_name())]
            if v.file_name() is not None
            else [v.name() or 'untitled', None]
            for v in self.window.views_in_group(self.window.active_group())
        ]

        names = list(zip(*files))[0]

        return [
            "{:02d} - {}".format(index + 1, item[0]) if names.count(item[0]) == 1 or item[1] is None
            else "{:02d} - {} ➔ {}".format(index + 1, item[0], item[1].replace(os.getenv('HOME'), '~'))
            for index, item in enumerate(files)
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
