import secrets

from university_system.auth import permissions
from university_system.models import user_manager, user_info_manager

virtual_repository = []


class AuthorizedUser(user_manager.User):
    def __init__(self, user):
        if user is not None:
            super().__init__(login=user.login, password=user.password, role=user.role, type=user.type,
                             info_id=user.info_id)
            self.type = permissions.from_str(user_manager.Type, self.type)
            self.role = permissions.from_str(permissions.Role, self.role)
            self.permissions = self.role.get_permissions()
            self.token = secrets.token_urlsafe(16)
            self.doc_id = user.doc_id
            self.info = self.get_info()

    def has_permission(self, scope, permission):
        return self.permissions.has_permission(scope, permission)

    def __eq__(self, other):
        return self.token == other.token and self.login == other.login

    def get_info(self):
        return user_info_manager.get(self.info_id)


def add(user):
    return virtual_repository.append(user)


def get(token):
    for user in virtual_repository:
        if token == user.token:
            return user
    return None


def remove(obj):
    return virtual_repository.remove(obj)


def log_in(login):
    user = AuthorizedUser(user_manager.search('login', login, False))
    add(user)
    return user


def log_out(token):
    user = get(token)
    remove(get(token))
    return user
