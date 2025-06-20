import unittest
from unittest.mock import patch


class TestOutscraperMCPServer(unittest.TestCase):
    """Test cases for Outscraper MCP Server functionality."""

    @patch('outscraper_mcp_server.server.client')
    def test_maps_search(self, mock_client):
        """Test the google_maps_search function."""

        mock_response = [{'name': 'Test Place', 'address': '123 Test St'}]
        mock_client.google_maps_search.return_value = mock_response

        from outscraper_mcp_server.server import google_maps_search

        result = google_maps_search(
            query='test place',
            limit=5,
            language='en',
            region='US'
        )

        mock_client.google_maps_search.assert_called_once_with(
            ['test place'],
            limit=5,
            drop_duplicates=False,
            language='en',
            region='US',
            skip=0,
            coordinates=None,
            enrichment=None,
            fields=None,
            async_request=False,
            ui=None,
            webhook=None
        )

        self.assertEqual(result, mock_response)

    @patch('outscraper_mcp_server.server.client')
    def test_maps_reviews(self, mock_client):
        """Test the google_maps_reviews function."""

        mock_response = [{'reviews': [{'text': 'Great place!', 'rating': 5}]}]
        mock_client.google_maps_reviews.return_value = mock_response

        from outscraper_mcp_server.server import google_maps_reviews

        result = google_maps_reviews(
            query='ChIJIQBpAG2ahYAR_6128GcTUEo',
            reviews_limit=10,
            sort='newest'
        )

        mock_client.google_maps_reviews.assert_called_once_with(
            'ChIJIQBpAG2ahYAR_6128GcTUEo',
            reviews_limit=10,
            limit=1,
            sort='newest',
            start=None,
            cutoff=None,
            cutoff_rating=None,
            ignore_empty=False,
            language='en',
            region=None,
            reviews_query=None,
            source=None,
            last_pagination_id=None,
            fields=None,
            async_request=False,
            ui=None,
            webhook=None
        )

        self.assertEqual(result, mock_response)

    @patch('outscraper_mcp_server.server.client')
    def test_error_handling(self, mock_client):
        """Test error handling in server functions."""
        mock_client.google_maps_search.side_effect = Exception('API Error')

        from outscraper_mcp_server.server import google_maps_search

        with self.assertRaises(Exception) as context:
            google_maps_search(query='test place')
        self.assertEqual(str(context.exception), 'API Error')

    @patch('outscraper_mcp_server.server.client')
    def test_emails_and_contacts(self, mock_client):
        """Test the emails_and_contacts function."""
        mock_response = [{'domain': 'example.com', 'emails': ['test@example.com']}]
        mock_client.emails_and_contacts.return_value = mock_response

        from outscraper_mcp_server.server import emails_and_contacts

        result = emails_and_contacts(domains=['example.com'])

        mock_client.emails_and_contacts.assert_called_once_with(
            ["example.com"],
            fields=None
        )

        self.assertEqual(result, mock_response)

    @patch('outscraper_mcp_server.server.client')
    def test_validate_emails(self, mock_client):
        """Test the validate_emails function."""
        mock_response = [{'email': 'test@example.com', 'valid': True}]
        mock_client.validate_emails.return_value = mock_response

        from outscraper_mcp_server.server import validate_emails

        result = validate_emails(query=['test@example.com'])

        mock_client.validate_emails.assert_called_once_with(
            ['test@example.com'],
            async_request=False
        )

        self.assertEqual(result, mock_response)

if __name__ == '__main__':
    unittest.main()
