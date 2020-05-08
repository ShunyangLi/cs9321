"""
Name: assign3.py
Author: Shunyang Li
Time: 2020/4/5

get data and clean data and do machine learning
"""
import ast
import sys
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score, accuracy_score, recall_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def extract_data(df):
    """
    convert the json to list
    :param df: data frame
    :return:
        the data frame after decode the json
    """
    data = df.copy()

    def extract_values(x):
        """
        the cast too much, so we may only need top 6 members
        :param x: the data x
        :return: list of cast
            return a list
        """
        x = ast.literal_eval(x)
        values = []
        if isinstance(x, list):
            for i in x:
                if len(values) < 1:
                    values.append(i["name"])
                else:
                    break
        return ",".join(values)

    cols = ['cast', 'crew', 'genres', 'production_companies']
    for col in cols:
        data[col] = data[col].apply(extract_values)

    # drop null value
    data = data.dropna()

    # try to add more columns and try to get some idea
    casts = []
    for cast in data['cast']:
        cast = str(cast).split(",")
        for c in cast:
            if c not in casts:
                casts.append(c)
    for cast in casts:
        temp = []
        for ca in data['cast']:
            if cast in str(ca).split(","):
                temp.append(1)
            else:
                temp.append(0)
        cast = cast.replace(" ", "_")
        data[cast] = pd.Series(temp)

    crews = []
    for crew in data['crew']:
        crew = str(crew).split(",")
        for c in crew:
            if c not in crews:
                crews.append(c)

    for crew in crews:
        temp = []
        for ca in data['crew']:
            if crew in str(ca).split(","):
                temp.append(1)
            else:
                temp.append(0)
        crew = crew.replace(" ", "_")
        data[crew] = pd.Series(temp)

    genres = []
    for genre in data['genres']:
        genre = str(genre).split(",")
        for c in genre:
            if c not in genres:
                genres.append(c)

    for genre in genres:
        temp = []
        for gen in data['genres']:
            if genre in str(gen).split(","):
                temp.append(1)
            else:
                temp.append(0)
        genre = genre.replace(" ", "_")
        data[genre] = pd.Series(temp)

    data['production_companies'] = data['production_companies'].apply(lambda x: str(x).split(",")[0])
    # data.append(cast_frame, ignore_index=True)
    # data.append(crew_frame, ignore_index=True)
    # data.append(genre_frame, ignore_index=True)
    data['original_language'] = LabelEncoder().fit_transform(data['original_language'])
    data['production_companies'] = LabelEncoder().fit_transform(data['production_companies'])
    data = data.drop(columns=['cast', 'crew', 'genres'])

    return data


def load_data(filename):
    """
    use pandas to load a csv file
    and we need to clean the data by
    :param filename: filename
    :return:
        data frame
    """
    df = pd.read_csv(filename)

    # drop the useless columns
    cols = ['homepage', 'tagline', 'production_countries', 'spoken_languages', 'status',
            'original_title', 'overview', 'rating', 'release_date', 'keywords']
    df = df.drop(columns=cols)

    # drop none values, and clean revenue if the revenue is 0
    # because revenue is y label can not be 0
    df = df.dropna()
    df = df[df.revenue != 0]

    # make all the date with same format
    # df.release_date = pd.to_datetime(df.release_date, errors='ignore', unit='s')
    # df.release_date = df['release_date'].apply(lambda x: "".join([i for i in str(x).split("-")]))
    # then convert the cast, crew, production_companies and genre columns
    df = extract_data(df)

    return df


if __name__ == '__main__':
    # check how many args
    if len(sys.argv) < 3:
        print("The command line should like: python3 z{id}.py path1 path2")
        sys.exit()

    train = load_data(sys.argv[1])
    test = load_data(sys.argv[2])

    y_train = train['revenue'].values
    x_train = train.drop(columns=['revenue'])

    y_test = test['revenue'].values
    x_test = test.drop(columns=['revenue'])
    print(x_train.shape, x_test)

    ln = LinearRegression()
    ln.fit(x_train, y_train)
    prediction = ln.predict(x_test)
    score = r2_score(y_test, prediction)
    print("prediction: ", prediction)
    print("accuracy: ", score)
    print("MSE: ", mean_squared_error(y_test, prediction))

    # knn = KNeighborsClassifier()
    # knn.fit(x_train, y_train)
    #
    # # predict the test set
    # predictions = knn.predict(x_test)
    # print("accuracy: ", accuracy_score(y_test, predictions))







