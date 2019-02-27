import re
import sublime
import sublime_plugin

# for debugging
# sublime.log_commands(True)

# pattern = re.compile(r".*test.*")         # match
# pattern = re.compile('(?!.*(?:test)).*')  # don't match


class CustomBuildSystemCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        params = self.window.extract_variables()
        # print(params)

        if params['file_extension'] == "py":
            if re.match(r".*test.*", params['file_name']):
                variant = "pytest"
            else:
                variant = "run"

            self.window.run_command("build", {
                "build_system": "Packages/User/py3k.sublime-build",
                "choice_build_system": "true",
                "choice_variant": "true",
                "variant": "{}".format(variant)
            }
            )

        else:
            # run regular build command
            self.window.run_command("build")


# params = {
#     "packages": "~/.config/sublime-text-3/Packages",
#     "file_name": "custom_buildSystem.py",
#     "file": "~/.config/sublime-text-3/Packages/User/custom_buildSystem.py",
#     "file_extension": "py",
#     "platform": "Linux",
#     "file_base_name": "custom_buildSystem",
#     "file_path": "~/.config/sublime-text-3/Packages/User"
# }
