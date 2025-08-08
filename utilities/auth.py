from cryptography.hazmat.primitives import serialization
import logging
import uuid
import time
import jwt
import base64
import httpx

# Setup logging
logger = logging.getLogger(__name__)

def create_client_assertion(client_id: str, tenant_id: str, cert_thumbprint: str, private_key: str, private_key_passphrase: bytes) -> str | None:
    try:
        # Load the private key
        with open(private_key, 'rb') as private_key_file:
            private_key_data = serialization.load_pem_private_key(
                private_key_file.read(),
                password=private_key_passphrase
            )
        
        # Serialize private key for signing assertion
        private_key_pem = private_key_data.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Create JWT client assertion payload
        jwt_payload = {
            "aud": f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
            "iss": client_id,
            "sub": client_id,
            "jti": str(uuid.uuid4()),
            "nbf": int(time.time()),
            "exp": int(time.time()) + 600  # Token valid for 10 minutes
        }

        # Convert thumbprint to base64 to be used as x5t header in JWT client assertion
        thumbprint_bytes = bytes.fromhex(cert_thumbprint)
        thumbprint_encoded_bytes = base64.b64encode(thumbprint_bytes)
        thumbprint_base64 = thumbprint_encoded_bytes.decode('utf-8')

        # Sign JWT client assertion
        jwt_client_assertion = jwt.encode(jwt_payload, private_key_pem, algorithm="RS256", headers={"x5t": thumbprint_base64})

        # Return the signed JWT client assertion
        return jwt_client_assertion

    except Exception as e:
        logging.error(f"Error creating client assertion: {e}")
        return None

def get_access_token(client_assertion: str, tenant_id: str, client_id: str, scope: str) -> str | None:
    try:
        # Prepare data to be sent to the token endpoint to obtain access token
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "scope": scope,
            "client_assertion": client_assertion,
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
        }
        
        # Retrieve access token by making a POST request to the token endpoint
        response = httpx.post(token_url, data=token_data)
        response.raise_for_status()
        
        # Parse the response and return the access token
        tokens = response.json()
        return tokens.get('access_token')

    except Exception as e:
        logging.error(f"Error obtaining access token: {e}")
        return None