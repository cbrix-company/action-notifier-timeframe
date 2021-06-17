from datetime import datetime

import pytz

from main import calculate_timeframes


class TestCalculateTimeframes:

    # --------------
    # 1 minute range
    # --------------

    def test_every_minute_left_range(self, mocker):
        mock_dt = datetime(2021, 6, 10, 15, 0, tzinfo=pytz.utc)
        mocker.patch('main.current_utc_time', return_value=mock_dt)
        left, right = calculate_timeframes(1, 'minutes')
        assert left == datetime(2021, 6, 10, 15, 0, tzinfo=pytz.utc)
        assert right == datetime(2021, 6, 10, 15, 1, tzinfo=pytz.utc)

    def test_every_minute_right_range(self, mocker):
        mock_dt = datetime(2021, 6, 10, 15, 59, tzinfo=pytz.utc)
        mocker.patch('main.current_utc_time', return_value=mock_dt)
        left, right = calculate_timeframes(1, 'minutes')
        assert left == datetime(2021, 6, 10, 15, 59, tzinfo=pytz.utc)
        assert right == datetime(2021, 6, 10, 16, 0, tzinfo=pytz.utc)

    # --------------
    # 5 minute range
    # --------------

    expected_5_minutes_left = datetime(2021, 6, 10, 15, 0, tzinfo=pytz.utc)
    expected_5_minutes_right = datetime(2021, 6, 10, 15, 5, tzinfo=pytz.utc)

    def test_every_5_minutes_left_range(self, mocker):
        mock_dt = datetime(2021, 6, 10, 15, 0, tzinfo=pytz.utc)
        mocker.patch('main.current_utc_time', return_value=mock_dt)
        left, right = calculate_timeframes(5, 'minutes')
        assert left == self.expected_5_minutes_left
        assert right == self.expected_5_minutes_right

    def test_every_5_minutes_middle_range(self, mocker):
        mock_dt = datetime(2021, 6, 10, 15, 2, tzinfo=pytz.utc)
        mocker.patch('main.current_utc_time', return_value=mock_dt)
        left, right = calculate_timeframes(5, 'minutes')
        assert left == self.expected_5_minutes_left
        assert right == self.expected_5_minutes_right

    def test_every_5_minutes_right_range(self, mocker):
        mock_dt = datetime(2021, 6, 10, 15, 4, tzinfo=pytz.utc)
        mocker.patch('main.current_utc_time', return_value=mock_dt)
        left, right = calculate_timeframes(5, 'minutes')
        assert left == self.expected_5_minutes_left
        assert right == self.expected_5_minutes_right

    # ---------------
    # 30 minute range
    # ---------------

    expected_30_minutes_left = datetime(2021, 6, 10, 15, 30, tzinfo=pytz.utc)
    expected_30_minutes_right = datetime(2021, 6, 10, 16, 0, tzinfo=pytz.utc)

    def test_every_30_minutes_left_range(self, mocker):
        mock_dt = datetime(2021, 6, 10, 15, 30, tzinfo=pytz.utc)
        mocker.patch('main.current_utc_time', return_value=mock_dt)
        left, right = calculate_timeframes(30, 'minutes')
        assert left == self.expected_30_minutes_left
        assert right == self.expected_30_minutes_right

    def test_every_30_minutes_middle_range(self, mocker):
        mock_dt = datetime(2021, 6, 10, 15, 45, tzinfo=pytz.utc)
        mocker.patch('main.current_utc_time', return_value=mock_dt)
        left, right = calculate_timeframes(30, 'minutes')
        assert left == self.expected_30_minutes_left
        assert right == self.expected_30_minutes_right

    def test_every_30_minutes_right_range(self, mocker):
        mock_dt = datetime(2021, 6, 10, 15, 59, tzinfo=pytz.utc)
        mocker.patch('main.current_utc_time', return_value=mock_dt)
        left, right = calculate_timeframes(30, 'minutes')
        assert left == self.expected_30_minutes_left
        assert right == self.expected_30_minutes_right

    def test_every_60_minutes(self, mocker):
        expected_60_minutes_left = datetime(2021, 6, 10, 15, 0, tzinfo=pytz.utc)
        expected_60_minutes_right = datetime(2021, 6, 10, 16, 0, tzinfo=pytz.utc)

        # left range
        mock_dt = datetime(2021, 6, 10, 15, 0, tzinfo=pytz.utc)
        mocker.patch('main.current_utc_time', return_value=mock_dt)
        left, right = calculate_timeframes(60, 'minutes')
        assert left == expected_60_minutes_left
        assert right == expected_60_minutes_right

        # middle range
        mock_dt = datetime(2021, 6, 10, 15, 30, tzinfo=pytz.utc)
        mocker.patch('main.current_utc_time', return_value=mock_dt)
        left, right = calculate_timeframes(60, 'minutes')
        assert left == expected_60_minutes_left
        assert right == expected_60_minutes_right

        # right range
        mock_dt = datetime(2021, 6, 10, 15, 59, tzinfo=pytz.utc)
        mocker.patch('main.current_utc_time', return_value=mock_dt)
        left, right = calculate_timeframes(60, 'minutes')
        assert left == expected_60_minutes_left
        assert right == expected_60_minutes_right
