import os

from find_executable import find_executable
from posix_or_nt import posix_or_nt

if posix_or_nt() == 'nt':
    from split_command_line import split_command_line_nt as iterate_command_line_arguments

    EDITOR_FALLBACKS = ('notepad',)

else:
    from split_command_line import split_command_line_posix as iterate_command_line_arguments

    EDITOR_FALLBACKS = ('nano', 'vi',)


def find_executable_first_match_or_none(executable_name):
    it = find_executable(executable_name)
    return next(it, None)


def check_split_and_canonicalize_editor_command(editor_command_or_none):
    if editor_command_or_none is None:
        return None

    command_line_arguments = list(iterate_command_line_arguments(editor_command_or_none))
    if not command_line_arguments:
        return None

    editor_name = command_line_arguments[0]
    remaining_arguments = command_line_arguments[1:]

    editor_executable_first_match_or_none = find_executable_first_match_or_none(editor_name)
    if editor_executable_first_match_or_none is None:
        return None

    return [editor_executable_first_match_or_none] + remaining_arguments


def get_args_to_launch_editor(editor=None):
    """Returns a list of arguments (absolute executable path and any arguments) to launch the user's preferred text editor.

    Args:
        editor (str or None): Optionally specify the editor command to use (overrides env vars and fallbacks).

    Returns:
        list[str]: A list of arguments (absolute executable path and any arguments) to launch the user's preferred text editor.

    Raises:
        EnvironmentError: if no editor could be found."""
    # Check if the user-provided `editor` is set and valid.
    editor_command_arguments_or_none = check_split_and_canonicalize_editor_command(editor)
    if editor_command_arguments_or_none is not None:
        return editor_command_arguments_or_none

    # Check if the `VISUAL` environment variable is set and valid.
    env_visual_command_arguments_or_none = check_split_and_canonicalize_editor_command(os.environ.get('VISUAL'))
    if env_visual_command_arguments_or_none is not None:
        return env_visual_command_arguments_or_none

    # If not, check if the `EDITOR` environment variable is set and valid.
    env_editor_command_arguments_or_none = check_split_and_canonicalize_editor_command(os.environ.get('EDITOR'))
    if env_editor_command_arguments_or_none is not None:
        return env_editor_command_arguments_or_none

    # If not, check if the fallbacks are set and valid.
    for editor_fallback in EDITOR_FALLBACKS:
        editor_fallback_command_arguments_or_none = check_split_and_canonicalize_editor_command(editor_fallback)
        if editor_fallback_command_arguments_or_none is not None:
            return editor_fallback_command_arguments_or_none

    raise EnvironmentError(
        'Cannot get the command to launch the default editor. '
        'Please pass a valid command to launch an editor to the `editor` parameter, '
        'or set the VISUAL or EDITOR environment variables.'
    )
