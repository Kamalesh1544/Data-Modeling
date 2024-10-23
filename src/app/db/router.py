from tortoise import Model


class Router:
    """
    A database router to control which database to use for read and write operations.

    Methods:
        db_for_read(model: type[Model]) -> str:
            Determines the database to use for read operations.

        db_for_write(model: type[Model]) -> str:
            Determines the database to use for write operations.
    """

    def db_for_read(self, model: type[Model]):
        return "master"

    def db_for_write(self, model: type[Model]):
        return "master"
