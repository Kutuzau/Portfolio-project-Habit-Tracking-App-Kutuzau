import pytest
from datetime import date
from statistics_and_additions import get_previous_habit_time
from my_exceptions import WrongHabitId


@pytest.mark.parametrize("habit, expected_result", [('tennis', date(2023, 12, 28)),
                                                    ('reading', date(2023, 12, 31)),
                                                    ('football', date(2024, 1, 1)),
                                                    ('swimming', date(2023, 12, 25)),
                                                    ('jogging', date(2024, 1, 1))])
def test_get_previous_habit_time(habit, expected_result):
    assert get_previous_habit_time(habit) == expected_result


@pytest.mark.parametrize("habit, expected_exception", [('not_existing_habit', WrongHabitId),
                                                       ('', WrongHabitId),
                                                       (0, WrongHabitId),
                                                       (-1, WrongHabitId),
                                                       (1.0, WrongHabitId)])
def test_get_previous_habit_time_with_exception(habit, expected_exception):
    with pytest.raises(expected_exception):
        get_previous_habit_time(habit)