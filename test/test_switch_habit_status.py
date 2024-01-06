import pytest
from statistics_and_additions import switch_habit_status
from my_exceptions import WrongHabitStatus, WrongHabitName


@pytest.mark.parametrize("habit, flag, expected_result", [('tennis', '0', 0),
                                                          ('tennis', '1', 1),
                                                          ('reading', '0', 0),
                                                          ('reading', '1', 1),
                                                          ('football', '0', 0),
                                                          ('football', '1', 1),
                                                          ('swimming', '0', 0),
                                                          ('swimming', '1', 1),
                                                          ('jogging', '0', 0),
                                                          ('jogging', '1', 1)])
def test_switch_habit_status(habit, flag, expected_result):
    assert switch_habit_status(habit, flag) == expected_result


@pytest.mark.parametrize("habit, flag, expected_exception", [('not_existing_habit', '1', WrongHabitName),
                                                             ('not_existing_habit', '0', WrongHabitName),
                                                             ('', '1', WrongHabitName),
                                                             ('', '0', WrongHabitName),
                                                             ('tennis', '2', WrongHabitStatus),
                                                             ('tennis', 1, WrongHabitStatus),
                                                             ('tennis', 0, WrongHabitStatus),
                                                             ('reading', '00', WrongHabitStatus),
                                                             ('football', '111', WrongHabitStatus),
                                                             ('swimming', '', WrongHabitStatus),
                                                             ('jogging', True, WrongHabitStatus),
                                                             ('jogging', False, WrongHabitStatus)])
def test_switch_habit_status_with_exception(habit, flag, expected_exception):
    with pytest.raises(expected_exception):
        switch_habit_status(habit, flag)
