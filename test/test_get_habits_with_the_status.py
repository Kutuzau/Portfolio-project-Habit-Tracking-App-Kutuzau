import pytest
from statistics_and_additions import get_habits_with_the_status
from my_exceptions import WrongHabitStatus


@pytest.mark.parametrize("status, expected_result", [('1', ['tennis', 'reading', 'swimming', 'jogging']),
                                                     ('0', ['football'])])
def test_get_habits_with_the_status(status, expected_result):
    assert get_habits_with_the_status(status) == expected_result


@pytest.mark.parametrize("status, expected_exception", [(1, WrongHabitStatus),
                                                        (0, WrongHabitStatus),
                                                        (True, WrongHabitStatus),
                                                        (False, WrongHabitStatus),
                                                        ('another text', WrongHabitStatus)])
def test_get_habits_with_the_status_with_exception(status, expected_exception):
    with pytest.raises(expected_exception):
        get_habits_with_the_status(status)
