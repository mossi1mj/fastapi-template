import os
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.configuration import Configuration
from plaid.api_client import ApiClient

from app.database import get_db
from app.services.user import get_user_by_uid
from app.dependencies import verify_firebase_token  # You will create this

logger = logging.getLogger(__name__)
router = APIRouter()

# Setup Plaid configuration using environment variables
plaid_env = os.getenv("PLAID_ENV", "sandbox")
configuration = Configuration(
    host=f"https://{plaid_env}.plaid.com",
    api_key={
        "clientId": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
    }
)

api_client = ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)

@router.post("/create_link_token")
def create_link_token(uid: str):
    """
    Generate a new Plaid Link token using a Firebase UID.
    """
    logger.info(f"Generating link token for UID: {uid}")
    response = plaid_client.LinkToken.create({
        "user": {"client_user_id": uid},
        "client_name": "Your Budget App",
        "products": ["auth", "transactions", "balance"],
        "country_codes": ["US"],
        "language": "en",
        "redirect_uri": None
    })
    logger.info("Link token created successfully.")
    return {"link_token": response["link_token"]}

@router.post("/exchange_public_token")
def exchange_token(public_token: str, db: Session = Depends(get_db), uid: str = Depends(verify_firebase_token)):
    """
    Exchange a public token for an access token and save it to the user's record.
    """
    logger.info(f"Exchanging public token for UID: {uid}")
    exchange_response = plaid_client.Item.public_token.exchange(public_token)
    access_token = exchange_response["access_token"]
    item_id = exchange_response["item_id"]

    # Update user record
    user = get_user_by_uid(db, uid)
    if not user:
        logger.error(f"User with UID {uid} not found.")
        return {"error": "User not found."}
    user.access_token = access_token
    user.item_id = item_id
    db.commit()
    logger.info(f"Access token and item ID stored for user {uid}")

    return {"access_token": access_token, "item_id": item_id}

@router.get("/accounts")
def get_accounts(db: Session = Depends(get_db), uid: str = Depends(verify_firebase_token)):
    """
    Get linked bank accounts using the stored access token.
    """
    logger.info(f"Fetching accounts for UID: {uid}")
    user = get_user_by_uid(db, uid)
    if not user or not user.access_token:
        logger.warning("Access token not found.")
        return {"error": "User or access token not found."}

    accounts_response = plaid_client.Accounts.get(user.access_token)
    return accounts_response.to_dict()


@router.get("/balance")
def get_balance(db: Session = Depends(get_db), uid: str = Depends(verify_firebase_token)):
    """
    Get real-time balance for all accounts.
    """
    logger.info(f"Fetching balances for UID: {uid}")
    user = get_user_by_uid(db, uid)
    if not user or not user.access_token:
        return {"error": "User or access token not found."}

    response = plaid_client.Accounts.balance.get(user.access_token)
    return response.to_dict()


@router.get("/transactions")
def get_transactions(db: Session = Depends(get_db), uid: str = Depends(verify_firebase_token)):
    """
    Get recent transactions for the user.
    """
    logger.info(f"Fetching transactions for UID: {uid}")
    user = get_user_by_uid(db, uid)
    if not user or not user.access_token:
        return {"error": "User or access token not found."}

    from datetime import datetime, timedelta
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")

    response = plaid_client.Transactions.get(user.access_token, start_date, end_date)
    return response.to_dict()