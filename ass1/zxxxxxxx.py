import ast
import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

studentid = os.path.basename(sys.modules[__name__].__file__)


#################################################
# Your personal methods can be here ...
def get_chars(chars):
    chars = ast.literal_eval(chars)
    result = []
    for ch in chars:
        result.append(ch['character'])
    result = sorted(result)
    return ", ".join(result)
#################################################


def log(question, output_df, other):
    print("--------------- {}----------------".format(question))
    if other is not None:
        print(question, other)
    if output_df is not None:
        print(output_df.head(5).to_string())


def question_1(movies, credits):
    """
    :param movies: the path for the movie.csv file
    :param credits: the path for the credits.csv file
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df1 = pd.merge(pd.read_csv(movies), pd.read_csv(credits), on='id')
    #################################################

    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df2 = df1.copy()
    keeps = ['id', 'title', 'popularity', 'cast', 'crew', 'budget', 'genres',
             'original_language', 'production_companies', 'production_countries',
             'release_date', 'revenue', 'runtime', 'spoken_languages', 'vote_average',
             'vote_count']
    for col in df2:
        if col not in keeps:
            df2.drop(columns=col, axis=1, inplace=True)

    #################################################

    log("QUESTION 2", output_df=df2, other=(len(df2.columns), sorted(df2.columns)))
    return df2


def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df3 = df2.copy()
    df3.set_index('id', inplace=True)
    #################################################

    log("QUESTION 3", output_df=df3, other=df3.index.name)
    return df3


def question_4(df3):
    """
    :param df3: the dataframe created in question 3
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df4 = df3.copy()
    df4 = df4[df4['budget'] != 0]
    #################################################

    log("QUESTION 4", output_df=df4, other=(df4['budget'].min(), df4['budget'].max(), df4['budget'].mean()))
    return df4


def question_5(df4):
    """
    :param df4: the dataframe created in question 4
    :return: df5
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df5 = df4.copy()
    df5['success_impact'] = ((df5['revenue'] - df5['budget']) / df5['budget'])
    #################################################

    log("QUESTION 5", output_df=df5,
        other=(df5['success_impact'].min(), df5['success_impact'].max(), df5['success_impact'].mean()))
    return df5


def question_6(df5):
    """
    :param df5: the dataframe created in question 5
    :return: df6
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df6 = df5.copy()
    max_popu = df6['popularity'].max()
    min_popu = df6['popularity'].min()
    df6['popularity'] = ((df6['popularity'] - min_popu) / (max_popu - min_popu)) * 100
    df6['popularity'] = pd.to_numeric(df6['popularity'], downcast='float')
    #################################################

    log("QUESTION 6", output_df=df6, other=(df6['popularity'].min(), df6['popularity'].max(), df6['popularity'].mean()))
    return df6


def question_7(df6):
    """
    :param df6: the dataframe created in question 6
    :return: df-
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df7 = df6.copy()
    df7['popularity'] = df7['popularity'].astype('int16')
    #################################################

    log("QUESTION 7", output_df=df7, other=df7['popularity'].dtype)
    return df7


def question_8(df7):
    """
    :param df7: the dataframe created in question 7
    :return: df8
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df8 = df7.copy()
    df8.cast = df8.cast.apply(get_chars)
    #################################################

    log("QUESTION 8", output_df=df8, other=df8["cast"].head(10).values)
    return df8


def question_9(df8):
    """
    :param df9: the dataframe created in question 8
    :return: movies
            Data Type: List of strings (movie titles)
            Please read the assignment specs to know how to create the output
    """

    #################################################
    # Your code goes here ...
    df9 = df8.copy()
    df9['characters_num'] = [len(chars.split(',')) for chars in df9['cast']]
    df9 = df9.sort_values(by='characters_num', ascending=False)
    movies = [row['title'] for index, row in df9.head(10).iterrows()]
    #################################################
    # we do not want to change the df8 data frame, so we copy one

    log("QUESTION 9", output_df=None, other=movies)
    return movies


def question_10(df8):
    """
    :param df8: the dataframe created in question 8
    :return: df10
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df10 = df8.copy()
    df10['release_date'] = pd.to_datetime(df10['release_date'], format='%d/%m/%Y', errors='ignore')
    df10.sort_values(by='release_date', ascending=False, inplace=True)
    # convert the date format into the origin one
    df10['release_date'] = df10['release_date'].apply(lambda x: x.strftime('%d/%m/%Y'))
    #################################################

    log("QUESTION 10", output_df=df10, other=df10["release_date"].head(5).to_string().replace("\n", " "))
    return df10


def question_11(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    fig, axes = plt.subplots()
    df11 = df10.copy()
    # we can get all the genres firstly, and apply
    genres = []
    for tuples in df11.genres:
        for g in ast.literal_eval(tuples):
            genres.append(g['name'])
    genreDF = pd.Series(genres)
    genres_data = genreDF.value_counts()
    genres_data.plot.pie(autopct='%1.1f%%', figsize=(20, 20), title='Genres', label='', legend=True)
    #################################################

    plt.savefig("{}-Q11.png".format(studentid))


def question_12(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    fig, axes = plt.subplots()
    df12 = df10.copy()
    df12['production_countries'] = df12['production_countries'].apply(
        lambda x: [c['name'] for c in ast.literal_eval(x)])

    data = []
    for i in df12['production_countries']:
        for j in i:
            data.append(j)
    df = pd.DataFrame({'country': data})

    country_data = df['country'].value_counts().sort_index()
    country_data.plot.bar(figsize=(20, 20), title='Production country')
    #################################################

    plt.savefig("{}-Q12.png".format(studentid))


def question_13(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    fig, axes = plt.subplots()
    df13 = df10.copy()
    groups = df13.groupby('original_language')
    random_color = plt.cm.get_cmap('hsv', len(groups) + 1)
    ax = None
    index = 0
    for name, group in groups:
        if ax is None:
            ax = group.plot.scatter(x='vote_average', y='success_impact', label=name, ax=axes,
                                    color=random_color(index), figsize=(10, 10))
        else:
            ax = group.plot.scatter(x='vote_average', y='success_impact', label=name, ax=ax,
                                    color=random_color(index), figsize=(10, 10))
        index += 1
    #################################################

    plt.savefig("{}-Q13.png".format(studentid))


if __name__ == "__main__":
    df1 = question_1("movies.csv", "credits.csv")
    df2 = question_2(df1)
    df3 = question_3(df2)
    df4 = question_4(df3)
    df5 = question_5(df4)
    df6 = question_6(df5)
    df7 = question_7(df6)
    df8 = question_8(df7)
    movies = question_9(df8)
    df10 = question_10(df8)
    question_11(df10)
    question_12(df10)
    question_13(df10)
