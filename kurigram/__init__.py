"""Compatibility shim for projects importing `kurigram`.

This repository primarily relies on the `kurigram` import path. Some runtime
images may only have `pyrogram` installed, so we expose `kurigram` as a thin
alias to `pyrogram`.
"""

from importlib import import_module
import sys

_pyrogram = import_module("pyrogram")

# Re-export top-level Pyrogram symbols (Client, enums, filters, errors, ...).
for _name in dir(_pyrogram):
    if not _name.startswith("__"):
        globals()[_name] = getattr(_pyrogram, _name)

# Register commonly imported submodules under the `kurigram.*` namespace.
_SUBMODULES = (
    "enums",
    "errors",
    "file_id",
    "filters",
    "handlers",
    "raw",
    "session",
    "session.internals",
    "types",
    "utils",
)

for _submodule in _SUBMODULES:
    try:
        sys.modules[f"{__name__}.{_submodule}"] = import_module(f"pyrogram.{_submodule}")
    except ModuleNotFoundError:
        # Keep startup resilient if an optional internal module isn't available.
        continue

__all__ = [name for name in globals() if not name.startswith("_")]
