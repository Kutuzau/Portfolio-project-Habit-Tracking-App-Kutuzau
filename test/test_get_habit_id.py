import pytest
from statistics_and_additions import get_habit_id
from my_exceptions import WrongHabitId


@pytest.mark.parametrize("habit, expected_result", [('tennis', 0),
                                                    ('reading', 1),
                                                    ('football', 2),
                                                    ('swimming', 3),
                                                    ('jogging', 4)])
def test_get_habit_id(habit, expected_result):
    assert get_habit_id(habit) == expected_result


@pytest.mark.parametrize("habit, expected_exception", [('not_existing_habit', WrongHabitId),
                                                       ('', WrongHabitId),
                                                       (0, WrongHabitId),
                                                       (-1, WrongHabitId),
                                                       (1.0, WrongHabitId)])
def test_get_habit_id_with_exception(habit, expected_exception):
    with pytest.raises(expected_exception):
        get_habit_id(habit)
