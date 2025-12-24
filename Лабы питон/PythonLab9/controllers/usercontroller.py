from controllers.databasecontroller import UserCRUD, UserCurrencyCRUD

class UserController:
    def __init__(self, user_db: UserCRUD, subscription_db: UserCurrencyCRUD):
        self.user_db = user_db
        self.subscription_db = subscription_db

    def create_user(self, name: str) -> int:
        return self.user_db.create(name)

    def list_users(self):
        rows = self.user_db.read_all()
        return [dict(row) for row in rows]

    def get_user_by_id(self, user_id: int):
        user = self.user_db.read_by_id(user_id)
        if not user:
            return None
        subscriptions = self.subscription_db.get_subscriptions(user_id)
        return {
            'user': dict(user),
            'subscriptions': [dict(c) for c in subscriptions]
        }