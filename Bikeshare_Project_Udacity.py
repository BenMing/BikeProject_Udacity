#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import pandas as pd
import numpy as np

from input_func import get_user_input

city_data = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

cities = ['chicago', 'new york', 'washington']

months = ['january', 'february', 'march', 'april', 'may', 'june']

days = ['sunday', 'monday', 'tuesday', 'wednesday', \
        'thursday', 'friday', 'saturday' ]

def get_filters():
    """
    要求用户数据想要查询的城市、月份、星期几。
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("欢迎探索美国共享单车数据集")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("你希望查看哪个城市？Chicago, New York 还是 Washington？\n> ").lower()
        if city in cities:
            break
        else:
            print("我不太懂你说的是哪个城市。")

    # get user input for month (all, january, february, ... , june)
    month = get_user_input("你想查看哪个月份？请从 January, February, March, April, May, June 中进行选择，"
                           "输入 all 选择所有月份。\n> ", months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_input("你希望查看星期几？请从 Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday 中进行选择。"
                         "若不想选特定某天，请输入 all .\n> ", days)

    return city, month, day

def load_data(city, month, day):
    """
    根据用户输入，筛选 DataFrame
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(city_data[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]


    return df

def time_stats(df):
    """展示共享单车用户使用人数最多的时间段。"""

    print('\n共享单车使用的时间相关信息\n')

    # display the most common month
    most_common_month = df['Month'].value_counts().idxmax()
    print("1~6月，骑共享单车的人最多的是：", most_common_month, "月.")

    # display the most common day of week
    most_common_day = df['Day of Week'].value_counts().idxmax()
    print("一周中，骑共享单车的人最多的一天是：", most_common_day, ".")

    # display the most common start hour
    most_common_hour = df['Hour'].value_counts().idxmax()
    print("一天24小时中，最多人在", most_common_hour, "点.")


    print('-'*40)


def station_stats(df):
    """展示最常见的起点和终点."""

    print('\n行程相关信息\n')

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("最热门的起始站点是： ", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("最热门的终点是： ", most_common_end_station)

    # display most frequent combination of start station and end station trip
    trip_series = df["Start Station"].astype(str) + " >>> " + df["End Station"].astype(str)
    trip_series.describe()
    most_popular_trip = trip_series.describe()["top"]
    print("最热门的行程是： ", most_popular_trip)

    print('-'*40)

def trip_duration_stats(df):
    """展示骑行时间相关信息"""

    print('\n骑行时间相关信息\n')

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("总骑行时间是： ", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("平均骑行时间是： ", mean_travel_time)

    # display max travel time
    max_travel_time = df['Trip Duration'].max()
    print("时间最长的一段骑行是： ", max_travel_time)

    print('-'*40)

def user_stats(df):
    """展示用户类型相关信息"""

    print('\n用户类型相关信息\n')

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print("所有用户类型与数量如下所示：\n", user_type_counts)

    print('-'*40)

def user_stats_gender(df):
    """展示用户性别相关信息"""

    print('\n用户性别相关信息\n')

    # Washington.csv 没有 Gender 和 Birth Year
    try:
        gender_col = df['Gender']

    except KeyError:
        print("此数据集没有出生年份相关信息")

    else:
        # Display counts of gender
        user_gender_counts = gender_col.value_counts()
        print("用户性别与数量如下所示：\n", user_gender_counts)

        # 展示 NaN 数量
        gender_isna = gender_col.isna().sum()
        print("性别信息不详的用户数量为： ", gender_isna)

    print('-'*40)


def user_stats_birth(df):
    """展示用户的年龄相关信息"""

    print("\n用户的年龄相关信息\n")

    # Washington.csv 没有 Gender 和 Birth Year
    try:
        birth_year = df['Birth Year']

    except KeyError:
        print("此数据集没有出生年份相关信息")

    else:
        # the most common birth year
        most_common_birth_year = birth_year.value_counts().idxmax()
        print("出生年份最常见的一年是： ", most_common_birth_year)

        # the most recent birth year
        most_recent_birth_year = birth_year.max()
        print("出生年份最晚的一年是： ", most_recent_birth_year)

        # the earliest birth year
        earliest_birth_year = birth_year.min()
        print("出生年份最早的一年是： ", earliest_birth_year)

    print('-'*40)

def table_stats(df, city):
    """数据集元信息"""

    print("\n数据集元信息\n")

    # counts the number of missing values in the entire dataset
    missing_values_counts = df.isnull().sum().sum()
    print("所选城市 {} 数据集，缺少数据的项的数量为 : {}".format(city, missing_values_counts))

    # counts the number of missing values in the User Type column
    non_usertype_counts = df['User Type'].isnull().sum().sum()
    print("User Type 一列的空数据项为 : {}".format(non_usertype_counts))


    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        user_stats_gender(df)
        user_stats_birth(df)

        table_stats(df, city)

        restart = input('\n是否需要重新开始，请输入 yes 或者 no。\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
