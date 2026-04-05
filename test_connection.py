from pymongo import MongoClient
import sys
import os
from dotenv import load_dotenv
from src.heart_disease.db.srv_dns import prefer_public_dns_for_srv

# Load environment variables from .env
load_dotenv()

# Get MongoDB URL
MONGODB_URL = os.getenv("MONGODB_URL")
if not MONGODB_URL:
    print("❌ MONGODB_URL missing in .env")
    sys.exit(1)

# Force public DNS for SRV URLs (Atlas workaround)
prefer_public_dns_for_srv(MONGODB_URL)

# Create MongoDB client with timeout
client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=15000)

# Test connection
try:
    client.admin.command("ping")
    print("✅ Connected successfully to MongoDB!")
except Exception as e:
    print("❌ Connection failed:", e)
    print("If this persists: use local/Docker MongoDB or Atlas standard (non-SRV) URL.")
    sys.exit(1)
