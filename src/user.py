import db_base as db


class User:
    def __init__(self, username, password):
        self._username = username
        self._password = password

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password


class UserDb(db.DBbase):
    def reset_or_create_db(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Users;

                Create TABLE Users (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    username VARCHAR(20) NOT NULL,
                    password VARCHAR(20) NOT NULL,
                    privilege TEXT NOT NULL CHECK (privilege IN ('admin', 'user'))
                );
            """
            super().execute_script(sql)
            self.save_to_database("admin", 123, 'admin')
        except Exception as e:
            print(e)

    def save_to_database(self, username, password, privilege):
        try:
            super().get_cursor.execute(
                """
                INSERT INTO Users
                (username, password, privilege)
                    VALUES(?, ?, ?)
                """,
                (username, password, privilege)
            )
            super().get_connection.commit()
            print("Created new account for", username)
        except Exception as e:
            print(e)

    def check_privilege(self, user: User):
        try:
            self.get_cursor.execute(
                """
                SELECT privilege FROM Users WHERE username = ? AND password = ?
                """,
                (user.username, user.password)
            )
            result = self.get_cursor.fetchone()
            if result:
                return result[0]  # Return the privilege of the user
            else:
                return None  # User not found or invalid credentials
        except Exception as e:
            print(e)
            return None

    def reset_and_reload(self):
        self.reset_or_create_db()

# csv_lab = UserDb("RecipeManager.sqlite")
# csv_lab.reset_or_create_db()

