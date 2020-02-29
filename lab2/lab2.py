"""
Data cleaning
"""
import re
import pandas as pd
"""
Task 1
"""


def read_data(filename):
    """
    load the data frame from csv file
    :param filename: read the dataset from csv file
    :return: data frame
    """
    return pd.read_csv(filename)


def display_data(df, col=True, row=True):
    """
    display data
    :param df: data frame
    :param col: whether display column
    :param row: whether display row
    :return: nothing
    """
    if col:
        print(", ".join([c for c in df]))

    if row:
        for index, r in df.iterrows():
            print(", ".join([str(r[c]) for c in df]))


def count_nan(df):
    """
    count how many nan in each column
    fix: we need to count as percentage, so we need to fix
    what function we need:
        shape: df.shape[1] # number of col
            : df.shape[0] # number of row
    :param df: data from
    :return:
    """
    row_num = df.shape[0]
    for col in df:
        percentage = (int(df[col].isna().sum()) / row_num)*100
        print(col, ":", percentage, '%')


def drop_col(df, cols):
    """
    drop the columns
    :param df: data frame
    :param cols: the column need to drop
    :return:
    """
    df.drop(cols, axis=1, inplace=True)


"""
Task 2
"""


def replace_values(addr):
    """
    replace any value contain London with London
    replace - with space
    :param addr:
    :return:
    """
    addr = re.sub('.*London.*', 'London', addr)
    addr = addr.replace('-', ' ')
    return addr


def replace_place(df, col):
    """
    replace the place
    :param df: data frame
    :param col: which col need to fix
    :return:
    The answer code:
        df[col] = df[col].apply(
        lambda x: 'London' if 'London' in x else x.replace('-', ' '))
    """
    df[col] = df[col].apply(replace_values)
    return df


def keep_four_date(df):
    """
    Keep the first 4 digit number in "Date of Publication"
    :param df: data frame
    :return:
    """
    df['Date of Publication'] = pd.to_numeric(df['Date of Publication'].str.extract(r'(\d{4})', expand=False),
                                              downcast='integer')
    # pd.to_numeric(df['Date of Publication'])
    return df


def replace_nan_zero(df):
    """
    Replace NaN with 0 for the cells of "Date of Publication"
    :param df: data frame
    :return:
    """
    df['Date of Publication'] = df['Date of Publication'].fillna(0)
    return df


def store_csv(df):
    """
    store the data into csv file
    :param df:
    :return:
    """
    df.to_csv('res.csv', encoding='utf-8')


"""
task 3
"""


def replace_column(df):
    """
    replace the space in column with _
    :param df: data frame
    :return:
    """
    df.columns = [c.replace(' ', '_') for c in df.columns]
    return df


def query_pandas(df):
    """
    Filter the rows and only keep books which are published in "London" after 1866.
    :param df:
    :return:
    """
    df.query('Date_of_Publication > 1886 and Place_of_Publication == "London"')
    return df


def merge_data_frame(df1, df2):
    """
    merge two data frame on base on id
    :param df1: data frame 1
    :param df2: data frame 2
    :return:
    function:
        pandas.merge(df1, df2, how='left', left_on=['id_key'], right_on=['fk_key'])
    """
    return pd.merge(df1, df2, left_on='Place_of_Publication', right_on='City')


def group_data(df):
    """
    group the data
    :param df: data frame
    :return:
    function:
        df.groupby('Country', as_index=False).count()
    """
    return df.groupby('Country', ).count()


def task1():
    """
    run the task 1 functions
    :return:
    """
    print("####### Start task 1 ######")
    df = read_data('Books.csv')
    display_data(df)
    count_nan(df)
    col = [
        'Edition Statement',
        'Corporate Author',
        'Corporate Contributors',
        'Former owner',
        'Engraver',
        'Contributors',
        'Issuance type',
        'Shelfmarks'
    ]
    drop_col(df, col)
    display_data(df)


def task2():
    """
    run task 2 functions
    :return:
    """
    print("####### Start task 2 ######")
    df = read_data('Books.csv')
    replace_place(df, 'Place of Publication')
    display_data(df)
    df = keep_four_date(df)
    df = replace_nan_zero(df)
    display_data(df)
    return df


def task3():
    """
    run task3 functions
    :return:
    """
    print("####### Start task 3 ######")
    df = task2()
    df = replace_column(df)
    df = query_pandas(df)
    display_data(df)
    return df


def task4():
    """
    run task 4 functions
    :return:
    """
    print("####### Start task 4 ######")
    df = task3()
    city_df = read_data('City.csv')
    res = merge_data_frame(df, city_df)
    res = group_data(res)
    display_data(res)


if __name__ == '__main__':
    task1()
    task4()

