"""Smoke test: the environment has the right Python and all core dependencies."""

import sys


def test_python_version():
    assert sys.version_info[:2] == (3, 12)


def test_core_dependencies_import():
    import matplotlib  # noqa: F401
    import numpy  # noqa: F401
    import pandas  # noqa: F401
    import pydantic  # noqa: F401
    import scipy  # noqa: F401
    import yaml  # noqa: F401


def test_project_packages_import():
    import analysis  # noqa: F401
    import common  # noqa: F401
    import runner  # noqa: F401
    import simulator  # noqa: F401
    import testbed  # noqa: F401
