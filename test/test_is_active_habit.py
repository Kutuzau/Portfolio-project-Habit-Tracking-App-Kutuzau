import pytest
from statistics_and_additions import is_active_habit
from my_exceptions import WrongHabitName


@pytest.mark.parametrize("habit, expected_result", [('tennis', True),
                                                    ('reading', True),
                                                    ('football', False),
                                                    ('swimming', True),
                                                    ('jogging', True)])
def test_is_active_habit_status(habit, expected_result):
    assert is_active_habit(habit) == expected_result


@pytest.mark.parametrize("habit, expected_exception", [('not_existing_habit', WrongHabitName),
                                                       ('', WrongHabitName),
                                                       (True, WrongHabitName),
                                                       (False, WrongHabitName),
                                                       (1, WrongHabitName),
                                                       (0, WrongHabitName)])
def test_is_active_habit_with_exception(habit, expected_exception):
    with pytest.raises(expected_exception):
        is_active_habit(habit)
