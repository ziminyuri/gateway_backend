from tests.constants import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                             POSTGRES_PORT, POSTGRES_USER)


def create_test_db_url():
    url = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
          f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    return url


def get_headers(access_token):
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
