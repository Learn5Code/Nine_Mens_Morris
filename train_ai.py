import ast
import random
import os
import NN_ebsl
import Mill_for_AIs
import datetime


def complete_game_gen_score(network_white, network_black):
    board = Mill_for_AIs.place_stones(network_white, network_black)
    for zug in range(31):
        # 31 so it will be at most 80 moves before the game ends
        poss_moves = Mill_for_AIs.poss_move(board, 1)
        if len(poss_moves) == 0 or Mill_for_AIs.count_stones(board)[0] <= 2:
            # white loss
            return -1
        board_change = Mill_for_AIs.best_board(network_white, 1, poss_moves)[:]
        if Mill_for_AIs.three_line(board_change):
            if len(Mill_for_AIs.poss_takements(board, 1)) != 0:
                board = Mill_for_AIs.best_board_takeing(network_white, Mill_for_AIs.poss_takements(board, 1), 1)[:]
        else:
            board = board_change[0][:]
        poss_moves = Mill_for_AIs.poss_move(board, -1)[:]
        if len(poss_moves) == 0 or Mill_for_AIs.count_stones(board)[1] <= 2:
            return 1
        board_change = Mill_for_AIs.best_board(network_black, -1, poss_moves)[:]
        if Mill_for_AIs.three_line(board_change):
            if len(Mill_for_AIs.poss_takements(board, 1)) != 0:
                board = Mill_for_AIs.best_board_takeing(network_black, Mill_for_AIs.poss_takements(board, -1), -1)[:]
        else:
            board = board_change[0][:]
    return 0


def gen_fitness(list_of_nws, how_percise):
    rand_nws = []
    file = open("Trained Networks/Fitness Test/Networks", "r").readlines(-1)
    score = 0
    [a, b, c, d] = ast.literal_eval(file[0])
    list_of_nws = Mill_for_AIs.select_top(list_of_nws, how_percise / len(list_of_nws) * 100)
    for nw in file[1:how_percise + 1]:
        rand_nws.append(ast.literal_eval(nw))

    x = NN_ebsl.create_network(a, b, c, d)[0]
    for nw in rand_nws:
        nw.insert(0, x)

    for nw in rand_nws:
        for fight in list_of_nws:
            score += complete_game_gen_score(nw, fight)
            score -= complete_game_gen_score(fight, nw)
    return score / how_percise


def change_gen_fitness_nw(folder_name, gen_what, file_name):
    file = open("Trained Networks/" + folder_name + "/" + gen_what + "/" + file_name, "r").readlines(-1)
    list_file = []

    for line in file:
        list_file.append(ast.literal_eval(line))

    sorted_nws = [list_file[0]]

    for nw in Mill_for_AIs.select_top(list_file[1:], 100):
        sorted_nws.append(nw)

    open("Trained Networks/Fitness Test/Networks", "w+").write("[24, 1, 1, 1]\n")

    for nw in sorted_nws[1:]:
        open("Trained Networks/Fitness Test/Networks", "a").write(str(nw) + "\n")


