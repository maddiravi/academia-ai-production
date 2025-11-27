import os
import requests
import logging

logger = logging.getLogger("HealthCheck")

def check_openrouter_api_health(api_key: str) -> bool:
    """
    Performs a simple health check by hitting the OpenRouter API endpoint.
    Verifies connectivity and API key validity before running expensive agents.
    """
    if not api_key:
        logger.error("Health check failed: OPENROUTER_API_KEY is missing.")
        return False

    url = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1") + "/models"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        # Set explicit timeout for the health check itself
        response = requests.get(url, headers=headers, timeout=5) 
        
        if response.status_code == 200:
            logger.info("OpenRouter API Health Check: SUCCESS (200 OK).")
            return True
        else:
            logger.error(f"Health Check FAILED. Status: {response.status_code}. Key may be invalid.")
            return False
    except Exception as e:
        logger.error(f"Health Check CONNECTION ERROR: {e}")
        return False