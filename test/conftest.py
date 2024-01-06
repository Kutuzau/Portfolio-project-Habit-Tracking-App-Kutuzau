import pytest
import shutil
import os
from pathlib import Path


# scope='session', autouse=True means the function will be used before and after all tests
# Code before 'yield' will be used before tests and after 'yield' will be used after all tests
@pytest.fixture(scope='session', autouse=True)
def get_test_db() -> None:
    """
    The function replaces real data to test it.
    If there is no any real data, test data are used temporary.
    During the process the backup of the existed real data is created.
    Warning: test data are located in test/test_db directory.
    The location should not be deleted or changed!
    """
    if Path('habit_info.csv').exists() and Path('habit_time.csv').exists():
        # To create the backup for real data
        shutil.copy('habit_info.csv', 'habit_info_temp.csv')
        shutil.copy('habit_time.csv', 'habit_time_temp.csv')

        # To replace the real data with the test data
        shutil.copy('test/test_db/habit_info.csv', 'habit_info.csv')
        shutil.copy('test/test_db/habit_time.csv', 'habit_time.csv')
    else:
        # To get the test data
        shutil.copy('test/test_db/habit_info.csv', 'habit_info.csv')
        shutil.copy('test/test_db/habit_time.csv', 'habit_time.csv')

    yield
    # To replace the test data with real data
    if Path('habit_info_temp.csv').exists() and Path('habit_time_temp.csv').exists():
        shutil.copy('habit_info_temp.csv', 'habit_info.csv')
        shutil.copy('habit_time_temp.csv', 'habit_time.csv')
        os.remove('habit_info_temp.csv')
        os.remove('habit_time_temp.csv')
    else:
        # To delete the temporary test data
        os.remove('habit_info.csv')
        os.remove('habit_time.csv')
