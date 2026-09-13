import asyncio

from app.core.database import create_user, init_db


async def main() -> None:
    await init_db()
    await create_user("admin", "secret", role="admin")
    print("User created.")


if __name__ == "__main__":
    asyncio.run(main())