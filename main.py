import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

US_STATES = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
             'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
             'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
             'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York State',
             'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
             'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
             'West Virginia', 'Wisconsin', 'Wyoming']


def read_data(file):
    # reads in the data from the csv file
    data = pd.read_csv(file)
    return data


def read_data_dict(filename, type_cast_dict={}):
    # reads in the data from the csv file
    # returns a list of dictionaries
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
    for dict in data:
        if dict["date"] == "2022-11-02" and dict["location"] in US_STATES:
            people_vax_ph.append(float(dict["people_vaccinated_per_hundred"]))
    vaxS = pd.Series(people_vax_ph)
    return vaxS


def date_vax_per_state(state):
    # returns a series of the number of people vaccinated per hundred for a given state
    data = read_data_dict("us_state_vaccinations.csv")
    vax_per_state = []
    for dict in data:
        if dict["location"] == state:
            if dict["people_vaccinated_per_hundred"] != "":
                vax_per_state.append({"date": dict["date"],
                                      "people_vaccinated_per_hundred": float(dict["people_vaccinated_per_hundred"])})
    return vax_per_state


def test_per_state():
    # returns a list of the average scores on the standardized english test for each state
    data = read_data_dict("SPCsv202211080904.csv")
    states = []
    scores = []
    for dict in data:
        for state in US_STATES:
            if dict["Jurisdiction"] == state:
                states.append(state)
                scores.append(int(dict["MN"]))
    return states, scores


def plot_states_vax():
    # plot the data for every state in the US in one graph
    i = 0
    states = []
    plt.figure(figsize=(8, 6))
    for state in US_STATES:
        vax_per_state = date_vax_per_state(state)
        dates = []
        vax_per_hundred = []
        for dict in vax_per_state:
            dates.append(np.datetime64(dict["date"]))
            vax_per_hundred.append(dict["people_vaccinated_per_hundred"])
        plt.plot(dates, vax_per_hundred, label=state)
        i = i + 1
        states.append(state)
        if i == 5:
            plt.legend()
            plt.title("People Vaccinated Per Hundred in the US for " + states[0] + " to " + states[len(states) - 1])
            plt.savefig(states[0] + " to " + states[len(states) - 1] + " Vaccination Percentage.png", dpi=300)
            plt.show()
            states = []
            i = 0


def plot_states_test():
    # plot the data for every state in the US in multiple graphs as groups of 5
    states, scores = test_per_state()
    states_chunks = [states[x:x + 5] for x in range(0, len(states), 5)]
    scores_chunks = [scores[x:x + 5] for x in range(0, len(scores), 5)]
    print(states_chunks)
    i = 0
    for chunk in states_chunks:
        plt.figure(figsize=(8, 6))
        plt.bar(chunk, scores_chunks[i])
        plt.ylim([min(scores_chunks[i]) - 10, max(scores_chunks[i]) + 10])
        plt.title("Average Scores on Standardized English Test for " + chunk[0] + " to " + chunk[len(chunk) - 1])
        plt.savefig(chunk[0] + " to " + chunk[len(chunk) - 1] + " Average Scores on Standardized English Test.png",
                    dpi=300)
        plt.show()
        i = i + 1


def clean_test():
    # cleans the standardized testing dataset by pulling out all the average scores for each state
    # returns it as a series
    scores = []
    data = read_data_dict("SPCsv202211080904.csv")
    for dict in data:
        if dict["Jurisdiction"] in US_STATES:
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
    # plots the data from the dataframe
    plt.figure(figsize=(8, 6))

    annotations = US_STATES
    dataframe.plot.scatter(x='Average Scores on Standardized English Test', y='People Vaccinated Per Hundred',
                           c='DarkBlue')
    for i, label in enumerate(annotations):
        plt.annotate(label, (
            dataframe["Average Scores on Standardized English Test"][i], dataframe['People Vaccinated Per Hundred'][i]))
    plt.title("Standardized English Test Scores vs. People Vaccinated Per Hundred")
    plt.savefig("Average Scores on Standardized English Test vs. People Vaccinated Per Hundred.png", dpi=300)
    plt.show()


def main():
    # main function, runs all the functions
    df = chart()
    plot(df)
    plot_states_vax()
    plot_states_test()


if __name__ == "__main__":
    main()
