# This program was written using PyCharm with Python version 3.12
# It contains 5 py files: main.py and 4 additional, which are also attached
# There are also additional test files, which were used for testing with pytest

import pandas as pd
from habit import Habit
from pathlib import Path
from my_exceptions import WrongTime, WrongHabitStatus, NoData
from statistics_and_additions import get_habits_with_equal_required_interval, get_max_habit_stripe_from_all_habits
from statistics_and_additions import get_all_habits, get_habits_from_previous_month, get_habits_with_the_status
from statistics_and_additions import get_previous_habit_time, get_max_habit_stripe
from statistics_and_additions import check_and_get_interval, input_habit_date
from statistics_and_additions import is_active_habit, switch_habit_status

# First of all main menu should be created, where user can select the desired function
# Depending on the user's choice, the app will perform different tasks
if __name__ == '__main__':
    while True:
        if not Path('habit_info.csv').exists():
            print('Hello! You do not have any habits. You have to create the first one.')
            main_menu = 'create'
            break
        main_menu = input('Main menu: \n'
                          '"create" - to create new habit; \n'
                          '"do" - to do existing habit; \n'
                          '"status" - to change habit status; \n'
                          '"statistics" - to get statistics; \n'
                          '"exit" - to exit the program. \n')
        if main_menu in ('create', 'do', 'status', 'statistics', 'exit'):
            habit_info_df = pd.read_csv('habit_info.csv')
            break
        else:
            print('You must use only "create", "do", "status", "statistics" or "exit".')

    # User can create a new habit
    if main_menu == "create":
        habit_name = input('The name of your new habit is: \n').strip()
        if habit_name:
            try:
                if habit_name in habit_info_df['name'].to_list():
                    print(f'The habit "{habit_name}" has already existed.')
            except NameError:
                pass

            interval = check_and_get_interval()
            day = input_habit_date()
            try:
                habit = Habit(habit_name, day, interval)
                habit.add()
            except NoData:
                print('habit_info.csv and habit_time.csv files are not correct. \n'
                      'Please, delete them and start working with your habits from the scratch.')
        else:
            print('You entered an empty string, which is not allowed.')

    # User can execute the existing habit
    if main_menu == "do":
        habit_name = input('The name of your habit is: \n').strip()
        if not habit_name:
            print('You entered an empty string, which is not allowed.')
        elif habit_name not in habit_info_df['name'].to_list():
            print(f'"{habit_name}" is not in your habit-list.')
        else:
            if habit_info_df[habit_info_df['name'] == habit_name]['status'].iloc[0] == 1:
                day = input_habit_date()
                try:
                    habit = Habit(habit_name, day)
                    habit.do()
                except WrongTime:
                    print("Wrong date. You used date less than previous habit date (or equal). It's impossible.")
                except NoData:
                    print('habit_info.csv and habit_time.csv files are not correct. \n'
                          'Please, delete them and start working with your habits from the scratch.')
            else:
                print(f'The habit "{habit_name}" is deactivated. \n'
                      f'If you want to work on the habit, you first need to activate it.')

    # User can activate and deactivate existing habits
    if main_menu == 'status':
        habit_name = input('Input habit name to change the habit status: \n').strip()
        if not habit_name:
            print('You entered an empty string, which is not allowed.')
        elif habit_name not in habit_info_df['name'].to_list():
            print(f'"{habit_name}" is not in your habit-list.')
        else:
            if is_active_habit(habit_name):
                print(f'Habit "{habit_name}" is active.')
                status = input('"0" - to deactivate the habit; \n"1" - to leave active status. \n')
            else:
                print(f'Habit "{habit_name}" is deactivated.')
                status = input('"1" - to activate the habit; \n"0" - to leave deactivated status. \n')
            try:
                switch_habit_status(habit_name, status)
                print(f'The status of the habit is "{"active" if status == "1" else "deactivated"}".')
            except WrongHabitStatus:
                print('This is a wrong option.')

    # User can get a full statistics for one or all existing habits
    if main_menu == 'statistics':
        next_option = input('"one" to get statistics for one habit;\n'
                            '"all" to get statistics for all habits. \n').strip()
        if next_option == 'one':
            habit_name = input('Input habit for statistics: \n').strip()
            if not habit_name:
                print('You entered an empty string, which is not allowed.')
            elif habit_name not in habit_info_df['name'].to_list():
                print(f'"{habit_name}" is not in your habit-list.')
            else:
                stat = input('Choose the next option: \n'
                             '"prev" - to show previous habit time; \n'
                             '"max" - to show max habit stripe; \n'
                             '"status" - to know is active habit or not. \n').strip()
                match stat:
                    case 'prev':
                        print(f'The last use of the habit took place on {get_previous_habit_time(habit_name)}.')
                    case 'max':
                        print(f'Maximum streak of the habit is {get_max_habit_stripe(habit_name)} time(s).')
                    case 'status':
                        if is_active_habit(habit_name):
                            print(f'Habit "{habit_name}" is active.')
                        else:
                            print(f'Habit "{habit_name}" is deactivated.')
                    case _:
                        print('Wrong input data.')
        elif next_option == 'all':
            stat = input('Choose the next option: \n'
                         '"all" - to show the list of your habits; \n'
                         '"active" - to show the list of active habits; \n'
                         '"deactivated" - to show the list if deactivated habits; \n'
                         '"max" - to know max habit stripe from all habits; \n'
                         '"interval" - to get habit names with equal required time interval; \n'
                         '"month" - to get the most used habits last month. \n').strip()
            match stat:
                case 'all':
                    habits = get_all_habits()
                    print('The list of your habits: ')
                    for habit in habits:
                        print(habit)
                case 'active':
                    print('The active habits: ')
                    for habit in get_habits_with_the_status('1'):
                        print(habit)
                case 'deactivated':
                    print('The deactivated habits: ')
                    for habit in get_habits_with_the_status('0'):
                        print(habit)
                case 'max':
                    name, times = get_max_habit_stripe_from_all_habits()
                    print(f'The most frequently committed habit is "{name}". It was done {times} times.')
                case 'interval':
                    interval, habits = get_habits_with_equal_required_interval()
                    print(f'There are habits with equal required time interval {interval} day(s): ')
                    for habit in habits:
                        print(habit)
                case 'month':
                    threshold = input('Specify the minimum threshold number of doing a habit last month. \n'
                                      'Habits had done less times will not be displayed. \n').strip()
                    try:
                        get_habits_from_previous_month(threshold)
                    except TypeError as ex:
                        print(ex)
                    except ValueError as ex:
                        print(ex)
                case _:
                    print('Wrong option.')
        else:
            print('Wrong option.')

    print('-' * 17)
    print('Program is finished.')
