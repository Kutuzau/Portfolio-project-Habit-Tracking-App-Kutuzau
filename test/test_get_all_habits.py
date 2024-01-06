from statistics_and_additions import get_all_habits


def test_get_all_habits():
    assert get_all_habits() == ['tennis', 'reading', 'football', 'swimming', 'jogging']
