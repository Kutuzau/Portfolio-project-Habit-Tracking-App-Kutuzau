# This file contains statistical and other functions for habits, which are used in main file

import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
from my_exceptions import WrongHabitName, WrongHabitId, WrongHabitStatus


def get_previous_habit_time(habit: str) -> date:
    # User can get the date of the last successful implementation of the habit
    """
    :param habit: habit name
    :return: date of the last successful implementation of the habit
    """
    habit_time_df = pd.read_csv('habit_time.csv')
    habit_id = get_habit_id(habit)
    habit_time = habit_time_df[habit_time_df['habit_id'] == habit_id]
    try:
        previous_habit_time = pd.to_datetime(habit_time['time'].iloc[-1], format='%Y-%m-%d %H:%M:%S')
    except ValueError:
        previous_habit_time = pd.to_datetime(habit_time['time'].iloc[-1], format='%Y-%m-%d')
    return previous_habit_time.date()


def get_max_habit_stripe(habit: str) -> int:
    # User can get the maximum habit stripe
    """
    :param habit: habit name
    :return: the maximum number of consecutive successful execution of the habit
    """
    habit_info_df = pd.read_csv('habit_info.csv')
    habit_id = get_habit_id(habit)
    return int(habit_info_df[habit_info_df['habit_id'] == habit_id]['max_streak_position'].iloc[0])


def switch_habit_status(habit: str, flag: str) -> int:
    # User can change activate or deactivate the habit
    """
    :param habit: habit name for possible changing its status
    :param flag: '1' - to activate habit; '0' - to deactivate habit
    :return the final status
    """
    if flag not in ('1', '0'):
        raise WrongHabitStatus(f'Habit status must be only 1 (activated) or 0 (deactivated).')
    raise_wrong_habit_name(habit)
    habit_info_df = pd.read_csv('habit_info.csv')
    habit_info_df.loc[habit_info_df['name'] == habit, 'status'] = int(flag)
    habit_info_df.to_csv('habit_info.csv', index=False)
    return int(flag)


def is_active_habit(habit: str) -> bool:
    """
    :param habit: habit name in string format
    :return: True if the habit is active and False if not
    """
    raise_wrong_habit_name(habit)
    habit_info_df = pd.read_csv('habit_info.csv')
    return habit_info_df[habit_info_df['name'] == habit]['status'].iloc[0] == 1


def get_habits_with_the_status(status: str) -> list[str]:
    # User can check what habits are activated and deactivated
    """
    Function return the list of habits with the status
    :param status: '1' - active habit; '0' - deactivated
    """
    if status not in ('0', '1'):
        raise WrongHabitStatus
    habit_info_df = pd.read_csv('habit_info.csv')
    return habit_info_df[habit_info_df['status'] == int(status)]['name'].to_list()


def get_all_habits() -> list[str]:
    # User can get information about all existing habits
    """Return the list of all habit names"""
    habit_info_df = pd.read_csv('habit_info.csv')
    return habit_info_df['name'].to_list()


def get_habits_from_previous_month(threshold: str = '1') -> list[str] | None:
    # User can get info about habits which were completed more than a certain number of times in the past month
    """Habits used less than "threshold" times last month will not return.
    Other ones will be returned with printing their using count.
    The results are also presented as a bar plot.
    return: list of habits or printing text if there is no such habits"""
    try:
        threshold = int(threshold)
    except ValueError:
        raise ValueError('Threshold number must be integer type and greater than 0.')

    if threshold < 1:
        raise ValueError('Threshold number must be greater than 0.')

    habit_info_df = pd.read_csv('habit_info.csv')
    habit_time_df = pd.read_csv('habit_time.csv')

    previous_month_mask = pd.to_datetime(habit_time_df['time']) >= (datetime.now() - timedelta(days=30))
    previous_month_habit_time = habit_time_df[previous_month_mask]
    habit_count = previous_month_habit_time.groupby('habit_id')['habit_id'].count().reset_index(name='habit_count')
    result = habit_count.merge(habit_info_df, on='habit_id')
    result = result[result['habit_count'] >= threshold]
    result = result.sort_values(by='habit_count', ascending=False)

    print(f'There is {len(result)} such habits.')
    plot_bar(x=result['name'], y=result['habit_count'], title="Habits completed last month")

    return result['name'].to_list() if result['name'].to_list() \
        else print('Unfortunately, you have no such habits last month.')


