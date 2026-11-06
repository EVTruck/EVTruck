"""Truck EV conversion bits and parts."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as import_version

try:
    version = import_version("EVTruck")
except PackageNotFoundError:  # pragma: no cover
    version = "0.0.0"
