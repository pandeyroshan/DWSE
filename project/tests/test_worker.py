import datetime
import sys
import os
from unittest.mock import patch, MagicMock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from worker import create_task

@patch("worker.update_weather_task")
def test_create_task(mock_update_weather_task):
    data = {
        "task_id": "test_task_id",
        "task_type": 2,
    }
    with patch("random.randint", return_value=2):
        with patch("random.uniform", return_value=42.0):
            with patch("datetime.datetime") as mock_datetime:
                mock_datetime.now.return_value = datetime.datetime(2023, 7, 30, 12, 34, 56)
                result = create_task(data)
                assert result is True
                mock_update_weather_task.assert_called_once_with("test_task_id", {
                    "task_id": "test_task_id",
                    "task_type": 2,
                    "status": "SUCCESS",
                    "result": 42.0,
                    "completed_at": datetime.datetime(2023, 7, 30, 12, 34, 56),
                })
