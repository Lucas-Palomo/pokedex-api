from .database import Database


def get_env_variable(envs: dict, variable: str) -> str:
    var = envs.get(variable, None)
    if var is None:
        exit("Missing {} in .env file".format(variable))
    return str(var)


def database(envs: dict) -> Database:
    pg_user = get_env_variable(envs, "POSTGRES_USER")
    pg_password = get_env_variable(envs, "POSTGRES_PASSWORD")
    pg_db = get_env_variable(envs, "POSTGRES_DB")
    pg_host = get_env_variable(envs, "POSTGRES_HOST")
    pg_port = get_env_variable(envs, "POSTGRES_PORT")

    return Database(host=pg_host, port=pg_port, database=pg_db, user=pg_user, password=pg_password)