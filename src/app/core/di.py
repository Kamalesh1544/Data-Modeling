"""Centralized InjectQ container configuration."""

from __future__ import annotations

from injectq import InjectQ
from injectq.modules import SimpleModule

# from src.app.routers.auth.repositories import UserRepo
# from src.app.routers.auth.services import UserService

"""
It will be used for the module level injection like we have 5 router then need for injection group by
we can do that...
"""
container = InjectQ.get_instance()

_modules_installed = False


def ensure_app_modules() -> None:
    """Install application service bindings once per process."""

    global _modules_installed
    if _modules_installed:
        return

    module = SimpleModule()
    # module.bind(UserRepo, UserRepo)
    # module.bind(UserService, UserService)

    container.install_module(module)
    _modules_installed = True


__all__ = ["container", "ensure_app_modules"]