# Habit Tracking App

Habit Tracking App is a feature-rich and intuitive App written in Python. It seamlessly combines the power of Object-Oriented and Functional Programming to provide users with a comprehensive tool for building and maintaining positive habits.

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Getting Started](#getting-started)
  - [Menu Options](#menu-options)
  - [Sample Data Generation](#sample-data-generation)
- [Habit Class](#habit-class)
- [Custom Exceptions](#custom-exceptions)
- [Statistics and Additions](#statistics-and-additions)
- [Testing](#testing)

## Project Overview
Habit Tracking App is designed to empower users in establishing and nurturing positive habits. It consists of modular components, each serving a specific purpose, making the codebase modular, maintainable, and extensible. Whether you want to create new habits, track your progress, or analyze statistics, Habit Tracking App has got you covered.

## Project Structure
- **main.py:** The central hub that imports functions from other modules to present a user-friendly interface.
- **generating_data.py:** Generates sample data for five different habits with varying periodicity.
- **habit.py:** Houses the Habit class and manages habit-related functionalities such as creation, execution, and data management.
- **my_exceptions.py:** Defines custom exceptions to enhance control and error handling in the program.
- **statistics_and_additions.py:** Contains statistical and utility functions for habits, utilized in the main file.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/Kutuzau/Portfolio-project-Habit-Tracking-App-Kutuzau
   ```
2. Install required dependencies:
   ```
   pip install pandas
   pip install matplotlib
   ```

## Usage

### Getting Started
To run Habit Tracking App, execute the following command in your terminal:
```
python main.py
```

### Menu Options
Habit Tracking App provides a rich set of menu options:
- **Create a New Habit:** Define a new habit and its properties.
- **Execute an Existing Habit:** Log the completion of an existing habit.
- **Activate/Deactivate Habits:** Enable or disable habits as needed.
- **Get Full Statistics:** View comprehensive statistics for one or all habits.

### Sample Data Generation
To check the functions by populating the app with sample habits, it is possible to use the `generating_data.py` script. Customize the start date and generating parameters as needed:
```
python generating_data.py
```

## Habit Class
The Habit class in `habit.py` is the backbone of Habit Tracking App. It encapsulates habit-related functionalities, ensuring seamless management and execution of habits. The class is designed with modularity and extensibility in mind, making it easy to integrate with the broader application.

## Custom Exceptions
The `my_exceptions.py` module defines custom exceptions to enhance error handling. These exceptions, such as `WrongTime`, `WrongHabitStatus`, and `NoData` are used to control the other parts of the program.

## Statistics and Additions
The `statistics_and_additions.py` module offers a suite of statistical and utility functions that power the app's analytical capabilities. From obtaining habit streaks to visualizing habits completed last month, these functions enrich the overall user experience.

## Testing
Habit Tracking App includes a comprehensive test suite to validate the correctness of its functions. The test suite covers critical functionalities such as habit ID retrieval, habit status switching, and obtaining statistics. It ensures the reliability and accuracy of the app's core features.

