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
        logging.StreamHandler(sys.stderr)
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
def google_maps_search(query: str, limit: int = 20, drop_duplicates: bool = False, language: str = 'en',
                      region: str = None, skip: int = 0, coordinates: str = None, enrichment: list = None,
                      fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Search businesses or places on Google Maps.

    Examples:
    - Find coffee shops: google_maps_search("coffee shops in san francisco", limit=5)
    - Get details for specific place: google_maps_search("ChIJIQBpAG2ahYAR_6128GcTUEo")

    Parameters:
        query (str): Search query, place name, or google_id.
        limit (int): Maximum places to retrieve per query. Default: 20.
        drop_duplicates (bool): Whether to remove duplicate results across queries.
        language (str): Results language code. Default: 'en'.
        region (str): Region code (e.g., 'US', 'GB').
        skip (int): Skip first N places (must be multiple of 20). Used for pagination.
        coordinates (str): Location coordinates as "latitude,longitude".
        enrichment (list): Data enrichments to apply to results.
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Searching Google Maps for: {query} (limit={limit}, language={language}, region={region})")
    try:
        result = client.google_maps_search([query], limit=limit, drop_duplicates=drop_duplicates,
                                         language=language, region=region, skip=skip,
                                         coordinates=coordinates, enrichment=enrichment,
                                         fields=fields, async_request=async_request,
                                         ui=ui, webhook=webhook)
        logger.info(f"Search completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error searching Google Maps: {str(e)}")
        raise

@mcp.tool()
def google_maps_reviews(query: str, reviews_limit: int = 10, limit: int = 1, sort: str = 'most_relevant',
                       start: int = None, cutoff: int = None, cutoff_rating: int = None, ignore_empty: bool = False,
                       language: str = 'en', region: str = None, reviews_query: str = None, source: str = None,
                       last_pagination_id: str = None, fields: str = None, async_request: bool = False,
                       ui: bool = None, webhook: str = None):
    """Get reviews for Google Maps places.

    Examples:
    - Get reviews for a place by ID: google_maps_reviews("ChIJIQBpAG2ahYAR_6128GcTUEo", reviews_limit=10)
    - Get reviews for a place by URL: google_maps_reviews("https://www.google.com/maps/place/Eiffel+Tower")

    Parameters:
        query (str): Search query, place_id, google_id or Maps URL.
        reviews_limit (int): Maximum reviews to extract per place. Default: 10.
        limit (int): Maximum places to retrieve per query. Default: 1.
        sort (str): Sort order - 'most_relevant', 'newest', 'highest_rating', 'lowest_rating'. Default: 'most_relevant'.
        start (int): Start timestamp for reviews (sets sort to 'newest').
        cutoff (int): Maximum timestamp for reviews (sets sort to 'newest').
        cutoff_rating (int): Min/max rating filter (requires appropriate sort).
        ignore_empty (bool): Whether to ignore reviews without text.
        language (str): Results language code. Default: 'en'.
        region (str): Region code (e.g., 'US', 'GB').
        reviews_query (str): Search term to filter reviews.
        source (str): Source filter (e.g., 'Booking.com', 'Expedia').
        last_pagination_id (str): ID of last item for pagination.
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting reviews for: {query} (reviews_limit={reviews_limit}, language={language}, sort={sort})")
    try:
        result = client.google_maps_reviews(query, reviews_limit=reviews_limit, limit=limit, sort=sort,
                                          start=start, cutoff=cutoff, cutoff_rating=cutoff_rating,
                                          ignore_empty=ignore_empty, language=language, region=region,
                                          reviews_query=reviews_query, source=source, 
                                          last_pagination_id=last_pagination_id, fields=fields,
                                          async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved reviews")
        return result
    except Exception as e:
        logger.error(f"Error getting Google Maps reviews: {str(e)}")
        raise

@mcp.tool()
def google_search(query: str, pages_per_query: int = 1, uule: str = None, language: str = "en", region: str = None,
               fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Search Google.

    Examples:
    - Simple search: google_search("what is the weather in london")
    - Search with multiple pages: google_search("python tutorials", pages_per_query=2)

    Parameters:
        query (str): Search query for Google.
        pages_per_query (int): Number of pages to return. Default: 1.
        uule (str): Google UULE location parameter.
        language (str): Results language code. Default: 'en'.
        region (str): Region/country code (e.g., 'US', 'GB', 'CA').
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.

    Returns:
        list: Google search results with organic listings, ads, and related data.
    """
    logger.info(f"Searching Google for: {query} (language={language}, region={region})")
    try:
        result = client.google_search([query], pages_per_query=pages_per_query, uule=uule,
                                    language=language, region=region, fields=fields,
                                    async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Search completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error searching Google: {str(e)}")
        raise

@mcp.tool()
def google_search_news(query: str, pages_per_query: int = 1, uule: str = None, tbs: str = None, language: str = "en", 
                   region: str = None, fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Search Google News.

    Examples:
    - Search for news: google_search_news("latest technology news")
    - Search news in a specific region: google_search_news("stock market today", region="US")

    Parameters:
        query (str): Search query for Google News.
        pages_per_query (int): Number of pages to return. Default: 1.
        uule (str): Google UULE location parameter.
        tbs (str): Date range filter (h: hour, d: day, w: week, m: month, y: year).
        language (str): Results language code. Default: 'en'.
        region (str): Region/country code (e.g., 'US', 'GB', 'CA').
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.

    Returns:
        list: Google News search results with articles and metadata.
    """
    logger.info(f"Searching Google News for: {query} (language={language}, region={region})")
    try:
        result = client.google_search_news([query], pages_per_query=pages_per_query, uule=uule, tbs=tbs,
                                         language=language, region=region, fields=fields,
                                         async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"News search completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error searching Google News: {str(e)}")
        raise

@mcp.tool()
def google_maps_photos(query: str, photos_limit: int = 20, limit: int = 1, tag: str = None, language: str = 'en',
                      region: str = None, fields: str = None, async_request: bool = False, ui: bool = None,
                      webhook: str = None):
    """Get photos from Google Maps places.

    Examples:
    - Get photos of a place: google_maps_photos("Eiffel Tower", photos_limit=10)
    - Get photos for a specific place ID: google_maps_photos("ChIJIQBpAG2ahYAR_6128GcTUEo")

    Parameters:
        query (str): Search query, place_id, google_id or Maps URL.
        photos_limit (int): Maximum photos to extract per place. Default: 20.
        limit (int): Maximum places to retrieve per query. Default: 1.
        tag (str): Filter type - 'all', 'latest', 'menu', 'by_owner'.
        language (str): Results language code. Default: 'en'.
        region (str): Region code (e.g., 'US', 'GB').
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting photos for: {query} (photos_limit={photos_limit}, language={language})")
    try:
        result = client.google_maps_photos(query, photosLimit=photos_limit, limit=limit, tag=tag,
                                         language=language, region=region, fields=fields,
                                         async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved photos")
        return result
    except Exception as e:
        logger.error(f"Error getting Google Maps photos: {str(e)}")
        raise

@mcp.tool()
def google_maps_directions(origins_destinations: list, departure_time: int = None, finish_time: int = None,
                          interval: int = 60, travel_mode: str = 'best', language: str = 'en',
                          region: str = None, fields: str = None, async_request: bool = False,
                          ui: bool = None, webhook: str = None):
    """Get directions between locations on Google Maps.

    Examples:
    - Get directions between two airports: google_maps_directions(origins_destinations=["SFO to LAX"])
    - Get walking directions using coordinates: google_maps_directions(origins_destinations=["48.8584,2.2945 48.8606,2.3376"], travel_mode="walk")
    Format: ['origin_lat,origin_lng destination_lat,destination_lng', ...]
    Example: ['29.696596,76.994928 30.7159662444353,76.8053887016268']

    Parameters:
        origins_destinations (list): Queries with format "<origin> <destination>".
        departure_time (int): Departure timestamp (default: current time).
        finish_time (int): End departure timestamp (requires interval).
        interval (int): Interval between departure_time and finish_time. Default: 60.
        travel_mode (str): Mode of travel - 'best', 'car', 'transit', 'walk', 'bike', 'flight'. Default: 'best'.
        language (str): Results language code. Default: 'en'.
        region (str): Region code (e.g., 'US', 'GB').
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting directions for: {origins_destinations}")
    try:
        result = client.google_maps_directions(origins_destinations, departure_time=departure_time,
                                             finish_time=finish_time, interval=interval,
                                             travel_mode=travel_mode, language=language,
                                             region=region, fields=fields,
                                             async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved directions")
        return result
    except Exception as e:
        logger.error(f"Error getting Google Maps directions: {str(e)}")
        raise

@mcp.tool()
def google_play_reviews(app_id: str, reviews_limit: int = 20, sort: str = 'most_relevant', cutoff: int = None,
                      rating: int = None, language: str = "en", fields: str = None, async_request: bool = False,
                      ui: bool = None, webhook: str = None):
    """Get reviews for an app from Google Play Store.

    Examples:
    - Get reviews for an app: google_play_reviews("com.google.android.apps.maps", reviews_limit=50)
    - Get newest reviews for an app: google_play_reviews("com.spotify.music", sort="newest")
    Example app_id: 'com.facebook.katana' for Facebook
    Parameters:
        app_id (str): App ID or direct link (e.g., 'com.facebook.katana').
        reviews_limit (int): Maximum reviews to extract. Default: 20.
        sort (str): Sort order - 'most_relevant', 'newest', or 'rating'. Default: 'most_relevant'.
        cutoff (int): Maximum timestamp for reviews (overwrites sort to 'newest').
        rating (int): Filter by specific rating (works only with sort='rating').
        language (str): Results language code. Default: 'en'.
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting reviews for app_id: {app_id} (reviews_limit={reviews_limit}, language={language})")
    try:
        result = client.google_play_reviews(app_id, reviews_limit=reviews_limit, sort=sort, cutoff=cutoff,
                                          rating=rating, language=language, fields=fields,
                                          async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved app reviews")
        return result
    except Exception as e:
        logger.error(f"Error getting Google Play reviews: {str(e)}")
        raise

@mcp.tool()
def emails_and_contacts(domains: list, fields: str = None):
    """Extract emails and contact information from websites.

    Examples:
    - Extract contacts from a single domain: emails_and_contacts(domains=["outscraper.com"])
    - Extract contacts from multiple domains: emails_and_contacts(domains=["github.com", "linkedin.com"])
    Example: ['outscraper.com']

    Parameters:
        domains (list): Domains or links to extract information from.
        fields (str): Fields to include in response.
    """
    logger.info(f"Extracting emails and contacts from domains: {domains}")
    try:
        result = client.emails_and_contacts(domains, fields=fields)
        logger.info(f"Successfully extracted emails and contacts")
        return result
    except Exception as e:
        logger.error(f"Error extracting emails and contacts: {str(e)}")
        raise

@mcp.tool()
def phones_enricher(query: list, fields: str = None):
    """Returns phones carrier data, validates phones, ensures messages deliverability.

    Examples:
    - Enrich a single phone number: phones_enricher(query=["+14155552671"])
    - Enrich multiple phone numbers: phones_enricher(query=["+442079460000", "+33153017600"])

    Parameters:
        query (list): Phone numbers to check (e.g., ['+1 281 236 8208']).
        fields (str): Fields to include in response.
    """
    logger.info(f"Enriching phone data for: {query}")
    try:
        result = client.phones_enricher(query, fields=fields)
        logger.info(f"Successfully enriched phone data")
        return result
    except Exception as e:
        logger.error(f"Error enriching phone data: {str(e)}")
        raise

@mcp.tool()
def amazon_products(query: list, limit: int = 24, domain: str = 'amazon.com', postal_code: str = '11201',
                    fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns information about products on Amazon.

    Examples:
    - Search for products: amazon_products(query=["https://www.amazon.com/s?k=laptop"], limit=10)
    - Get product details: amazon_products(query=["https://www.amazon.com/dp/B0862269YP"])

    Parameters:
        query (list): Amazon product or summary pages URLs.
        limit (int): Maximum products to get from one query. Default: 24.
        domain (str): Amazon domain to use (e.g., 'amazon.com', 'amazon.co.uk'). Default: 'amazon.com'.
        postal_code (str): Postal code for delivery. Default: '11201'.
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting Amazon products for: {query} (limit={limit}, domain={domain})")
    try:
        result = client.amazon_products(query, limit=limit, domain=domain, postal_code=postal_code,
                                      fields=fields, async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved Amazon products")
        return result
    except Exception as e:
        logger.error(f"Error getting Amazon products: {str(e)}")
        raise

@mcp.tool()
def amazon_reviews(query: list, limit: int = 10, sort: str = 'helpful', filter_by_reviewer: str = 'all_reviews',
                   filter_by_star: str = 'all_stars', domain: str = None, fields: str = None,
                   async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns reviews from Amazon products.

    Examples:
    - Get reviews for a product by ASIN: amazon_reviews(query=["B0862269YP"], limit=20)
    - Get recent reviews for a product by URL: amazon_reviews(query=["https://www.amazon.com/dp/1612680194"], sort="recent")

    Parameters:
        query (list): URLs or ASINs from Amazon products (e.g., 'https://www.amazon.com/dp/1612680194', '1612680194').
        limit (int): Maximum reviews to get from one query. Default: 10.
        sort (str): Sort type - 'helpful' or 'recent'. Default: 'helpful'.
        filter_by_reviewer (str): Reviewer filter - 'all_reviews' or 'avp_only_reviews'. Default: 'all_reviews'.
        filter_by_star (str): Star rating filter (e.g., 'all_stars', 'five_star', 'positive'). Default: 'all_stars'.
        domain (str): Amazon domain to use (e.g., 'amazon.com', 'amazon.co.uk').
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting Amazon reviews for: {query} (limit={limit}, sort={sort})")
    try:
        result = client.amazon_reviews(query, limit=limit, sort=sort, filter_by_reviewer=filter_by_reviewer,
                                     filter_by_star=filter_by_star, domain=domain, fields=fields,
                                     async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved Amazon reviews")
        return result
    except Exception as e:
        logger.error(f"Error getting Amazon reviews: {str(e)}")
        raise

@mcp.tool()
def yelp_search(query: list, limit: int = 100, fields: str = None,
               async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns search results from Yelp.

    Examples:
    - Search for restaurants in a city: yelp_search(query=["https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco%2C+CA"], limit=10)

    Parameters:
        query (list): Yelp search URLs with parameters (e.g., "https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco%2C+CA").
        limit (int): Maximum items to get from one query. Default: 100.
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Searching Yelp for: {query} (limit={limit})")
    try:
        result = client.yelp_search(query, limit=limit, fields=fields,
                                  async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved Yelp search results")
        return result
    except Exception as e:
        logger.error(f"Error searching Yelp: {str(e)}")
        raise

@mcp.tool()
def yelp_reviews(query: list, limit: int = 100, sort: str = 'relevance_desc', cutoff: int = None,
                fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns reviews from Yelp businesses.

    Examples:
    - Get reviews for a business: yelp_reviews(query=["https://www.yelp.com/biz/cancha-boutique-gastrobar-san-francisco"], limit=5)

    Parameters:
        query (list): Yelp business URLs or IDs (e.g., "https://www.yelp.com/biz/cancha-boutique-gastrobar-san-francisco").
        limit (int): Maximum reviews to get from one query. Default: 100.
        sort (str): Sort order (e.g., 'relevance_desc', 'date_desc', 'rating_desc'). Default: 'relevance_desc'.
        cutoff (int): Maximum timestamp for reviews (sets sort to 'date_desc').
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting Yelp reviews for: {query} (limit={limit}, sort={sort})")
    try:
        result = client.yelp_reviews(query, limit=limit, sort=sort, cutoff=cutoff,
                                   fields=fields, async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved Yelp reviews")
        return result
    except Exception as e:
        logger.error(f"Error getting Yelp reviews: {str(e)}")
        raise

@mcp.tool()
def tripadvisor_reviews(query: list, limit: int = 100, cutoff: int = None,
                        fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns reviews from Tripadvisor businesses.

    Examples:
    - Get reviews for a restaurant: tripadvisor_reviews(query=["https://www.tripadvisor.com/Restaurant_Review-g187147-d12947099-Reviews"], limit=10)

    Parameters:
        query (list): Tripadvisor page URLs (e.g., "https://www.tripadvisor.com/Restaurant_Review-g187147-d12947099-Reviews").
        limit (int): Maximum reviews to get from one query. Default: 100.
        cutoff (int): Maximum timestamp for reviews.
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting Tripadvisor reviews for: {query} (limit={limit})")
    try:
        result = client.tripadvisor_reviews(query, limit=limit, cutoff=cutoff,
                                          fields=fields, async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved Tripadvisor reviews")
        return result
    except Exception as e:
        logger.error(f"Error getting Tripadvisor reviews: {str(e)}")
        raise

@mcp.tool()
def apple_store_reviews(query: list, limit: int = 100, sort: str = 'mosthelpful', cutoff: int = None,
                        fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns reviews from AppStore apps.

    Examples:
    - Get reviews from an app URL: apple_store_reviews(query=["https://apps.apple.com/us/app/telegram-messenger/id686449807"], limit=50)
    - Get most recent reviews from an app ID: apple_store_reviews(query=["686449807"], sort="mostrecent")

    Parameters:
        query (list): AppStore app URLs or IDs (e.g., "https://apps.apple.com/us/app/telegram-messenger/id686449807").
        limit (int): Maximum reviews to extract per query. Default: 100.
        sort (str): Sort type - 'mosthelpful' or 'mostrecent'. Default: 'mosthelpful'.
        cutoff (int): Maximum timestamp for reviews (sets sort to "newest").
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting AppStore reviews for: {query} (limit={limit}, sort={sort})")
    try:
        result = client.apple_store_reviews(query, limit=limit, sort=sort, cutoff=cutoff,
                                          fields=fields, async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved AppStore reviews")
        return result
    except Exception as e:
        logger.error(f"Error getting AppStore reviews: {str(e)}")
        raise

@mcp.tool()
def youtube_comments(query: list, per_query: int = 100, language: str = 'en', region: str = None,
                     fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns comments from YouTube videos.

    Examples:
    - Get comments from a video URL: youtube_comments(query=["https://www.youtube.com/watch?v=dQw4w9WgXcQ"], per_query=20)
    - Get comments from a video ID: youtube_comments(query=["ph5pHgklaZ0"])

    Parameters:
        query (list): YouTube video links or video IDs (e.g., "https://www.youtube.com/watch?v=ph5pHgklaZ0").
        per_query (int): Maximum comments to return per query. Default: 100.
        language (str): Language code for results. Default: 'en'.
        region (str): Region code for results.
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting YouTube comments for: {query} (per_query={per_query}, language={language})")
    try:
        result = client.youtube_comments(query, per_query=per_query, language=language, region=region,
                                       fields=fields, async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved YouTube comments")
        return result
    except Exception as e:
        logger.error(f"Error getting YouTube comments: {str(e)}")
        raise

@mcp.tool()
def g2_reviews(query: list, limit: int = 100, sort: str = 'g2_default', cutoff: int = None,
               fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns reviews from G2 products.

    Examples:
    - Get reviews for a product: g2_reviews(query=["https://www.g2.com/products/outscraper"], limit=15)

    Parameters:
        query (list): G2 product URLs (e.g., "https://www.g2.com/products/outscraper").
        limit (int): Maximum reviews to get per query. Default: 100.
        sort (str): Sort type - 'g2_default', 'most_recent', 'most_helpful', etc. Default: 'g2_default'.
        cutoff (int): Oldest timestamp for reviews (sets sort to most recent).
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting G2 reviews for: {query} (limit={limit}, sort={sort})")
    try:
        result = client.g2_reviews(query, limit=limit, sort=sort, cutoff=cutoff,
                                 fields=fields, async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved G2 reviews")
        return result
    except Exception as e:
        logger.error(f"Error getting G2 reviews: {str(e)}")
        raise

@mcp.tool()
def trustpilot_reviews(query: list, limit: int = 100, languages: str = 'default', sort: str = '',
                       cutoff: int = None, fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns reviews from Trustpilot businesses.

    Examples:
    - Get reviews for a domain from Trustpilot: trustpilot_reviews(query=["outscraper.com"], limit=10)

    Parameters:
        query (list): Trustpilot page URLs or domain names (e.g., "outscraper.com").
        limit (int): Maximum reviews to get per query. Default: 100.
        languages (str): Language filter - 'default', 'all', 'en', 'es', 'de'. Default: 'default'.
        sort (str): Sort type - e.g., 'recency'. Default: ''.
        cutoff (int): Oldest timestamp for reviews (sets sort to newest first).
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting Trustpilot reviews for: {query} (limit={limit}, languages={languages})")
    try:
        result = client.trustpilot_reviews(query, limit=limit, languages=languages, sort=sort,
                                         cutoff=cutoff, fields=fields, async_request=async_request, 
                                         ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved Trustpilot reviews")
        return result
    except Exception as e:
        logger.error(f"Error getting Trustpilot reviews: {str(e)}")
        raise

@mcp.tool()
def glassdoor_reviews(query: list, limit: int = 100, sort: str = 'DATE', 
                        cutoff: int = None, fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns reviews from Glassdoor companies.

    Examples:
    - Get company reviews: glassdoor_reviews(query=["https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036.htm"], limit=25)

    Parameters:
        query (list): Glassdoor company URLs (e.g., "https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036.htm").
        limit (int): Maximum reviews to get per query. Default: 100.
        sort (str): Sort type - 'DATE' or 'RELEVANCE'. Default: 'DATE'.
        cutoff (int): Oldest timestamp for reviews (sets sort to newest first).
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting Glassdoor reviews for: {query} (limit={limit}, sort={sort})")
    try:
        result = client.glassdoor_reviews(query, limit=limit, sort=sort, cutoff=cutoff,
                                        fields=fields, async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved Glassdoor reviews")
        return result
    except Exception as e:
        logger.error(f"Error getting Glassdoor reviews: {str(e)}")
        raise

@mcp.tool()
def capterra_reviews(query: list, limit: int = 100, sort: str = 'MOST_HELPFUL', cutoff: int = None,
                     language: str = 'en', region: str = None,
                     fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns reviews from Capterra.

    Examples:
    - Get reviews for a software product: capterra_reviews(query=["https://www.capterra.com/p/228041/Google-Maps-scraper/"], limit=20)

    Parameters:
        query (list): Capterra product page URLs (e.g., "https://www.capterra.com/p/228041/Google-Maps-scraper/").
        limit (int): Maximum reviews to get per query. Default: 100.
        sort (str): Sort type - 'MOST_HELPFUL', 'MOST_RECENT', 'HIGHEST_RATING', 'LOWEST_RATING'. Default: 'MOST_HELPFUL'.
        cutoff (int): Oldest timestamp for reviews (sets sort to newest first).
        language (str): Language code for results. Default: 'en'.
        region (str): Region code for results.
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting Capterra reviews for: {query} (limit={limit}, sort={sort})")
    try:
        result = client.capterra_reviews(query, limit=limit, sort=sort, cutoff=cutoff,
                                       language=language, region=region, fields=fields,
                                       async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved Capterra reviews")
        return result
    except Exception as e:
        logger.error(f"Error getting Capterra reviews: {str(e)}")
        raise

@mcp.tool()
def geocoding(query: list, fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Translates human-readable addresses into map locations (latitude, longitude).

    Examples:
    - Geocode an address: geocoding(query=["321 California Ave, Palo Alto, CA 94306"])

    Parameters:
        query (list): Addresses to geocode (e.g., "321 California Ave, Palo Alto, CA 94306").
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Geocoding addresses: {query}")
    try:
        result = client.geocoding(query, fields=fields, async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully geocoded addresses")
        return result
    except Exception as e:
        logger.error(f"Error geocoding addresses: {str(e)}")
        raise

@mcp.tool()
def reverse_geocoding(query: list, fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Translates map locations (latitude, longitude) into human-readable addresses.

    Examples:
    - Reverse geocode coordinates: reverse_geocoding(query=["40.7624284 -73.973794"])

    Parameters:
        query (list): Coordinates to reverse geocode (e.g., "40.7624284 -73.973794").
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Reverse geocoding coordinates: {query}")
    try:
        result = client.reverse_geocoding(query, fields=fields, async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully reverse geocoded coordinates")
        return result
    except Exception as e:
        logger.error(f"Error reverse geocoding coordinates: {str(e)}")
        raise

@mcp.tool()
def whitepages_phones(query: list, fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns insights about phone number owners (name, address, etc.) from Whitepages.

    Examples:
    - Look up a phone number: whitepages_phones(query=["+12812368208"])

    Parameters:
        query (list): Phone numbers to look up (e.g., "+1 281 236 8208").
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting Whitepages phone info for: {query}")
    try:
        result = client.whitepages_phones(query, fields=fields, async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved Whitepages phone information")
        return result
    except Exception as e:
        logger.error(f"Error getting Whitepages phone information: {str(e)}")
        raise

@mcp.tool()
def whitepages_addresses(query: list, fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns insights about addresses and their residents from Whitepages.

    Examples:
    - Look up an address: whitepages_addresses(query=["321 California Ave, Palo Alto, CA 94306"])

    Parameters:
        query (list): Addresses to look up (e.g., "321 California Ave, Palo Alto, CA 94306").
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting Whitepages address info for: {query}")
    try:
        result = client.whitepages_addresses(query, fields=fields, async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved Whitepages address information")
        return result
    except Exception as e:
        logger.error(f"Error getting Whitepages address information: {str(e)}")
        raise

@mcp.tool()
def company_insights(query: list, fields: str = None, async_request: bool = False, enrichment: list = None):
    """Finds company details such as revenue, size, founding year, public status, etc.

    Examples:
    - Get insights for a company: company_insights(query=["outscraper.com"])
    - Get insights with social media enrichment: company_insights(query=["dominopark.com"], enrichment=["social_media"])

    Parameters:
        query (list): Domains or websites (e.g., "dominopark.com").
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        enrichment (list): Additional data enrichments to apply to results.
    """
    logger.info(f"Getting company insights for: {query}")
    try:
        result = client.company_insights(query, fields=fields, async_request=async_request, enrichment=enrichment)
        logger.info(f"Successfully retrieved company insights")
        return result
    except Exception as e:
        logger.error(f"Error getting company insights: {str(e)}")
        raise

@mcp.tool()
def validate_emails(query: list, async_request: bool = False):
    """Validates email addresses and checks if they are deliverable.

    Examples:
    - Validate a single email: validate_emails(query=["support@outscraper.com"])
    - Validate multiple emails: validate_emails(query=["test@example.com", "invalid-email"])

    Parameters:
        query (list): Email addresses to validate (e.g., "support@outscraper.com").
        async_request (bool): If True, returns request ID for later retrieval.
    """
    logger.info(f"Validating emails: {query}")
    try:
        result = client.validate_emails(query, async_request=async_request)
        logger.info(f"Successfully validated emails")
        return result
    except Exception as e:
        logger.error(f"Error validating emails: {str(e)}")
        raise

@mcp.tool()
def trustpilot_search(query: list, limit: int = 100, skip: int = 0, enrichment: list = None,
                      fields: str = None, async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns search results from Trustpilot.

    Examples:
    - Search for businesses on Trustpilot: trustpilot_search(query=["real estate"], limit=10)

    Parameters:
        query (list): Companies or categories to search on Trustpilot (e.g., "real estate").
        limit (int): Maximum items to get per query. Default: 100.
        skip (int): Number of items to skip (for pagination). Default: 0.
        enrichment (list): Additional data enrichments to apply to results.
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Searching Trustpilot for: {query} (limit={limit}, skip={skip})")
    try:
        result = client.trustpilot_search(query, limit=limit, skip=skip, enrichment=enrichment,
                                        fields=fields, async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved Trustpilot search results")
        return result
    except Exception as e:
        logger.error(f"Error searching Trustpilot: {str(e)}")
        raise

@mcp.tool()
def trustpilot(query: list, enrichment: list = None, fields: str = None,
               async_request: bool = False, ui: bool = None, webhook: str = None):
    """Returns data from Trustpilot businesses.

    Examples:
    - Get Trustpilot data for a domain: trustpilot(query=["outscraper.com"])

    Parameters:
        query (list): Trustpilot page URLs or domain names (e.g., "outscraper.com").
        enrichment (list): Additional data enrichments to apply to results.
        fields (str): Fields to include in response.
        async_request (bool): If True, returns request ID for later retrieval.
        ui (bool): If True, executes as UI task (sets async_request=True).
        webhook (str): URL for POST notification when task completes.
    """
    logger.info(f"Getting Trustpilot business data for: {query}")
    try:
        result = client.trustpilot(query, enrichment=enrichment, fields=fields,
                                 async_request=async_request, ui=ui, webhook=webhook)
        logger.info(f"Successfully retrieved Trustpilot business data")
        return result
    except Exception as e:
        logger.error(f"Error getting Trustpilot business data: {str(e)}")
        raise

def run():
    logger.info("Starting Outscraper MCP Server...")
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise
