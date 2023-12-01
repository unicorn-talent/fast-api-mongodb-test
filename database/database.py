from models.wallet import Wallet

from motor.motor_asyncio import AsyncIOMotorClient
from config.config import Settings

DATABASE_URL = Settings().DATABASE_URL
DATABASE_NAME = Settings().DATABASE_NAME

client = AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]
wallet_collection = db["Wallet"]

async def add_wallet(balance_data: Wallet) -> bool:
    try:
        wallet_collection.update_one({"wallet": balance_data["wallet"]}, {"$set": balance_data}, upsert=True)
        return "Added balances successfully"
    except Exception as e:
        return "Something went wrong"

async def get_wallet(address: str):
    try:
         # Find documents where wallet address matches the parameter's address
        matching_wallets = await db["Wallet"].find_one({'wallet': address})
        return matching_wallets
    except Exception as e:
        print(str(e))
        return "Something went wrong"