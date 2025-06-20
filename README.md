# Outscraper MCP Server

[![smithery](https://img.shields.io/badge/smithery-enabled-brightgreen)](https://github.com/smithery-io/smithery)
[![PyPI version](https://img.shields.io/pypi/v/outscraper-mcp-server.svg)](https://pypi.org/project/outscraper-mcp-server/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A comprehensive Model Context Protocol (MCP) server that provides AI assistants with access to Outscraper's data extraction services. This server implements 25+ tools for extracting business intelligence, location data, reviews, and contact information from Google Maps, Amazon, Yelp, Trustpilot, and many other online platforms with high reliability and performance.

## 🚀 Features

### Google Maps Data Extraction
- 🗺️ **Google Maps Search** - Search for businesses and places with detailed information
- ⭐ **Google Maps Reviews** - Extract customer reviews from any Google Maps place
- 📸 **Google Maps Photos** - Get photos from Google Maps places
- 🧭 **Google Maps Directions** - Get directions between locations on Google Maps

### Search & Reviews
- 🔍 **Google Search** - Search Google and retrieve organic listings, ads, and related data
- 📰 **Google Search News** - Search Google News for articles and metadata
- 📱 **Google Play Reviews** - Get reviews for apps from Google Play Store
- 🛒 **Amazon Products** - Get information about products on Amazon
- 📝 **Amazon Reviews** - Extract reviews from Amazon products
- 🏨 **Tripadvisor Reviews** - Get reviews from Tripadvisor businesses
- 📲 **Apple Store Reviews** - Extract reviews from AppStore apps
- 📺 **YouTube Comments** - Get comments from YouTube videos
- 💼 **G2 Reviews** - Extract reviews from G2 products
- ✅ **Trustpilot Data & Reviews** - Get business data and reviews from Trustpilot
- 👔 **Glassdoor Reviews** - Extract company reviews from Glassdoor
- 💻 **Capterra Reviews** - Get software product reviews from Capterra

### Business & Contact Intelligence
- 📧 **Emails & Contacts** - Extract emails and contact information from websites
- 📞 **Phones Enricher** - Get carrier data and validate phone numbers
- 🏢 **Company Insights** - Find company details like revenue, size, founding year, etc.
- 📨 **Email Validation** - Validate email addresses and check deliverability
- 📑 **Whitepages Data** - Get insights about addresses and phone number owners

### Geolocation Services
- 📍 **Geocoding** - Convert addresses to coordinates (latitude, longitude)
- 🗺️ **Reverse Geocoding** - Convert coordinates to human-readable addresses

### Advanced Capabilities
- **Data Enrichment** - Enhance results with additional contact information via enrichment parameter
- **Multi-language Support** - Search and extract data in different languages
- **Regional Filtering** - Target specific countries/regions for localized results
- **Flexible Sorting** - Sort reviews by relevance, date, rating, etc.
- **Time-based Filtering** - Filter reviews by date using cutoff parameter
- **High Volume Support** - Handles async processing for large requests automatically
- **Pagination Support** - Skip and limit parameters for handling large result sets

## Installation

### Installing via Smithery (Recommended)
To install the Outscraper MCP server for Claude Desktop automatically via Smithery:

```bash
npx -y @smithery/cli install outscraper-mcp-server --client claude
```

### Installing via PyPI
```bash
# Using pip
pip install outscraper-mcp-server

# Using uv (recommended)
uv add outscraper-mcp-server

# Using uvx for one-time execution
uvx outscraper-mcp-server
```

### Manual Installation
```bash
git clone https://github.com/outscraper/outscraper-mcp
cd outscraper-mcp-server

# Using uv (recommended)
uv sync

# Using pip
pip install -e .
```

## Configuration

### Get Your API Key
1. Sign up at [Outscraper](https://outscraper.com)
2. Get your API key from the profile page

### Set Environment Variable
```bash
export OUTSCRAPER_API_KEY="your_api_key_here"
```
Or create a `.env` file:
```
OUTSCRAPER_API_KEY=your_api_key_here
```
[Link to the profile page to create the API key](https://auth.outscraper.com/profile)

## Client Configuration

### Claude Desktop
Add to your `claude_desktop_config.json`:

**Via Smithery (Automatic):**
```json
{
  "mcpServers": {
    "outscraper": {
      "command": "npx",
      "args": ["-y", "@smithery/cli", "run", "outscraper-mcp-server"],
      "env": {
        "OUTSCRAPER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Via Local Installation:**
```json
{
  "mcpServers": {
    "outscraper": {
      "command": "uvx",
      "args": ["outscraper-mcp-server"],
      "env": {
        "OUTSCRAPER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Via Manual Installation:**
```json
{
  "mcpServers": {
    "outscraper": {
      "command": "uv",
      "args": ["run", "python", "-m", "outscraper_mcp_server"],
      "env": {
        "OUTSCRAPER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Cursor AI
**Automatic Installation with UVX (Recommended):**
```json
{
  "mcpServers": {
    "outscraper": {
      "command": "uvx",
      "args": ["outscraper-mcp-server"],
      "env": {
        "OUTSCRAPER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Manual Installation:**
```json
{
  "mcpServers": {
    "outscraper": {
      "command": "outscraper-mcp-server",
      "env": {
        "OUTSCRAPER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🔄 Integration with MCP Clients
This server is compatible with any MCP client, including:

- Claude Desktop
- Cursor AI
- Windsurf IDE
- Raycast
- VS Code with MCP extensions
- Custom MCP clients

## 📊 Rate Limits & Pricing
- Check [Outscraper Pricing](https://outscraper.com/pricing/) for current rates
- API key usage is tracked per request
- Consider implementing caching for frequently accessed data

## 📄 License
Experimental Software License - see LICENSE file for details.

Notice: This software is experimental and free to use for all purposes. Created by [nikolaout](https://github.com/nikolaout).

## 🔗 Links
- [Outscraper API Documentation](https://app.outscraper.com/api-docs)
- [FastMCP Documentation](https://gofastmcp.com/getting-started/welcome)
- [Model Context Protocol](https://modelcontextprotocol.io/)
