"""nox-poetry configuration file."""

from calcipy.dev.noxfile import build_check, build_dist, coverage, pin_dev_dependencies, tests  # noqa: F401

# Ensure that non-calcipy dev-dependencies are available in Nox environments
pin_dev_dependencies([
    'freezegun>=1.2.2',
    'hypothesis>=6.56.4',
])
