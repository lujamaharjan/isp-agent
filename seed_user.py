# create_user.py
import asyncio
from core.database import init_db, create_user

async def main():
    await init_db()
    await create_user("admin", "secret", role="admin")
    print("User created.")

if __name__ == "__main__":
    asyncio.run(main())