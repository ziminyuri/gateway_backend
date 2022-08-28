import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
import uuid
import datetime


class PostgresSaver:
    def __init__(self, connection: _connection):
        self.__connection = connection

    def save_data(self, query: str):
        cursor: DictCursor = self.__connection.cursor()
        try:
            cursor.execute(query)
            self.__connection.commit()
        except Exception as e:
            print(f"Ошибка записи в PostgreSQL: {e}")

    def get_data(self, query: str):
        cursor: DictCursor = self.__connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def add_fake_data(pg_conn: _connection):
    """ Наполнение БД фейковыми данными """
    postgres_saver = PostgresSaver(pg_conn)

    n = 5
    for i in range(1, 3):
        create_role_query = f"INSERT INTO role (name) VALUES ('new_user_{i}');"
        postgres_saver.save_data(create_role_query)
        role = postgres_saver.get_data(f"select * from role where name = 'new_user_{i}' ")
        role_id = role[0][0]
        today = datetime.datetime.today()
        for j in range(n*i, n*i+n):
            id = uuid.uuid4()
            profile_id = uuid.uuid4()
            create_user_query = f"INSERT INTO public.user (id, username, hashed_password," \
                                f" is_active, is_superuser) " \
                                f"VALUES ('{id}', 'testtest{j}', 'test', true, false);"
            postgres_saver.save_data(create_user_query)
            create_user_role_query = f"INSERT INTO public.user_role (user_id, role_id) " \
                                     f"VALUES ('{id}', '{role_id}');"
            postgres_saver.save_data(create_user_role_query)

            create_user_profile_query = f"INSERT INTO public.profile " \
                                        f"(id, is_active, first_name, last_name, phone," \
                                        f" email, user_id, birthday) " \
                                        f"VALUES ('{profile_id}', true, 'Иван{j}','Иванов{j}'," \
                                        f" '7999999{j}', 'test{j}@yandex.ru', '{id}', '{today}');"
            postgres_saver.save_data(create_user_profile_query)


if __name__ == '__main__':
    dsl = {
            'dbname': 'ms_auth',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': '5432'
        }

    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        add_fake_data(pg_conn)
