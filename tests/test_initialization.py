import os
import unittest
import logging
import sys
from io import StringIO
from unittest.mock import patch, MagicMock


class TestOutscraperMCPInitialization(unittest.TestCase):
    """Test cases for Outscraper MCP Server initialization."""

    def test_initialization_with_api_key(self):
        """Test server initialization with API key set."""
        for module in list(sys.modules.keys()):
            if module.startswith('outscraper_mcp_server'):
                del sys.modules[module]

        with patch.dict(os.environ, {'OUTSCRAPER_API_KEY': 'test_api_key'}):
            with patch('outscraper.ApiClient', autospec=True) as mock_api_client_class:
                mock_client_instance = MagicMock()
                mock_api_client_class.return_value = mock_client_instance

                with patch('mcp.server.fastmcp.FastMCP') as mock_fastmcp:
                    mock_mcp_instance = MagicMock()
                    mock_fastmcp.return_value = mock_mcp_instance

                    from outscraper_mcp_server.server import OUTSCRAPER_API_KEY

                    mock_api_client_class.assert_called_once()
                    _, kwargs = mock_api_client_class.call_args
                    self.assertEqual(kwargs.get('api_key'), 'test_api_key')

                    mock_fastmcp.assert_called_once_with("Outscraper MCP Server")
                    mock_fastmcp.assert_called_once_with("Outscraper MCP Server")

                    self.assertEqual(OUTSCRAPER_API_KEY, 'test_api_key')

    def test_initialization_without_api_key(self):
        """Test server initialization without API key set."""
        for module in list(sys.modules.keys()):
            if module.startswith('outscraper_mcp_server'):
                del sys.modules[module]

        log_capture = StringIO()
        handler = logging.StreamHandler(log_capture)
        logger = logging.getLogger('outscraper-mcp-server')
        logger.addHandler(handler)

        original_env = os.environ.copy()

        try:
            os.environ.clear()
            if 'OUTSCRAPER_API_KEY' in os.environ:
                del os.environ['OUTSCRAPER_API_KEY']

            with patch('dotenv.load_dotenv', return_value=False):
                with patch('outscraper.ApiClient', autospec=True) as mock_api_client_class:
                    mock_client_instance = MagicMock()
                    mock_api_client_class.return_value = mock_client_instance

                    with patch('mcp.server.fastmcp.FastMCP') as mock_fastmcp:
                        mock_mcp_instance = MagicMock()
                        mock_fastmcp.return_value = mock_mcp_instance

                        from outscraper_mcp_server.server import OUTSCRAPER_API_KEY

                        mock_api_client_class.assert_called_once()
                        _, kwargs = mock_api_client_class.call_args
                        self.assertIsNone(kwargs.get('api_key'))

                        mock_fastmcp.assert_called_once_with("Outscraper MCP Server")

                        self.assertIsNone(OUTSCRAPER_API_KEY)

                        self.assertIn('OUTSCRAPER_API_KEY environment variable not set', log_capture.getvalue())
        finally:
            os.environ.clear()
            os.environ.update(original_env)
            logger.removeHandler(handler)

    def test_run_function(self):
        """Test the run function."""
        if 'outscraper_mcp_server.server' in sys.modules:
            del sys.modules['outscraper_mcp_server.server']

        with patch('mcp.server.fastmcp.FastMCP') as mock_fastmcp:
            mock_mcp_instance = MagicMock()
            mock_fastmcp.return_value = mock_mcp_instance

            from outscraper_mcp_server.server import run

            run()

            mock_mcp_instance.run.assert_called_once()

    def test_main_function(self):
        """Test the main function."""
        for module in list(sys.modules.keys()):
            if module.startswith('outscraper_mcp_server'):
                del sys.modules[module]

        mock_run = MagicMock()

        with patch.dict('sys.modules', {'outscraper_mcp_server.server': MagicMock()}):
            sys.modules['outscraper_mcp_server.server'].run = mock_run

            from outscraper_mcp_server import main

            main()

            mock_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
