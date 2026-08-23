"""
Unit Tests — NVIDIA AI Client Mock Verification
Validates request formatting, error handling, and parameter serialization without network dependencies.
"""

import unittest
from unittest.mock import patch, MagicMock
from nvidia_ai.client import NvidiaAIClient


class TestNvidiaAIClient(unittest.TestCase):
    def setUp(self):
        self.client = NvidiaAIClient(api_key="nvapi-mock-test-key-12345")

    @patch("urllib.request.urlopen")
    def test_list_models_mocked(self, mock_urlopen):
        """Verifies that model listing parses returned JSON array correctly."""
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"data": [{"id": "meta/llama-3.1-70b-instruct"}, {"id": "mistralai/mistral-large-2-instruct"}]}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        models = self.client.list_models()
        self.assertEqual(len(models), 2)
        self.assertIn("meta/llama-3.1-70b-instruct", models)

    @patch("urllib.request.urlopen")
    def test_chat_mocked(self, mock_urlopen):
        """Verifies that chat completion response extraction works accurately."""
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"choices": [{"message": {"content": "Zero-trust AI gateway prevents unauthorized tool execution."}}]}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        resp = self.client.chat(
            prompt="Explain zero-trust AI.",
            model="meta/llama-3.1-70b-instruct"
        )
        self.assertEqual(resp, "Zero-trust AI gateway prevents unauthorized tool execution.")

    def test_missing_api_key_raises_error(self):
        """Verifies that initializing with no API key and no env var raises ValueError."""
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError):
                NvidiaAIClient(api_key=None)


if __name__ == "__main__":
    unittest.main()
