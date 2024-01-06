# This file contains code for generating data for 5 examples of habits with different periodicity

from datetime import date, timedelta
from habit import Habit
from random import sample

habits = {'tennis': timedelta(days=4),
          'reading': timedelta(days=1),
          'football': timedelta(weeks=1),
          'swimming': timedelta(weeks=2),
          'jogging': timedelta(days=1)}

# The start date and generating parameters can be changed
for habit, interval in habits.items():
    new_habit = Habit(habit, date(2023, 12, 1), interval)
    new_habit.add()

for day in range(1, 32):
    for habit in habits.keys():
        if 1 in sample([1, 2, 3, 4], 1):
            habit_to_do = Habit(habit, date(2023, 12, 1) + timedelta(days=day))
            habit_to_do.do()
