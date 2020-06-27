import time
import pandas as pd
import numpy as np
import sys
import traceback

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}
VALID_CITY = ['Chicago', 'New York', 'Washington']
# DEBUG can be changed to display error tracestack
DEBUG = False
VALIDATORS_MESSAGE = {
    'INVALID_CITY': 'Please enter a valid city name.',
    'INVALID_MONTH': 'Please enter a valid month name.',
    'INVALID_DAY_OF_WEEK': 'Please enter a valid day of week.'
}
TRIP_DURATION_ASTYPE = 'timedelta64[m]'
TRIP_DURATION_TIME_UNIT = 'mins'
PAGE_SIZE = 5

def convert_month(month):
    try:
        converted_month = time.strptime(month, '%B').tm_mon
        return converted_month
    except:
        return ''

def convert_day_of_week(day):
    try:
        converted_day_of_week = time.strptime(day, '%A').tm_wday
        return converted_day_of_week
    except:
        return ''

def is_valid_city(city):
    try:
        return city and city in VALID_CITY
    except:
        if DEBUG:
            traceback.print_exc(file=sys.stdout)
            return False

def is_valid_month(month):
    converted_month = convert_month(month)
    return converted_month

def is_valid_day_of_week(day_of_week):
    converted_day_of_week = convert_day_of_week(day_of_week)
    return converted_day_of_week is 0 or converted_day_of_week

def is_column_valid(df, column_name):
    try:
        return True if not df.empty and column_name in df.columns else False
    except:
        if DEBUG:
            traceback.print_exc(file=sys.stdout)
        return False

def print_most_popular_value_by_column(df, column_name, print_context):
    try:
        if is_column_valid(df, column_name):
            popular_value = df[column_name].mode()[0]
            print(print_context, popular_value)
    except:
        if DEBUG:
            traceback.print_exc(file=sys.stdout)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ''
    month = ''
    day = ''
    filter_by = ''
    is_valid_input = True
    done = False

    while not done:
        if not city:
            # get user input for city (chicago, new york city, washington).
            city = input(
            "Would you like to see data for Chicago, New York, or Washington? Please enter 'Chicago' or 'New York' or 'Washington': ")
        
        is_valid_input = is_valid_city(city)
        if is_valid_input:
            if not filter_by:
                filter_by = input(
                    "Would you like to filter the data by month, day, or not at all? Please enter 'month' or 'day' or 'not at all' or any other character(s) for no filter: ")
            
            if filter_by == 'month':
                # get user input for month (all, january, february, ... , june)
                month = input(
                    'Which month - January, February, March, April, May, or June? ')
                day = ''
                is_valid_input = is_valid_month(month)
                if not is_valid_input:
                    print(VALIDATORS_MESSAGE.get('INVALID_MONTH'))
            elif filter_by == 'day':
                # get user input for day of week (all, monday, tuesday, ... sunday)
                day = input(
                    'Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ')
                month = ''
                is_valid_input = is_valid_day_of_week(day)
                if not is_valid_input:
                    print(VALIDATORS_MESSAGE.get('INVALID_DAY'))
            else:
                month = ''
                day = ''
        else:
            city = ''
            print(VALIDATORS_MESSAGE.get('INVALID_CITY'))

        if not month:
            month = ''
        if not day:
            day = ''
        
        done = True if is_valid_input else False

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = ''
    try:
        filename = CITY_DATA.get(city.lower())
        if filename:
            # load data file into a dataframe
            df = pd.read_csv(filename)
            # convert the Start Time column to datetime
            if is_column_valid(df, 'Start Time'):
                df['Start Time'] = pd.to_datetime(df['Start Time'])
                # extract month and day of week from Start Time to create new columns
                df['month'] = df['Start Time'].dt.month
                df['day_of_week'] = df['Start Time'].dt.day_name()
                if month:
                    df = df[df['month'] == convert_month(month)]
                elif day:
                    df = df[df['day_of_week'] == day.title()]
                return df
    except:
        if DEBUG:
            traceback.print_exc(file=sys.stdout)
        return None


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print_most_popular_value_by_column(df, 'month', 'Most Common Month: ')

    # display the most common day of week
    print_most_popular_value_by_column(
        df, 'day_of_week', 'Most Common Day of Week: ')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print_most_popular_value_by_column(df, 'hour', 'Most Common Start Hour: ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print_most_popular_value_by_column(
        df, 'Start Station', 'Most Common Used Start Station: ')

    # display most commonly used end station
    print_most_popular_value_by_column(
        df, 'End Station', 'Most Common Used End Station: ')

    # display most frequent combination of start station and end station trip
    if is_column_valid(df, 'Start Station') and is_column_valid(df, 'End Station'):
        df['Start-End Station'] = df['Start Station'] + ' -> ' + df['End Station']
        print_most_popular_value_by_column(
            df, 'Start-End Station', 'Most Frequent Combination of Start Station and End Station Trip: ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if is_column_valid(df, 'Start Time') and is_column_valid(df, 'End Time'):
        df['Total Duration'] = (pd.to_datetime(
            df['End Time']) - pd.to_datetime(df['Start Time'])).astype(TRIP_DURATION_ASTYPE)

        # display total travel time
        total_duration = (df['Total Duration'].sum(min_count=0))
        print('Total Travel Time: ', total_duration, TRIP_DURATION_TIME_UNIT)

        # display mean travel time
        mean_duration = (df['Total Duration'].mean(skipna=True))
        print('Mean Travel Time: ', mean_duration, TRIP_DURATION_TIME_UNIT)
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if is_column_valid(df, 'User Type'):
        print('Counts of User Types:\n', df['User Type'].value_counts(dropna=True))

    # Display counts of gender
    if is_column_valid(df, 'Gender'):
        print('\nCounts of Gender:\n', df['Gender'].value_counts(dropna=True))

    # Display earliest, most recent, and most common year of birth
    if is_column_valid(df, 'Birth Year'):
        print('\nEarliest year of birth: ', int(df['Birth Year'].min(skipna=True)))
        print('Most recent year of birth: ', int(
            df['Birth Year'].max(skipna=True)))
        print('Most common year of birth: ', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def handle_display_raw_data(df):
    try:
        is_continue = True
        start = 0
        end = PAGE_SIZE
        prompt = f"Would you like to see {PAGE_SIZE} lines of raw data? Enter 'yes' or 'no': "
        while is_continue:
            display_raw_data = input(prompt)
            
            if display_raw_data == 'yes':
                print(df.iloc[start:end, :])
                start = end
                end = start + PAGE_SIZE
                prompt =  "Would you like to see more raw data? Enter 'yes' or 'not': "
            else:
                is_continue = False
    except:
        traceback.print_exc(file=sys.stdout)

def main():
    try:
        while True:
            city, month, day = get_filters()
            if DEBUG:
                if city:
                    print('accessing data of city ', city, end='')
                    if day:
                        print(' on ', day, end='')
                    if month:
                        print(' in ', month, end='')
                    print('...')
                    print('-'*40)
            if city:
                df = load_data(city, month, day)
                if df is not None and not df.empty:
                    time_stats(df)
                    station_stats(df)
                    trip_duration_stats(df)
                    user_stats(df)
                    handle_display_raw_data(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
    except:
        if DEBUG:
            traceback.print_exc(file=sys.stdout)


if __name__ == "__main__":
    main()
