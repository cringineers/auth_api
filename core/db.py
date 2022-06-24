from sqlalchemy import text


async def check_user_data(engine, user, password):
    async with engine.connect() as connection:
        query = text("""
            select id from tag_system.users where login = :name and hash = :hash
        """)
        user_id = await connection.execute(query, {"name": user, "hash": password})
        user_id = user_id.fetchall()
        await connection.commit()
    return user_id != [], user_id[0][0] if user_id != [] else None
