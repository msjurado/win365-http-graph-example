from utilities.auth import create_client_assertion, get_access_token
from endpoints.cloud_pcs import get_cloud_pcs
from dotenv import load_dotenv
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Tenant configuration
tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
private_key = os.getenv("PRIVATE_KEY")
private_key_passphrase = bytes(os.getenv("PRIVATE_KEY_PASSPHRASE"), 'utf-8')
cert_thumbprint = os.getenv("CERT_THUMBPRINT")
scope = "https://graph.microsoft.com/.default"

# Create client assertion that will be used to obtain the access token
client_assertion = create_client_assertion(client_id, tenant_id, cert_thumbprint, private_key, private_key_passphrase)

# Exit script if not able to create client assertion
if not client_assertion:
    logger.error("Failed to create client assertion.")
    exit(1)

# Obtain access token using the client assertion
access_token = get_access_token(client_assertion, tenant_id, client_id, scope)

# Exit script if not able to obtain access token
if not access_token:
    logger.error("Failed to obtain access token.")
    exit(1)

# Get list of Cloud PCs
cloud_pcs = get_cloud_pcs(access_token)
if "error" in cloud_pcs:
    logger.error(f"Error fetching Cloud PCs: {cloud_pcs['error']}")
else:
    for pc in cloud_pcs.get("value", []):
        logger.info(f"Name: {pc.get('displayName')}, Status: {pc.get('status')}, User: {pc.get('userPrincipalName')}")