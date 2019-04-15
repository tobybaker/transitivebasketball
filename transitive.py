# Submission for fivethirtyeight's Riddler Classic 12/04/19
# https://fivethirtyeight.com/features/how-many-times-a-day-is-a-broken-clock-right/

import matplotlib.pyplot as plt


def get_teams_from_line(line):
    # remove home team specification
    line = line.replace("@", " ")
    # split according to multiple spaces
    tokens = line.split("  ")
    # remove any empty entries in the list
    tokens = list(filter(lambda element: element != "",  tokens))
    return tokens[1], tokens[3]


# generate a dict of lists of teams each key team has lost to
def generate_losing_dict(filepath):
    file = open(filepath, 'r')

    losing_dict = {}
    for line in file:

        winning_team, losing_team = get_teams_from_line(line)
        # adding winning team to list of teams the loser has lost to
        if losing_team not in losing_dict.keys():
            losing_dict[losing_team] = [winning_team]
        else:
            losing_dict[losing_team].append(winning_team)

    file.close()
    return losing_dict


# produce a single set of all teams
def get_all_teams(filepath):
    file = open(filepath, 'r')

    all_teams = set()
    for line in file:
        winning_team, losing_team = get_teams_from_line(line)
        all_teams.add(winning_team)
        all_teams.add(losing_team)

    file.close()

    return all_teams


def collapse_transitive_layers(transitive_layers):
    return_set = set()
    for layer in transitive_layers:
        return_set.update(layer)
    return return_set


def generate_transitive_victories(losing_dict, champion):
    all_transitive_teams = set()

    transitive_layers = []

    # first layer (the actual champion)
    transitive_layers.append([champion])

    # tracking the layer that we should find we lose to
    previous_layer = 0

    # continue looping until all possible transitive victors found
    while True:
        current_layer_winners = []

        all_transitive_teams_length = len(all_transitive_teams)

        # for all transitive victors in the previous layer
        for winner in transitive_layers[previous_layer]:

            # if transitive victor has recorded losses
            if winner in losing_dict.keys():

                # add victor of losses to current transitive layer
                # if it has not been seen before
                for next_winner in losing_dict[winner]:
                    if next_winner not in all_transitive_teams:
                        current_layer_winners.append(next_winner)
                        all_transitive_teams.add(next_winner)

        # if current layer does not add any more victors all have been found
        if all_transitive_teams_length == len(all_transitive_teams):
            return transitive_layers

        transitive_layers.append(current_layer_winners)
        previous_layer += 1


def get_transitive_lengths(transitive_layers):
    return_list = []
    for layer in transitive_layers:
        return_list.append(len(layer))
    return return_list


def plot_transitive_layers(transitive_layers, filename, title, bar_colour="green"):
    transitive_lengths = get_transitive_lengths(transitive_layers)
    layer_range = range(len(transitive_lengths))
    plt.bar(layer_range, transitive_lengths, color=bar_colour, edgecolor="black")
    plt.title(title)
    plt.xlabel("Transitive Victory Separation")
    plt.ylabel("Number of Winners")
    plt.xticks(range(9))
    plt.savefig("figs/"+filename)

if __name__ == "__main__":
    data_filepath = 'menbasketball2018.txt'
    champion_team = 'Virginia'

    all_teams = get_all_teams(data_filepath)

    losing_dict = generate_losing_dict(data_filepath)

    transitive_layers = generate_transitive_victories(losing_dict, champion_team)

    transitive_victors = collapse_transitive_layers(transitive_layers)

    not_transitive_victors = all_teams.difference(transitive_victors)

    print("Teams that are not Transitive Winners :", len(not_transitive_victors))
    print("Total Number of Teams : ", len(all_teams))

    plot_title = "Men's NCAA Championship"
    plot_output_file = "mensbasketball.png"
    plot_transitive_layers(transitive_layers, plot_output_file, plot_title)
