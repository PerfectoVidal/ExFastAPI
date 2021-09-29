import settings_db
from users.models import User

if __name__ == '__main__':
    settings_db.Base.metadata.create_all(settings_db.engine)
