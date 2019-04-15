import transitive

def generate_losing_dict_from_test(filepath):
    file = open(filepath, 'r')

    losing_dict = {}
    for line in file:
        line = line.replace("\n","")
        tokens = line.split(",")
        winning_team, losing_team = tokens[0],tokens[1]
        # adding winning team to list of teams the loser has lost to
        if losing_team not in losing_dict.keys():
            losing_dict[losing_team] = [winning_team]
        else:
            losing_dict[losing_team].append(winning_team)

    file.close()
    return losing_dict

data_filepath = "testset.txt"
champion_team = "A"
losing_dict = generate_losing_dict_from_test(data_filepath)
print(losing_dict)
transitive_layers = transitive.generate_transitive_victories(losing_dict, champion_team)
print(transitive_layers)
