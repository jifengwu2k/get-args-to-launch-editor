# `get-args-to-launch-editor`

A cross-platform Python utility to determine how to launch the user's preferred text editor, using user input, environment variables, and platform-specific fallbacks.

## Features

- Resolves a preferred text editor using (in order of precedence):
  1. User-supplied command (`editor` parameter)
  2. `$VISUAL` environment variable
  3. `$EDITOR` environment variable
  4. Platform-specific fallbacks:
     - NT: `notepad`
     - POSIX: `nano`, `vi`
- Verifies that the editor executable exists on the system.
- Canonicalizes the returned command as a list suitable for `os.execvp()` or `subprocess` calls.
- Command-line splitting and executable resolution is platform-aware.

## Installation

```commandline
pip install get-args-to-launch-editor
```

## Usage

```python
from get_args_to_launch_editor import get_args_to_launch_editor

# Example output on Linux:
# ['/usr/bin/nano']
print(get_args_to_launch_editor())

# Example output on Linux:
# ['/usr/bin/vim', '-R']
print(get_args_to_launch_editor('vim -R'))
```

## API

### `get_args_to_launch_editor(editor=None)`

Returns a list of arguments (absolute executable path and any arguments) to launch the user's preferred text editor.

- `editor` (str or None): Optionally specify the editor command to use (overrides env vars and fallbacks).
- Raises `EnvironmentError` if no editor could be found.

## Contributing

Contributions welcome! Please open issues or pull requests on GitHub.

## License

This project is licensed under the [MIT License](LICENSE).