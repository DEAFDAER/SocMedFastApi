import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from neomodel import config

import os as _os

# Load .env located next to this config.py (app/.env) so values resolve regardless of cwd
_base_dir = _os.path.dirname(__file__)
_dotenv_path = _os.path.join(_base_dir, ".env")
load_dotenv(_dotenv_path)

# Read environment variables (support Aura which uses NEO4J_USERNAME)
NEO4J_USER = os.getenv("NEO4J_USER") or os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")  # no quotes needed
NEO4J_URI = os.getenv("NEO4J_URI")  # e.g. neo4j+s://<host> or bolt://localhost:7687
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")  # optional (Aura provides this)

# Basic validation to avoid passing None or unexpected types to quote_plus
if not NEO4J_USER or not NEO4J_PASSWORD or not NEO4J_URI:
	raise RuntimeError(
		"Missing Neo4j environment variables. Ensure .env contains NEO4J_USER, NEO4J_PASSWORD, and NEO4J_URI"
	)

# Ensure they are strings
NEO4J_USER = str(NEO4J_USER)
NEO4J_PASSWORD = str(NEO4J_PASSWORD)
NEO4J_URI = str(NEO4J_URI)

# URL-encode the password safely
encoded_password = quote_plus(NEO4J_PASSWORD, safe="")

# Build the DATABASE_URL preserving the scheme and host part of NEO4J_URI
if "://" in NEO4J_URI:
	scheme, host_port = NEO4J_URI.split("://", 1)
else:
	# default scheme to neo4j if not present
	scheme = "neo4j"
	host_port = NEO4J_URI

config.DATABASE_URL = f"{scheme}://{NEO4J_USER}:{encoded_password}@{host_port}"

# If a specific database name is provided (Aurа), set it for neomodel
if NEO4J_DATABASE:
	try:
		config.DATABASE_NAME = str(NEO4J_DATABASE)
	except Exception:
		pass

print("[ℹ️] Connecting to Neo4j at:", config.DATABASE_URL, "database=", NEO4J_DATABASE)