def train_networks(network_proprieties, pop_size, num_macroevolution_gen, num_microevoultion_gen, safe_folder,
                   max_games_gen, percentage_old_macro=20, percentage_children=50, percentage_old_micro=5,
                   micro_error=5, changesize=0.25, from_gen=0, how_percise=5):
    print("start", datetime.datetime.now())
    # checks parameters and if they're not possible/sensible changes them
    if percentage_old_macro * pop_size // 100 < 1:
        percentage_old_macro = int(100 / pop_size) + 1
    if percentage_old_micro * pop_size // 100 < 1:
        percentage_old_micro = int(100 / pop_size) + 1
    if percentage_old_macro + percentage_children > 100:
        percentage_old_macro = 20
        percentage_children = 50
    if from_gen > 0:
        num_macroevolution_gen = 0
    if how_percise < 1:
        how_percise = 1
    if how_percise > 100:
        how_percise = 100
    # if folder "Trained Networks" doesn't exist, creates it
    try:
        os.mkdir("Trained Networks/")
    except OSError:
        pass

    try:
        os.mkdir("Trained Networks/" + str(safe_folder))
    except OSError:
        pass
    try:
        os.mkdir("Trained Networks/" + str(safe_folder) + "/gen_1")
        os.mkdir("Trained Networks/" + str(safe_folder) + "/gen_2")
    except OSError:
        pass

    all_proprieties = str(network_proprieties) + "\npopulation size: " + str(pop_size) + \
                      "\nhow many macro evolutions:" + str(num_macroevolution_gen) + "\nHow many micro evolutions:" \
                      + str(num_microevoultion_gen) + "\nHighest ammount of Games played generation:" + \
                      str(max_games_gen) + "\npercentage_old_macro:" + str(percentage_old_macro) + \
                      "\npercentage_children:" + str(percentage_children) + "\npercentage_old_micro:" + \
                      str(percentage_old_micro) + "\nMicro Error in percentages:" + str(micro_error) + \
                      "Change size during Microevolutions: " + str(changesize)
    if from_gen == 0:
        file = open("Trained Networks/" + str(safe_folder) + "/proprieties", "w+")
        file.write(all_proprieties)
        file.close()
    list_of_nw = []
    ip, layer, npl, op = network_proprieties[0], network_proprieties[1], network_proprieties[2], network_proprieties[3]
    if from_gen == 0:

        for new in range(pop_size):
            list_of_nw.append(NN_ebsl.create_network(ip, layer, npl, op))

        list_of_nw = Mill_for_AIs.findout_fitness(list_of_nw, max_games_gen)
        # save these networks
        file = open("Trained Networks/" + str(safe_folder) + "/gen_1/gen_1.0", "a+")
        file.write(str(network_proprieties) + "\n")
        file.close()
        for network in list_of_nw:
            NN_ebsl.safe_network(network[1:], "Trained Networks/" + str(safe_folder) + "/gen_1/gen_1.0")
        from_gen_macro = from_gen_micro = 0
    else:
        if from_gen > 0:
            from_gen_num = "2."
            from_gen_macro = num_macroevolution_gen
            from_gen_micro = from_gen
            safe_folder2 = "/gen_2"

        else:
            from_gen_num = "1."
            from_gen_macro = -from_gen
            from_gen_micro = 0
            from_gen *= -1
            safe_folder2 = "/gen_1"

        try:
            list_file = open("Trained Networks/" + safe_folder + safe_folder2 + "/gen_" + from_gen_num +
                             str(from_gen), "r").readlines(-1)
        except FileNotFoundError:
            print("Stupid ass nigga! You can't even write the right name of a file. GO COMMIT DIE!")
            return

        props = ast.literal_eval(list_file[0])
        x = NN_ebsl.create_network(props[0], props[1], props[2], props[3])
        for network in range(1, len(list_file)):
            list_of_nw.append(ast.literal_eval(list_file[network]))
            list_of_nw[network - 1].insert(0, x[0])
            list_of_nw[network - 1][-1] = [0]

    # macroevolution
    nw_prev_gen = list_of_nw
    for gen in range(from_gen_macro + 1, num_macroevolution_gen + 1):
        # selcts the best out of the old generation
        nw_current_gen = Mill_for_AIs.select_top(nw_prev_gen, percentage_old_macro)
        for network_index in range(len(nw_current_gen)):
            nw_current_gen[network_index][-1] = [0]
        # make their children         hehehe
        for i in range(2, int(2 + (-3 + (9 + 24 * percentage_children / 100 * pop_size) ** 0.5) / 6)):
            for k in range(1, i):
                for network in NN_ebsl.combine_networks(nw_prev_gen[k], nw_prev_gen[i], 3):
                    nw_current_gen.append(network)

        # create random networks
        while len(nw_current_gen) < pop_size:
            nw_current_gen.append(NN_ebsl.create_network(ip, layer, npl, op))

        nw_prev_gen = Mill_for_AIs.findout_fitness(nw_current_gen, max_games_gen)
        # save these networks
        file = open("Trained Networks/" + str(safe_folder) + "/gen_1/gen_1." + str(gen), "a")
        file.write(str(network_proprieties) + "\n")
        file.close()
        for network in nw_prev_gen:
            NN_ebsl.safe_network(network[1:], "Trained Networks/" + str(safe_folder) + "/gen_1/gen_1." + str(gen))

        gen_score_file = open("Trained Networks/" + str(safe_folder) + "/Generation Fitness", "a")
        gen_score_file.write("gen 1." + str(gen) + ": " + str(gen_fitness(nw_current_gen, how_percise)) + "\n")

        print("macroevolution", gen, "done ", datetime.datetime.now())
        nw_prev_gen = nw_current_gen[:]
    print("Macroevolutions Done\n")

    # microevolution
    for gen in range(from_gen_micro + 1, num_microevoultion_gen + 1):
        nw_current_gen = Mill_for_AIs.select_top(nw_prev_gen, percentage_old_micro)
        for network_index in range(len(nw_current_gen)):
            nw_current_gen[network_index][-1] = [0]

        # apply small changes to individual networks
        how_many = int((pop_size - len(nw_current_gen)) / percentage_old_micro)
        for network_index in range(len(nw_current_gen)):
            for i in range(how_many // len(nw_current_gen)):
                nw_current_gen.append(NN_ebsl.micro_evolution(nw_current_gen[network_index],
                                                              micro_error, changesize)[:])

        # while the population size is too small
        while len(nw_current_gen) < pop_size:
            network_index = random.randint(0, int(percentage_old_micro / 100 * pop_size) - 1)
            nw_current_gen.append(NN_ebsl.micro_evolution(nw_current_gen[network_index], micro_error, changesize)[:])

        nw_prev_gen = Mill_for_AIs.findout_fitness(nw_current_gen, max_games_gen)
        # save networks
        open("Trained Networks/" + str(safe_folder) + "/gen_2/gen_2." + str(gen), "a")\
            .write(str(network_proprieties) + "\n")
        for network in nw_prev_gen:
            NN_ebsl.safe_network(network[1:], "Trained Networks/" + str(safe_folder) + "/gen_2/gen_2." + str(gen))

        gen_score_file = open("Trained Networks/" + str(safe_folder) + "/Generation Fitness", "a")
        gen_score_file.write("gen 2." + str(gen) + ": " + str(gen_fitness(nw_current_gen, how_percise)) + "\n")

        print("Microevolution", gen, "Done", datetime.datetime.now())
        nw_prev_gen = nw_current_gen
    print("Microevolutions Done")


"""network_proprieties = [inputs, num_layer, neurons_pro_layer, num_outputs] 
   pop_size = howw many networks are in one generation
   num_macroevolution_gen = how many generations of macroevolutions are done 
   num_microevoultion_gen = how many generations of microevolutions are done
   safe_folder = string with the name of the folder
   max_games_gen = how many games are played at most in one generation 
   percentage_old_macro = what percentage of the previous generation remains the same/ 
                          continues living in the following gen
   percentage_children = what percentage of the new generation are children 
   percentage_old_micro = what percentage of the previous generation remains the same/ 
                          continues living in the following gen
   micro_error = the probability for changes during the microevolution 
   changesize = how the big the difference between new weights and biases are during micro evolution
   from_gen = negative number (-71) = macro gen number (1.71), positive number (71) = micro gen number (2.71) 
   how_percise = how many games are played to find out the fitness from the generation"""

nw_proprieties = [24, 2, 40, 1]
population_size = 500
howmany_macroevolutions = 10
howmany_microevolutions = 100
folder = "First Mill AI"
games_per_generation = 20000

train_networks(nw_proprieties, population_size, howmany_macroevolutions, howmany_microevolutions, folder,
               games_per_generation)
# change_gen_fitness_nw("First Mill AI", "gen_2", "gen_2.100")
