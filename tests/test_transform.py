import json
from datetime import datetime, timezone
from unittest.mock import mock_open, patch
from transform import transform

def test_transform_success():
    """Verify raw OpenWeather JSON is successfully mapped to the target schema format."""
    fake_dt = 1787749562
    fake_data = {
        "name": "Stockholm",
        "main": {
            "temp": 23.00,
            "humidity": 40
        },
        "weather": [
            {"description": "sunny"}
        ],
        "dt": fake_dt
    }

    json_string = json.dumps(fake_data)
    mock_file = mock_open(read_data=json_string)
    with patch("builtins.open", mock_file):
        transform()

    written_pieces = [call.args[0] for call in mock_file().write.call_args_list]
    written_data = "".join(written_pieces)
    result = json.loads(written_data)

    assert result["city"] == "Stockholm"
    assert result["temperature"] == 23.00
    assert result["humidity"] == 40
    assert result["description"] == "sunny"
    assert result["observed_at"] == datetime.fromtimestamp(fake_dt, tz=timezone.utc).isoformat()