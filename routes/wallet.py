from fastapi import APIRouter, HTTPException
from database.database import add_wallet, get_wallet
from web3 import Web3
import re
from datetime import datetime
from config.config import Settings
from erc20_abi import token_abi
import httpx

router = APIRouter()

WEB3_PROVIDER_URL = Settings().WEB3_PROVIDER_URL
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

async def get_token_price(token_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{COINGECKO_API_URL}/simple/price", params={"ids": token_id, "vs_currencies": "usd"})
        data = response.json()
        return data.get(token_id, {}).get("usd")

async def update_balance_history(wallet_address, timestamp, token_balance, usd_balance):
    # Retrieve the current document
    document = await get_wallet(wallet_address)

    if document is None:
        new_entry = {
            "timestamp": timestamp.isoformat(),
            "token_balance": token_balance,
            "usd_balance": usd_balance
        }
        # If no document found, create a new one
        document = {
            "wallet": wallet_address,
            "balances_history": [new_entry],
            "last_update_time": timestamp,
            "token_balance": token_balance,
            "usd_balance": usd_balance
        }
    else:
        # Update existing document
        document["last_update_time"] = timestamp
        document["token_balance"] = token_balance
        document["usd_balance"] = usd_balance
    
        # Update the balances_history array with the new entry
        new_entry = {
            "timestamp": timestamp.isoformat(),
            "token_balance": token_balance,
            "usd_balance": usd_balance
        }
        document["balances_history"].append(new_entry)
    
    # Update or insert the document in the database
    return await add_wallet(document)


# Endpoint to fetch wallet balances
@router.get("/balances/{address}")
async def get_wallet_balances(address: str):
    try:
        wallet_address = w3.to_checksum_address(address.lower())

        if not re.match(r"^0x[a-fA-F0-9]{40}$", wallet_address):
            raise HTTPException(status_code=400, detail="Invalid Ethereum address")

        token_address = Settings().CRV_token
        token_address_checksum = w3.to_checksum_address(token_address.lower())
        contract = w3.eth.contract(address=token_address_checksum, abi=token_abi)

        balance_wei = contract.functions.balanceOf(wallet_address).call()

        # Convert balance from Wei to token's decimal precision
        token_decimals = contract.functions.decimals().call()
        balance_token = balance_wei / 10**token_decimals


        token_id = "curve-dao-token"
        token_price_usd = await get_token_price(token_id)
        if token_price_usd is None:
            raise HTTPException(status_code=500, detail="Failed to fetch token price from CoinGecko")
        
        # Calculate USD balance
        usd_balance = balance_token * token_price_usd

        # Save data to MongoDB
        timestamp = datetime.now()

        # Update balances_history array
        return await update_balance_history(wallet_address, timestamp, balance_token, usd_balance)

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))
    

# Endpoint to fetch wallet balances
@router.get("/info/{address}")
async def get_wallet_info(address: str):
    try:
        wallet_address = w3.to_checksum_address(address.lower())
        get_data = await get_wallet(wallet_address)
        
        if get_data is None:
            raise HTTPException(status_code=404, detail="Wallet not found")
        
        # Convert the MongoDB document to a dictionary and remove the _id field
        data_without_id = {key: value for key, value in get_data.items() if key != "_id"}
        
        # Include the complete balances history
        balances_history = data_without_id.get("balances_history", [])
        data_without_id["balances_history"] = balances_history
        
        return data_without_id
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))