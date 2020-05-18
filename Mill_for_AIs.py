import Mill_humans
import NN_ebsl
import random


def possible_boards_placing(board, placer):
    poss_boards_change = []
    for place in range(24):
        if board[place] == 0:
            board[place] = placer
            poss_boards_change.append([board[:], place])
            board[place] = 0
    return poss_boards_change


def best_board(network, high_low, poss_boards_change):
    final_board_change = [poss_boards_change[0][0], poss_boards_change[0][1],
                          NN_ebsl.calculate_output(network, poss_boards_change[0][0])[:]]
    if high_low == 1:
        for board_change in poss_boards_change[1:]:
            x = [NN_ebsl.calculate_output(network, board_change[0])[:]]
            if final_board_change[2][0] < x[0][0]:
                final_board_change = [board_change[0], board_change[1], x[0][:]]
    else:
        for board_change in poss_boards_change[1:]:
            x = [NN_ebsl.calculate_output(network, board_change[0])[:]]
            if final_board_change[2][0] > x[0][0]:
                final_board_change = [board_change[0], board_change[1], x[0][:]]
    return final_board_change


def best_board_takeing(network, board_list, taker):
    # adds 1 fitness score to the network
    network[3][0] += 1
    return_board = [board_list[0], NN_ebsl.calculate_output(network, board_list[0])]
    for board in board_list[1:]:
        x = NN_ebsl.calculate_output(network, board)
        if x * taker > return_board[1]:
            return_board = [board[:],  x[:]]
    return return_board[0]


def three_line(board_change):
    # nexus[place on field][row, column][both other places in this row]
    # it has a place with a change and it checks the row and column connected to this place
    board, change = board_change[0], board_change[1]
    nexus = Mill_humans.nexus
    for line in [0, 1]:
        if board[change] == board[nexus[change][line][0]] == board[nexus[change][line][1]]:
            return True
    return False


def poss_takements(board, taker):
    poss_boards = []
    for place in range(len(board)):
        if board[place] == -1 * taker:
            if not three_line([board, place, 0]):
                board[place] = 0
                poss_boards.append(board[:])
                board[place] = -1 * taker
    if len(poss_boards) == 0:
        return [board]
    return poss_boards


def poss_move(board, who):
    # returns possible list as [[board], change]
    poss_boards_change = []
    connected_points = Mill_humans.connected_points
    if who == 1:
        player = 0
    else:
        player = 1
    if count_stones(board)[player] == 3:
        for stone in range(len(board)):
            if board[stone] == who:
                for to in range(len(board)):
                    if board[to] == 0:
                        board[stone] = 0
                        board[to] = who
                        poss_boards_change.append([board[:], to])
                        board[stone] = who
                        board[to] = 0
    else:
        for stone in range(len(board)):
            if board[stone] == who:
                for to in connected_points[stone]:
                    if board[to] == 0:
                        board[stone] = 0
                        board[to] = who
                        poss_boards_change.append([board[:], to])
                        board[stone] = who
                        board[to] = 0
    return poss_boards_change


def count_stones(board):
    white = black = 0
    for stone in board:
        if stone == 1:
            white += 1
        elif stone == -1:
            black += 1
    return white, black


def place_stones(network_white, network_black):
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for double_placement in range(9):
        board_change = best_board(network_white, 1, possible_boards_placing(board, 1))[:]
        board = board_change[0][:]
        if three_line(board_change):
            board = best_board_takeing(network_white, poss_takements(board, 1), 1)
        else:
            board = board_change[0]
        board_change = best_board(network_black, -1, possible_boards_placing(board, -1))[:]
        board = board_change[0][:]
        if three_line(board_change):
            board = best_board_takeing(network_black, poss_takements(board, -1), -1)
        else:
            board = board_change[0][:]
    return board


def complete_game_pcs(network_white, network_black):
    board = place_stones(network_white, network_black)
    for zug in range(16):
        # 16 so it will be at most 50 moves before the game ends
        poss_moves = poss_move(board, 1)
        if len(poss_moves) == 0 or count_stones(board)[0] <= 2:
            network_black[3][0] += 5
            # print("black wins")
            break
        board_change = best_board(network_white, 1, poss_moves)[:]
        if three_line(board_change):
            if len(poss_takements(board_change[0], 1)) != 0:
                board = best_board_takeing(network_white, poss_takements(board_change[0][:], 1), 1)[:]
        else:
            board = board_change[0][:]
        poss_moves = poss_move(board, -1)[:]
        if len(poss_moves) == 0 or count_stones(board)[1] <= 2:
            network_white[3][0] += 5
            # print("white wins")
            break
        board_change = best_board(network_black, -1, poss_moves)[:]
        if three_line(board_change):
            if len(poss_takements(board_change[0], 1)) != 0:
                board = best_board_takeing(network_black, poss_takements(board_change[0][:], -1), -1)[:]

        else:
            board = board_change[0][:]
    return network_white, network_black


def select_top(list_to_select, percentage):
    return_list = []
    if percentage == 0:
        num = 1
    else:
        num = int(len(list_to_select) / 100 * percentage // 1)
    # put the first n networks inn the return list
    for i in range(num):
        return_list.append(list_to_select[i])

    # sorts the returnlist:
    for check in range(num, 0, -1):
        for index in range(0, check - 1):
            if return_list[index][-1] < return_list[index + 1][-1]:
                return_list[index + 1], return_list[index] = return_list[index], return_list[index + 1]

    # replaces the worse networks with better ones
    for network_index in range(num, len(list_to_select)):
        if list_to_select[network_index][-1] > return_list[-1][-1]:
            for place in range(0, num):
                if list_to_select[network_index][-1] > return_list[place][-1]:
                    return_list.insert(place, list_to_select[network_index])
                    return_list.pop(-1)
                    break
    return return_list


def findout_fitness(list_of_networks, num_games):
    pop_size = len(list_of_networks)
    maxgames = pop_size * (pop_size + 1) / 2
    # all possible games will be played
    if num_games >= maxgames:
        for challanger in range(len(list_of_networks) - 1, 1, -1):
            for acceptant in range(0, challanger - 1):
                placeholder = complete_game_pcs(list_of_networks[challanger], list_of_networks[acceptant])
                list_of_networks[challanger], list_of_networks[acceptant] = placeholder[0], placeholder[1]
        return list_of_networks

    # shuffels arrangement of the networks in list
    random.shuffle(list_of_networks)
    start_places = []
    for i in range(-len(list_of_networks), 0):
        start_places.append(i)

    for complete_round in range(num_games // len(list_of_networks)):
        start_place = random.choice(start_places)
        start_places.remove(start_place)
        for game in range(len(list_of_networks)):
            placeholder = complete_game_pcs(list_of_networks[game], list_of_networks[game + start_place])
            list_of_networks[game], list_of_networks[game + start_place] = placeholder[0], placeholder[1]

    return list_of_networks

