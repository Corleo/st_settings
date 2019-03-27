import sublime
import Default.comment as c


def region_is_empty(view, region):
    for line in view.lines(region):
        if not line.empty():
            return False

    return True


class SwapCommentCommand(c.ToggleCommentCommand):
    def run(self, edit):
        for region_sel in self.view.sel():
            comment_data = c.build_comment_data(self.view, region_sel.begin())
            empty_region = region_is_empty(self.view, region_sel)

            for line in sorted(self.view.lines(region_sel), reverse=True):
                # don't comment blank lines in block selection
                if not empty_region and line.empty():
                    continue

                line = sublime.Region(
                    c.advance_to_first_non_white_space_on_line(self.view, line.begin()), line.end())

                if self.view.match_selector(line.begin(), "comment.line"):
                    self.remove_line_comment(self.view, edit, comment_data, line)

                elif not self.view.match_selector(line.begin(), "comment.block"):
                    self.add_comment(self.view, edit, comment_data, False, line)

                # only blank lines selected
                elif empty_region:
                    self.remove_block_comment(self.view, edit, comment_data, line)

                # selection region has line with the beginning of comment block
                elif self.view.match_selector(line.begin(), "punctuation.definition.comment"):
                    self.remove_block_comment(self.view, edit, comment_data, line)

            # if not region_sel.empty():
            #     for region_block in sorted(self.view.find_by_selector("comment.block"), reverse=True):
            #         region = region_sel.intersection(region_block)

            #         if region:
            #             self.remove_block_comment(self.view, edit, comment_data, region)
