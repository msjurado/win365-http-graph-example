import httpx
import logging

logger = logging.getLogger(__name__)

# Requires CloudPC.Read.All permission
def get_cloud_pcs(access_token: str) -> dict:
    try:
        # Prepare headers to pass bearer token for authentication
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Make a GET request to the Cloud PCs endpoint
        response = httpx.get("https://graph.microsoft.com/v1.0/deviceManagement/virtualEndpoint/cloudPCs", headers=headers)
        response.raise_for_status()

        # Return the JSON response containing Cloud PCs
        return response.json()
    
    except httpx.HTTPError as e:
        logger.error(f"Error fetching Cloud PCs: {e}")
        return {"error": str(e)}