import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

valid_months = 'january, february, march, april, may, june, july, august, september, october, november, december'.split(', ')
valid_days = 'sunday, monday, tuesday, wednesday, thursday, friday, saturday'.split(', ')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Initialize variables
    city, month, day = None, None, None
    mismatch = 'Does not match options.'
    
    # Get city input
    while city == None:
        city = input('Choose a city by name from this list: Chicago, New York City, Washington: ')
        city = city.lower()
        if city not in CITY_DATA.keys():
            print(mismatch)
            city = None
   
    # Get month input
    while month == None:
        month = input('Choose a month (e.g. January) or hit enter for all months: ')
        month = month.lower()
        if month == '':
            month = 'all'
        else:
            if month not in valid_months:
                print(mismatch)
                month = None
    
    # Get day input
    while day == None:
        day = input('Choose a day (e.g. Monday) or hit enter for all days: ')
        day = day.lower()
        if day == '':
            day = 'all'
        else:
            if day not in valid_days:
                print(mismatch)
                day = None
    print(f'Filters are - City: {city}, Month: {month}, Day: {day}')
    print('-'*40)
    return city, month, day

def load_data(city, month='all', day='all'):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    
    print('Before filters, the frame is:')
    print(df.shape)
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_num = valid_months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month_num]
        print('After filtering by month, the frame is:')
        print(df.shape)
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day_num = valid_days.index(day)
        df = df[df['day_of_week'] == day_num]
        print('After filtering by day, the frame is:')
        print(df.shape)
        
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    top_month = valid_months[df['month'].mode()[0] - 1]
    print(f'The top month is: {top_month}')

    # TO DO: display the most common day of week
    top_day = valid_days[df['day_of_week'].mode()[0]]
    print(f'The top day is: {top_day}')

    # TO DO: display the most common start hour
    top_hour = df['Start Time'].dt.hour.mode()[0]
    print(f'The top hour is: {top_hour}:00')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print(f'Common start: {start_station}')

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print(f'Common end: {end_station}')

    # TO DO: display most frequent combination of start station and end station trip
    station_combo_group = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    station_combo_group = station_combo_group.sort_values('count', ascending=False)
    most_combo = station_combo_group.iloc[0] 
    print(f'Common route: {most_combo}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print(f'Total trip duration is {total_travel} and mean duration is {mean_travel}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User types are:')
    print(df['User Type'].value_counts())

    # Display counts of gender if available
    if 'Gender' in df.columns:
        print('\nReported gender is:')
        print(df['Gender'].value_counts())
    else:
        print('\nNo gender data available for this city.')

    # Display birth year stats if available
    if 'Birth Year' in df.columns:
        birth_earliest = df['Birth Year'].dropna().min()
        birth_latest = df['Birth Year'].dropna().max()
        birth_mode = df['Birth Year'].dropna().mode()[0]
        print(f'\nFor birth year:')
        print(f'Earliest: {int(birth_earliest)}')
        print(f'Latest: {int(birth_latest)}')
        print(f'Most common: {int(birth_mode)}')
    else:
        print('\nNo birth year data available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw_data(df):
    """Offers to show the user the raw data of the filtered data, 5 rows at a time, as long as the user requests it."""
    
    start_loc = 0
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no: ').lower()
        if view_data != 'yes':
            break
            
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        
        # Check if we've reached the end of the dataset
        if start_loc >= len(df):
            print('\nNo more data to display.')
            break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        view_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
