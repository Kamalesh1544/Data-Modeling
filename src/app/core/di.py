"""Centralized InjectQ container configuration."""

from __future__ import annotations

from injectq import InjectQ
from injectq.modules import SimpleModule


container = InjectQ.get_instance()

_modules_installed = False


def ensure_app_modules() -> None:
    """Install application service bindings once per process."""

    global _modules_installed  # noqa: PLW0603
    if _modules_installed:
        return

    module = SimpleModule()
    container.install_module(module)
    _modules_installed = True


__all__ = ["container", "ensure_app_modules"]
