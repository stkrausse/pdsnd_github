import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Global definition to be used in the functions
# get_filters(), load_data(city, month, day), time_stats(df)
month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

#  global variable since it should exist beyond its funktion display_raw_data(df)
counter = 0

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        print("\n Please enter one from the following city names: \n")
        for key in CITY_DATA:
            print("\t {}".format(key))
        city = input("\n City name: ").lower()
        if city in CITY_DATA:
            break
        else:
            print("\n The city you selected was NOT in the list. Please try again. \n")

    # get user input for month (all, january, february, ... , june)

    while True:
        print("\n For what month you want to look up the data? Please select from the following list: \n")
        for mnth in month_list:
            print("\t {}".format(mnth))
        month = input("\n Month name: ").lower()
        if month in month_list:
            break
        else:
            print("\n The month you selected was NOT in the list. Please try again. \n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        weekday_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        print("\n For what day you want to look up the data? Please select from the following list: \n")
        for wd in weekday_list:
            print("\t {}".format(wd))
        day = input("\n Day name: ").lower()
        if day in weekday_list:
            break
        else:
            print("\n The day you selected was NOT in the list. Please try again. \n")

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
    df = pd.read_csv('./' + city.replace(" ", "_") + '.csv')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() # weekday_name # .day_name()

    #####################################################################
    # Timestamp.weekday_name is deprecated since version 0.23.0:
    # Change code to Timestamp.day_name() with newer versions
    # of pandas
    #####################################################################

    # filter by month if applicable
    if month != 'all':
       # use the index of the months list to get the corresponding int
        month = month_list.index(month) # definition matches without increment since index zero = 'all'

        # filter by month to create the new dataframe
        df = df.loc[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'].str.lower()==day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    sol_month = month_list[df['month'].mode()[0]]
    print("Most common month:\t {} [count = {}]".format(sol_month, np.count_nonzero(df['month'] == month_list.index(sol_month))))

    # display the most common day of week
    sol_day = (df['day_of_week'].mode()[0])
    print("Most common day:\t {} [count = {}]".format(sol_day.lower(), np.count_nonzero(df['day_of_week'] == sol_day)))

    # display the most common start hour
    sol_hour = df['Start Time'].dt.hour.mode()[0]
    print("Most common start hour:\t {} [count = {}]".format(sol_hour, np.count_nonzero(df['Start Time'].dt.hour == sol_hour)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    sol_start_station = df['Start Station'].mode()[0]
    print("Most common start station:\t {} [count = {}]".format(sol_start_station, np.count_nonzero(df['Start Station'] == sol_start_station)))

    # display most commonly used end station
    sol_end_station = df['End Station'].mode()[0]
    print("Most common end station:\t {} [count = {}]".format(sol_end_station, np.count_nonzero(df['End Station'] == sol_end_station)))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " -> " + df['End Station']
    sol_trip = df['Trip'].mode()[0]
    print("Most common trip:\t\t {} [count = {}]".format(sol_trip, np.count_nonzero(df['Trip'] == sol_trip)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def time_format(total_time_in_seconds):
    """Returns a string which converts seconds into days, days, hours, minutes and seconds."""
    seconds_in_day = 86400 # [one day has 86400 = 60 * 60 * 24 seconds]
    seconds_in_hour = 3600 # [one hour has 3600 = 60 * 60 seconds]
    seconds_in_minute = 60 # [one minute has 60 seconds]
    time_dict = {}
    time_dict["day(s)"] = int(total_time_in_seconds // seconds_in_day)
    total_time_in_seconds %= seconds_in_day
    time_dict["hour(s)"] = int(total_time_in_seconds // seconds_in_hour)
    total_time_in_seconds %= seconds_in_hour
    time_dict["minute(s)"] = int(total_time_in_seconds // seconds_in_minute)
    total_time_in_seconds %= seconds_in_minute
    time_dict["second(s)"] = int(round(total_time_in_seconds, 0))
    return_string = ""
    if time_dict["day(s)"] != 0:
        return_string += " {} day(s)".format(time_dict["day(s)"])
    if time_dict["hour(s)"] != 0:
        return_string += " {} hour(s)".format(time_dict["hour(s)"])
    if time_dict["minute(s)"] != 0:
        return_string += " {} minute(s)".format(time_dict["minute(s)"])
    if time_dict["second(s)"] != 0:
        return_string += " {} seconds".format(time_dict["second(s)"])
    return return_string

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time:\t {}".format(time_format(df['Trip Duration'].sum())))

    # display mean travel time
    print("Mean travel time:\t {}".format(time_format(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df_helper = df['User Type'].value_counts()
    for key in df_helper.index:
        print("{} \t {}".format(key, df_helper[key]))

    # Display counts of gender
    print()
    if 'Gender' in df.columns:
        df_helper = df['Gender'].value_counts()
        for key in df_helper.index:
            print("{} \t\t {}".format(key, df_helper[key]))
    else:
        print("Dataset does NOT contain 'Gender'")

    # Display earliest, most recent, and most common year of birth
    print()
    if 'Birth Year' in df.columns:
        print("Erliest year of birth:\t\t {}".format(int(df['Birth Year'].min())))
        print("Most recent year of birth:\t {}".format(int(df['Birth Year'].max())))
        sol_common_birth = df['Birth Year'].mode()[0]
        print("Most common year of birth:\t {} [count = {}]".format(int(sol_common_birth), np.count_nonzero(df['Birth Year'] == sol_common_birth)))
    else:
        print("Dataset does NOT contain 'Birth Year'")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data on user request, iterating 5 entries each."""
    global counter
    while True:
        answer = input("\n Do you want to see raw data? Enter yes or no: ").lower()
        if answer == 'yes':
            helper = pd.DataFrame(df, columns = ['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year'])
            print(helper[counter:counter + 5])
            counter += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