def plot_bar(x: pd.Series | list, y: pd.Series | list, title: str) -> None:
    """
    Show bar plot
    :param x: list of values
    :param y: number of the value
    :param title: title of the bar plot
    """
    colors = ['black', 'blue', 'red', 'green', 'limegreen',
              'springgreen', 'orange', 'violet', 'pink', 'gray']
    plt.bar(x, y, alpha=0.6, color=colors)
    plt.xticks(rotation=15, ha='right')
    plt.title(title, fontsize=15)
    plt.ylabel('count', fontsize=15)
    plt.show()


def get_max_habit_stripe_from_all_habits() -> tuple[str, int]:
    # User can check the longest streaks for all habits
    """
    :return: tuple of habit name and corresponding max streak from all the habit exist
    """
    habit_info_df = pd.read_csv('habit_info.csv')
    habit_time_df = pd.read_csv('habit_time.csv')
    result = habit_info_df.merge(habit_time_df, on='habit_id')
    result = result[result['max_streak_position'] == result['max_streak_position'].max()]
    return result['name'].iloc[0], result['max_streak_position'].iloc[0]


def get_habits_with_equal_required_interval() -> tuple:
    # User can check which habits has certain periodicity
    """
    During execution, the function asks the user for a time interval.
    :return: timedelta that mentioned above and list of all corresponding habits
    """
    interval = check_and_get_interval()
    habit_info_df = pd.read_csv('habit_info.csv')
    result = habit_info_df[pd.to_timedelta(habit_info_df['required_interval']) == interval]
    return interval.days, result['name'].to_list()


def check_and_get_interval() -> timedelta:
    """
    Getting time interval in string format and return timedelta format.
    Validation of input data is also included.
    """
    while True:
        period = input('Choose the time interval that you are going to use for the habit: \n'
                       'For example: "2 w" for 2 weeks, "5 d" for 5 days.\n'
                       'Use only days or weeks. \n').strip()
        try:
            num_interval = int(period.split()[0])
        except (TypeError, ValueError):
            print('Interval is not in the correct form. Note, use only positive numbers. Try again.')
            continue
        if num_interval <= 0:
            print('You must use positive numbers for days and weeks. Try again.')
            continue
        if period[-1] == 'w':
            return timedelta(weeks=num_interval)
        elif period[-1] == 'd':
            return timedelta(days=num_interval)
        else:
            print('Interval is not in the correct form. Try again.')
            continue


def input_habit_date() -> date:
    """
    Get date from user and converts to date format
    :return: date
    """
    while True:
        time_str = input('Specify the date for performing the habit in the following format: dd-mm-yyyy. \n'
                         'For example: 05-10-2023. \n').strip()
        try:
            return datetime.strptime(time_str, '%d-%m-%Y').date()
        except ValueError:
            print('Date is not in the correct form. Try again.')
            continue


def get_habit_id(habit) -> int | None:
    """
    Based on the habit name, the corresponding ID number is returned.
    :param habit: habit name
    :return: habit_id
    """
    habit_info_df = pd.read_csv('habit_info.csv')
    if habit not in habit_info_df['name'].to_list():
        raise WrongHabitId(f'{habit} is not in habit-list.')
    return habit_info_df[habit_info_df['name'] == habit]['habit_id'].iloc[0]


def raise_wrong_habit_name(habit: str) -> None:
    habit_info_df = pd.read_csv('habit_info.csv')
    if habit not in habit_info_df['name'].to_list():
        raise WrongHabitName(f'There is no habit with the name "{habit}".')