from tortoise import Model


class Router:
    def db_for_read(self, model: type[Model]):
        return "master"

    def db_for_write(self, model: type[Model]):
        return "master"
