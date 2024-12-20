import motor.motor_asyncio
from os import environ

DATABASE_URL = environ.get('DATABASE_URL', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")

class Database:
    
    def __init__(self, db_url, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups


    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )


    def new_group(self, id, title, username):
        return dict(
            id = id,
            title = title,
            username = username,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

db = Database(DATABASE_URL, DATABASE_NAME)