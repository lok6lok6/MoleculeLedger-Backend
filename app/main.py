# app/main.py
from fastapi import FastAPI
from web3 import Web3
from dotenv import load_dotenv
import os

# --- Load environment variables from .env file ---
# Purpose: python-dotenv loads key-value pairs from a .env file into
# environment variables. This is one of the best practice for managing configurations
# (like API keys) securely, keeping them out of my codebase.
load_dotenv()

# --- FastAPI Application Instance ---
# Role: This line creates the FastAPI application instance. This 'app' object
# is the core of our web service, defining routes and managing the server.
app = FastAPI(
    title="Molecule Ledger Backend API",
    description="API for managing molecular science experiments and blockchain interactions.",
    version="0.1.0",
)

# --- Blockchain Configuration (Example using Infura for Sepolia Testnet) ---
# Role: Configures the connection to the Ethereum blockchain. We're using
# Sepolia Testnet for development to avoid real transaction costs.
# We'll connect via Infura, a blockchain node provider.
# Best Practice: Your Infura Project ID is a sensitive credential and should
# be stored as an environment variable, NOT directly in the code.
INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID")
if not INFURA_PROJECT_ID:
    raise ValueError("INFURA_PROJECT_ID not found in .env file. Please create one.")

INFURA_URL = f"https://sepolia.infura.io/v3/{INFURA_PROJECT_ID}"
# Web3.py: The Python library for interacting with Ethereum.
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# --- FastAPI Startup Event ---
# Purpose: This decorator ensures the 'startup_event' function runs when the
# FastAPI application starts. It's a good place to perform initializations
# like database connections or, in this case, blockchain connection checks.
@app.on_event("startup")
async def startup_event():
    print("Molecule Ledger Backend starting up...")
    # Check if connected to the blockchain
    if web3.is_connected():
        # web3.eth.chain_id returns the ID of the connected chain (Sepolia's is often 11155111)
        print(f"Connected to Ethereum network: Chain ID {web3.eth.chain_id} (Sepolia Testnet)")
    else:
        print("Failed to connect to Ethereum network! Check INFURA_PROJECT_ID or network.")

# --- Root Endpoint ---
# Purpose: A simple endpoint to confirm the API is running.
@app.get("/")
async def read_root():
    return {"message": "Welcome to Molecule Ledger API!"}

# --- Status Endpoint ---
# Purpose: Provides a health check for the API, including blockchain connection status.
@app.get("/status")
async def get_status():
    is_blockchain_connected = web3.is_connected()
    current_block = None
    if is_blockchain_connected:
        try:
            current_block = web3.eth.block_number
        except Exception as e:
            print(f"Error fetching block number: {e}")
            current_block = "N/A" # Handle potential errors if connection drops after is_connected check

    return {
        "api_status": "online",
        "blockchain_connected": is_blockchain_connected,
        "current_block": current_block,
        "version": app.version
    }

# How to run this file:
# Save it as main.py inside the 'app' directory of my MoleculeLedgerBackend project.
# From the MoleculeLedgerBackend directory (one level above 'app'), run:
# uvicorn app.main:app --reload