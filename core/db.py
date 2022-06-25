import asyncpg


async def check_user_data(connection_params, user, password):
    connection = await asyncpg.connect(**connection_params)
    query = "select id from tag_system.users where login = $1 and hash = $2"
    user_id = await connection.fetchrow(query, user, password)
    return user_id != [], user_id[0] if user_id != [] else None
