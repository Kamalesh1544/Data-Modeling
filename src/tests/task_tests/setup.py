from injector import Injector

from src.app.routers.auth.repositories import UserRepo
from src.tests.fake_data.fake_user_repo import FakeUserRepo


def register_fake_repos(injector: Injector):
    injector.binder.bind(UserRepo, FakeUserRepo())
