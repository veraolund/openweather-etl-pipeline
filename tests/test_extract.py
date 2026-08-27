import json
from unittest.mock import MagicMock, patch, mock_open
from extract import extract

@patch("extract.requests.get")
def test_extract_success(mock_get):
    """Verify API data is successfully written to a JSON file"""
    fake_response = MagicMock()
    fake_response.json.return_value = {"name": "Stockholm"}
    mock_get.return_value = fake_response

    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        extract()

    written_pieces = [call.args[0] for call in mock_file().write.call_args_list]
    written_data = "".join(written_pieces)
    result = json.loads(written_data)

    mock_get.assert_called_once()
    fake_response.raise_for_status.assert_called_once()
    assert result["name"] == "Stockholm"