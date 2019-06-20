from university_system.server import bd_config
from university_system.server import tiny_repository

__repository_cache = {}


def __get_path(title=None):
    if title is None:
        return bd_config.default_db_path

    path = bd_config.db_paths.get(title, None)
    if path is None:
        path = bd_config.default_db_path
    return path


def get_repository(title):
    repository = __repository_cache.get(title, None)
    if repository is None:
        repository = tiny_repository.TinyRepository(__get_path(title), title)
        __repository_cache[title] = repository
    return repository