from unittest.mock import MagicMock, patch
from verify import verify

@patch("verify.psycopg.connect")
def test_verify_success(mock_connect):
    """Verify data successfully passes verification"""

    mock_conn = MagicMock()
    mock_cur = MagicMock()

    mock_connect.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    mock_cur.fetchone.side_effect = [
        (1,),
        ("Stockholm", 20.59, 59, "broken clouds", "2026-08-27T16:27:44+00:00")
    ]

    verify()

    mock_connect.assert_called_once()
    assert mock_cur.execute.call_count == 2
    assert mock_cur.fetchone.call_count == 2