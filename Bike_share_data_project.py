from calendar import month_name, day_name
from os import get_terminal_size, path
import pandas as pd
import time



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (list) city - name of the city to analyze
        (list) month - name of the month to filter by, or "all" to apply no month filter
        (list) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cutoff('*')
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = []
    cities = ['chicago', 'new york city', 'washington']
    list_of_cities = '\n'.join('"'+city_name.title()+'"' for city_name in cities)
    while not city:
        usr_inp = input('Please, type the name of one of the cities from the list:'
                        f'\n{list_of_cities}\n"all": for choosing all the cities above.'
                        '\n\nUser: ').lower().strip()
        if usr_inp in ['chicago', 'new york city', 'washington']:
            city.append(usr_inp)
            cutoff('~')
        elif usr_inp == 'all':
            city = cities
            cutoff('~')
        else:
            input_error()

    # get user input for month (all, january, february, ... , june)
    month = []
    available_months = '\n'.join('"'+month+'"' for month in month_name[1:7])
    while not month:
        usr_inp = input('Please enter the month name from the list below:'
                        f'or type "all" for not to set up the date filter. \nAvailable options:\n{available_months}' +
                        '\n"all": not to set up the date filter\n\nUser: ').title().strip()
        if usr_inp in month_name[1:7]:
            month.append(list(month_name).index(usr_inp))
            cutoff('~')
        elif usr_inp.strip().lower() == 'all':
            month = [*range(1, 7)]
            cutoff('~')
        else:
            input_error()
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = []
    weekday_names = '\n'.join('"'+one_day+'"' for one_day in day_name)
    while not day:
        usr_inp = input('Please enter the day name \nAvailable options:\n'
                f'{weekday_names}\n"all": not to set up the filter.\n\nUser: ').title().strip()
        if usr_inp in day_name:
            day.append([*day_name].index(usr_inp))
            cutoff('~')
        elif usr_inp.strip().lower() == 'all':
            day = [*range(7)]
            cutoff('~')
        else:
            input_error()
    return city, month, day


def cutoff(symbol = '-'):
    """
    Prints a console-wide string of thr symbol

    :param symbol: str. Only first symbol of a string will be printed.
    :return: None
    """
    try:
        print(get_terminal_size().columns*symbol[0])
    except OSError:
        print(symbol*40)
        return True


def input_error():
    """
    Prints a message about a wrong input.

    :return: None
    """
    print('I\'m sorry, I can\'t understand your query. Try again!\n')

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


    df = pd.DataFrame()
    try:
        for city_name in city:
            file_path = path.join(path.dirname(__file__), CITY_DATA[city_name])
            temp_df = pd.read_csv(file_path, parse_dates=['Start Time', 'End Time'])
            df = pd.concat([df, temp_df], ignore_index=True)

    except FileNotFoundError:
        print('I\'m sorry, but file for {} is not found. Please make sure that data files are in the same folder as '
              'file for this program. After that please restart the program!'.format(*city))
        exit()


    df['Month'] = df['Start Time'].dt.month
    df['Day of week'] = df['Start Time'].dt.dayofweek
    df['Start Hour'] = df['Start Time'].dt.hour


    if len(month) == 1:
        df = df.loc[df['Month'] == month[0]]


    if len(day) == 1:
        df = df.loc[df['Day of week'] == day[0]]


    return df


def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.

    :param df (pandas.DataFrame): DataFrame containing city data
    :param month (int): Number of the month used for filtering
    :param day (int): Number of the day of the week used for filtering
    :return: None
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if len(month) != 1:
        popular_month = df['Month'].mode()[0]
        popular_month_str = month_name[popular_month]
        # Creating a chart for months statistics
        popular_month_for_chart = df.groupby(['Month'])['Month'].count()
        popular_month_for_chart_labels = [month_name[i] for i in popular_month_for_chart.index]
        
        print('The most popular month was:', popular_month_str, '\n')

    # display the most common day of week
    if len(day) != 1:
        popular_dow = df['Day of week'].mode()[0]
        popular_dow_str = day_name[popular_dow]
        print('The most popular day of the week was:', popular_dow_str, '\n')
    
    # display the most common start hour
    start_hour_rating = df.groupby(['Start Hour'])['Start Hour'].count()
    print('The most popular hour for starting a route was:', df['Start Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    cutoff()


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    :param df (pandas.DataFrame): DataFrame containing city data
    :return: None
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most most commonly start station was:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most most commonly end station was:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_comb_stations = (df['Start Station'] + ' and ' + df['End Station']).mode()[0]
    print('The most frequent combination of start station and end station trip is:', popular_comb_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    cutoff()


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    :param df (pandas.DataFrame): DataFrame containing city data
    :return: None
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'], "s")
    # print(df['Trip Duration'])
    total_trip_time = df['Trip Duration'].sum()
    print('Total travel time is:', total_trip_time)

    # display mean travel time
    mean_trip_time = df['Trip Duration'].mean()
    print('Mean travel time is:', mean_trip_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    cutoff()


def user_stats(df, city):
    """
    Displays statistics on bikeshare users.
    :param df (pandas.DataFrame): DataFrame containing city data
    :return:
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users_types = df.groupby(['User Type']).count().iloc[:, 0:1]
    users_types.columns = ['User Type Count']
    users_types['User Type Percent'] = users_types/users_types.sum()*100
    print('User type statistics\n', users_types)
    cutoff()

    # Display counts of gender
    if city != ['washington']:
        if city == ['chicago', 'new york city', 'washington']:
            print('This statistics doesn\'t include users from Washington DC!')
        users_genders = df.groupby(['Gender']).count().iloc[:, 0:1]
        users_genders.columns = ['Count Users By Gender']
        users_genders['Percent Of Users By Genders'] = round((users_genders/users_genders.sum()*100), 2)
        print('Statistics based on users genders\n', users_genders)
        cutoff()

        # Display earliest, most recent, and most common year of birth
        year_of_birth = df['Birth Year'].dropna().astype(int)

        print('The earliest year of birth is:', min(year_of_birth))
        print('The most recent year is:', max(year_of_birth))
        print('The most common year is', year_of_birth.mode()[0])
        print()


        print("\nThis took %s seconds." % (time.time() - start_time))
        cutoff()

def row_data(df):
    """
    Displays row data from a DataFrame in batches.

    This function prompts the user to determine if they want to see the row data from a DataFrame.
    If the user chooses to proceed, they can specify the number of rows to display at a time.
    The function uses the pandas options to set the maximum number of rows and columns to display.

    :param df (pandas.DataFrame): The DataFrame containing the row data.

    :return: None
    """
    if input('Do you want to see row data? (Type "yes" or any other key)\nUser: ').lower() == 'yes':
        rows_qty = ''
        while not rows_qty.isdigit():
            rows_qty = input('\nHow many rows at the time do you want to see? (Please use only natural numbers)\nUser: ')
        rows_qty = int(rows_qty)
        key = input(f'Press "Enter" to print next {rows_qty} rows. Type any other key + "Enter" to stop quit printing.')
        x = 0
        y = rows_qty
        pd.set_option('display.max_rows', rows_qty)
        pd.set_option('display.max_columns', 10)
        pd.set_option('display.width', None)
        while not key:
            print(df.iloc[x:y, :-3])
            x += rows_qty
            y += rows_qty
            key = input()




def main():
    """
    The main function that controls the flow of the program.

    :return: None
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
