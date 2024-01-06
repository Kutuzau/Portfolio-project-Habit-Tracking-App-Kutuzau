import pytest
from statistics_and_additions import raise_wrong_habit_name
from my_exceptions import WrongHabitName


@pytest.mark.parametrize("habit, expected_result", [('tennis', None),
                                                    ('reading', None),
                                                    ('football', None),
                                                    ('swimming', None),
                                                    ('jogging', None)])
def test_raise_wrong_habit_name(habit, expected_result):
    assert raise_wrong_habit_name(habit) == expected_result


@pytest.mark.parametrize("habit, expected_exception", [('not_existing_habit', WrongHabitName),
                                                       ('', WrongHabitName),
                                                       (0, WrongHabitName),
                                                       (-1, WrongHabitName),
                                                       (1.0, WrongHabitName)])
def test_raise_wrong_habit_name_with_exception(habit, expected_exception):
    with pytest.raises(expected_exception):
        raise_wrong_habit_name(habit)
