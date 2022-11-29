import pandas as pd
import matplotlib.pyplot as plt
from art import *


def read_data(file):
    data = pd.read_csv(file)
    return data


def read_data_dict(filename, type_cast_dict={}):
    """
    Reads in the data in a given file
    and stores the values in a list of dicts of strings (by default).
    Assumes that commas separate row items in the given file.

    Parameters
    ----------
    filename : string
        name of the file

    type_cast_dict: dict, optional
        type specification for each column in the data
    Returns
    -------
    data : list of dicts
        list of dicts of values for all lines in the file
    """
    file = open(filename, "r")
    data = []

    headers = file.readline()
    headers = headers.strip().split(",")

    for line in file:
        pieces = line.strip().split(",")

        row_dict = {}
        # go through each column and link the value
        # to the appropriate header
        for i in range(len(pieces)):

            if headers[i] in type_cast_dict:
                cast_func = type_cast_dict[headers[i]]
                row_dict[headers[i]] = cast_func(pieces[i])
            else:
                row_dict[headers[i]] = pieces[i]

        data.append(row_dict)

    file.close()
    return data


def clean_vax():
    # cleans the vaccine dataset, pulling out the most recent data values for people vaxinated per 100 people for
    # each state returns it as a series
    people_vax_ph = []
    data = read_data_dict("us_state_vaccinations.csv")
    us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
                 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York State',
                 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
                 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                 'West Virginia', 'Wisconsin', 'Wyoming']
    for dict in data:
        if dict["date"] == "2022-11-02" and dict["location"] in us_states:
            people_vax_ph.append(float(dict["people_vaccinated_per_hundred"]))
    vaxS = pd.Series(people_vax_ph)
    return vaxS


def clean_test():
    # cleans the standardized testing dataset by pulling out all the average scores for each state
    # returns it as a series
    us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
                 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
                 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
                 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                 'West Virginia', 'Wisconsin', 'Wyoming']
    scores = []
    data = read_data_dict("SPCsv202211080904.csv")
    for dict in data:
        if dict["Jurisdiction"] in us_states:
            scores.append(int(dict["MN"]))
    scoreS = pd.Series(scores)
    return scoreS


def chart():
    # combines the vaccine and test series into a dataframe
    test_series = clean_test()
    vaccine_series = clean_vax()
    frame = {'Average Scores on Standardized English Test': test_series,
             'People Vaccinated Per Hundred': vaccine_series}
    df = pd.DataFrame(frame)
    print(df.to_string())
    return df

def plot(dataframe):
    dataframe.plot.scatter(x='Average Scores on Standardized English Test', y='People Vaccinated Per Hundred', c='DarkBlue')
    plt.show()

def main():
    print(text2art("DS2001    FINAL    PROJECT"))
    df = chart()
    plot(df)


main()
