from unittest.mock import MagicMock, patch, mock_open
from load import load

@patch("load.psycopg.connect")
def test_load_success(mock_connect):
    """Verify transformed data is loaded into database"""

    mock_file = mock_open(read_data="""{
        "city": "Stockholm",
        "temperature": 21.87,
        "humidity": 47,
        "description": "broken clouds",
        "observed_at": "2026-08-27T13:23:17+00:00"
    }""")

    mock_conn = MagicMock()
    mock_cur = MagicMock()

    mock_connect.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    with patch("builtins.open", mock_file):
        load()

    mock_connect.assert_called_once()
    mock_cur.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

    sql, values = mock_cur.execute.call_args.args
    assert values == (
        "Stockholm",
        21.87,
        47,
        "broken clouds",
        "2026-08-27T13:23:17+00:00"
    )