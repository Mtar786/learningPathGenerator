"""Learning Path Generator package.

This package provides a CLI and helper modules to construct a multi‑week learning
plan for any skill or technology using resources from YouTube and Medium.  See
the :mod:`cli` module for command‑line usage.
"""

from .cli import main as run

__all__ = ["run"]