import asyncpg


async def get_user_creds(connection_params, user):
    connection = await asyncpg.connect(**connection_params)
    query = "select id, hash from tag_system.users where login = $1"
    result = await connection.fetchrow(query, user)
    if result is not None:
        return result[0], result[1]
    return None, None