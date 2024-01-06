# This file contains code for creating and using class Habit

from pathlib import Path
from datetime import timedelta, date
import pandas as pd
from my_exceptions import WrongTime, NoData
from statistics_and_additions import get_habit_id, get_previous_habit_time, get_max_habit_stripe


class Habit:

    def __init__(self, habit_name: str, day: date, interval: timedelta = None) -> None:
        """
        The __init__ method creates:
        self.habit_info: DataFrame with habit info;
        self.habit_time: DataFrame with time info for habit

        :param habit_name: habit name
        :param day: date of using the habit
        :param interval: required interval for the habit
        """
        self.habit_name = habit_name
        self.day = day
        self.interval = interval

        if Path('habit_info.csv').exists() or Path('habit_time.csv').exists():
            try:
                self.habit_info_df = pd.read_csv('habit_info.csv')
                self.habit_time_df = pd.read_csv('habit_time.csv')
                self.is_data = True
            except FileNotFoundError:
                raise NoData('There are no files habit_info.csv and/or habit_time.csv or they are incorrect.')
        else:
            # During the first start DataFrames will be created and habit will be added automatically
            self.is_data = False
            self.habit_info_df, self.habit_time_df = self._make_dataframes(0)
            self.habit_info_df.to_csv('habit_info.csv', index=False)
            self.habit_time_df.to_csv('habit_time.csv', index=False)
            print(f'The habit "{habit_name}" was added to database and starts to go.')

    def _make_dataframes(self, habit_id: int) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        :param habit_id: unique id corresponding to the habit
        :param habit: habit name
        :param habit_interval: required interval for the habit
        :param habit_day: day of using the habit
        :return: tuple of 2 DataFrames
        """
        habit_info_df = pd.DataFrame({'habit_id': [habit_id],
                                      'name': [self.habit_name],
                                      'required_interval': [self.interval],
                                      'current_streak_position': [1],
                                      'max_streak_position': [1],
                                      'status': [1]})
        habit_time_df = pd.DataFrame({'habit_id': [habit_id],
                                      'time': [self.day],
                                      'stripe_length': [1]})
        return habit_info_df, habit_time_df

    def add(self) -> None:
        """
        This part of code will add a habit to database
        """
        if self.is_data:
            habit_id = int(self.habit_info_df['habit_id'].max()) + 1
            new_habit_info, new_habit_time = self._make_dataframes(habit_id)
            self.habit_info_df = pd.concat([self.habit_info_df, new_habit_info], ignore_index=True)
            self.habit_time_df = pd.concat([self.habit_time_df, new_habit_time], ignore_index=True)
            self.habit_info_df.to_csv('habit_info.csv', index=False)
            self.habit_time_df.to_csv('habit_time.csv', index=False)
            print(f'The habit "{self.habit_name}" was added to database and starts to go.')

    def do(self) -> None:
        """
        This method allows to execute the habit
        As a result self.habit_time_df and corresponding csv file will be changed
        if "time" is greater than "previous habit time"
        """

        previous_habit_time = get_previous_habit_time(self.habit_name)
        if previous_habit_time >= self.day:
            raise WrongTime(f'The day {self.day} is greater than your previous habit day {previous_habit_time}. \n'
                            f'It is impossible.')
        habit_id = get_habit_id(self.habit_name)
        stripe_length_number = self._update_max_habit_stripe(habit_id)

        new_habit_time = pd.DataFrame({'habit_id': [habit_id],
                                       'time': [self.day],
                                       'stripe_length': [stripe_length_number]})
        self.habit_time_df = pd.concat([self.habit_time_df, new_habit_time])
        self.habit_time_df.to_csv(f'habit_time.csv', index=False)
        print(f'The habit "{self.habit_name}" was used again.')

    def _update_max_habit_stripe(self, habit_id: int) -> int:
        """
        Submethod to update the stripe length for the habit.
        :param habit_id: unique id corresponding to the habit
        :return: increment of the habit stripe or setting the value to '1' if the habit execution time was missed.
        """
        previous_habit_time = get_previous_habit_time(self.habit_name)
        habit_time = self.habit_time_df[self.habit_time_df['habit_id'] == habit_id]
        habit_df = self.habit_info_df[self.habit_info_df['habit_id'] == habit_id]
        interval = pd.to_timedelta(habit_df['required_interval'].iloc[0])

        # Updating max habit stripe
        if self.day - previous_habit_time <= interval:
            stripe_length_number = int(habit_time['stripe_length'].iloc[-1]) + 1
            if stripe_length_number > get_max_habit_stripe(self.habit_name):
                self.habit_info_df.loc[
                    self.habit_info_df['habit_id'] == habit_id, 'max_streak_position'] = stripe_length_number
        else:
            stripe_length_number = 1

        self.habit_info_df.loc[
            self.habit_info_df['habit_id'] == habit_id, 'current_streak_position'] = stripe_length_number
        self.habit_info_df.to_csv(f'habit_info.csv', index=False)

        return stripe_length_number
