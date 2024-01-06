import pytest
from statistics_and_additions import get_max_habit_stripe
from my_exceptions import WrongHabitId


@pytest.mark.parametrize("habit, expected_result", [('tennis', 4),
                                                    ('reading', 3),
                                                    ('football', 14),
                                                    ('swimming', 6),
                                                    ('jogging', 4)])
def test_get_max_habit_stripe(habit, expected_result):
    assert get_max_habit_stripe(habit) == expected_result


@pytest.mark.parametrize("habit, expected_exception", [('not_existing_habit', WrongHabitId),
                                                       ('', WrongHabitId),
                                                       (0, WrongHabitId),
                                                       (-1, WrongHabitId),
                                                       (1.0, WrongHabitId)])
def test_get_max_habit_stripe_with_exception(habit, expected_exception):
    with pytest.raises(expected_exception):
        get_max_habit_stripe(habit)
