import logging
import sys
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from outscraper import ApiClient

# Load environment variables from .env file
load_dotenv()

# Set up logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("outscraper-mcp-server")

# Get API key from environment variables (now including those loaded from .env)
OUTSCRAPER_API_KEY = os.getenv("OUTSCRAPER_API_KEY")
if not OUTSCRAPER_API_KEY:
    logger.warning("OUTSCRAPER_API_KEY environment variable not set. API calls will fail.")

client = ApiClient(api_key=OUTSCRAPER_API_KEY)


mcp = FastMCP("Outscraper MCP Server")


@mcp.tool()
def maps_search(query: str, limit: int = 20, language: str = "en", region: str = None):
    """Search businesses or places on Google Maps."""
    logger.info(f"Searching Google Maps for: {query} (limit={limit}, language={language}, region={region})")
    try:
        result = client.google_maps_search([query], limit=limit, language=language, region=region)
        logger.info(f"Search completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error searching Google Maps: {str(e)}")
        raise

@mcp.tool()
def maps_reviews(place_id: str, reviews_limit: int = 20, language: str = "en", sort: str = "newest", cutoff: int = None):
    """Get reviews for a Google Maps place."""
    logger.info(f"Getting reviews for place_id: {place_id} (reviews_limit={reviews_limit}, language={language}, sort={sort})")
    try:
        result = client.google_maps_reviews(place_id, reviews_limit=reviews_limit, language=language, sort=sort, cutoff=cutoff)
        logger.info(f"Successfully retrieved reviews")
        return result
    except Exception as e:
        logger.error(f"Error getting Google Maps reviews: {str(e)}")
        raise

@mcp.tool()
def google_search(query: str, language: str = "en", region: str = None):
    """Search Google."""
    logger.info(f"Searching Google for: {query} (language={language}, region={region})")
    try:
        result = client.google_search([query], language=language, region=region)
        logger.info(f"Search completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error searching Google: {str(e)}")
        raise

@mcp.tool()
def google_search_news(query: str, language: str = "en", region: str = None):
    """Search Google News."""
    logger.info(f"Searching Google News for: {query} (language={language}, region={region})")
    try:
        result = client.google_search_news([query], language=language, region=region)
        logger.info(f"News search completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error searching Google News: {str(e)}")
        raise

@mcp.tool()
def maps_photos(query: str, photos_limit: int = 20, language: str = "en"):
    """Get photos from Google Maps places."""
    logger.info(f"Getting photos for: {query} (photos_limit={photos_limit}, language={language})")
    try:
        # Use photosLimit parameter name as expected by the API
        result = client.google_maps_photos(query, photosLimit=photos_limit, language=language)
        logger.info(f"Successfully retrieved photos")
        return result
    except Exception as e:
        logger.error(f"Error getting Google Maps photos: {str(e)}")
        raise

@mcp.tool()
def maps_directions(origins_destinations: list):
    """Get directions between locations on Google Maps.

    Format: ['origin_lat,origin_lng destination_lat,destination_lng', ...]
    Example: ['29.696596,76.994928 30.7159662444353,76.8053887016268']
    """
    logger.info(f"Getting directions for: {origins_destinations}")
    try:
        result = client.google_maps_directions(origins_destinations)
        logger.info(f"Successfully retrieved directions")
        return result
    except Exception as e:
        logger.error(f"Error getting Google Maps directions: {str(e)}")
        raise

@mcp.tool()
def google_play_reviews(app_id: str, reviews_limit: int = 20, language: str = "en"):
    """Get reviews for an app from Google Play Store.

    Example app_id: 'com.facebook.katana' for Facebook
    """
    logger.info(f"Getting reviews for app_id: {app_id} (reviews_limit={reviews_limit}, language={language})")
    try:
        result = client.google_play_reviews(app_id, reviews_limit=reviews_limit, language=language)
        logger.info(f"Successfully retrieved app reviews")
        return result
    except Exception as e:
        logger.error(f"Error getting Google Play reviews: {str(e)}")
        raise

@mcp.tool()
def emails_and_contacts(domains: list):
    """Extract emails and contact information from websites.

    Example: ['outscraper.com']
    """
    logger.info(f"Extracting emails and contacts from domains: {domains}")
    try:
        result = client.emails_and_contacts(domains)
        logger.info(f"Successfully extracted emails and contacts")
        return result
    except Exception as e:
        logger.error(f"Error extracting emails and contacts: {str(e)}")
        raise

def run():
    logger.info("Starting Outscraper MCP Server...")
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise
