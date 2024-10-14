from core.db import get_db_connection
from exceptions import UserNotFoundError

async def get_user_info(user_id: str):
    conn = await get_db_connection()
    
    sql = """
    SELECT user_name, age, location
    FROM Users
    WHERE user_id = %s;
    """

    try:
        async with conn.cursor() as cur:
            await cur.execute(sql, (user_id,))
            user_info = await cur.fetchone()
            if user_info:
                return {
                    "name": user_info[0],
                    "age": user_info[1],
                    "location": user_info[2]
                }
            else:
                raise UserNotFoundError(f"존재하지 않는 user_id: {user_id}")
    finally:
        conn.close()

async def save_user_interests(user_id, interests):
    conn = await get_db_connection()

    sql = """
    INSERT INTO UserInterests (user_id, interest) 
    VALUES (%s, %s)
    """
    
    try:
        async with conn.cursor() as cursor:
            for interest in interests:
                await cursor.execute(sql, (user_id, interest))
            await conn.commit()
    finally:
        conn.close()