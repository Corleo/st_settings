import sublime
import sublime_plugin


class DevCommentCommand(sublime_plugin.TextCommand):
    """Swap comments and lines between current line and upper line.
    """
    def run(self, edit):
        regions = self.view.sel()
        sel = self.view.lines(regions[0])

        if regions.__len__() == 1 and len(sel) == 1:
            bottom_line = sel[0]
            line, _ = self.view.rowcol(bottom_line.a)
            pt = self.view.text_point(line - 1, 0)
            top_line = self.view.line(pt)

            if top_line.empty():
                self.view.run_command("swap_comment")
            else:
                two_lines = sublime.Region(top_line.a, bottom_line.b)
                regions.clear()
                regions.add(two_lines)
                self.view.run_command("swap_comment")

                regions.clear()
                regions.add(two_lines.b)
                self.view.run_command("swap_line_up")

                regions.clear()
                regions.add(two_lines.b)
