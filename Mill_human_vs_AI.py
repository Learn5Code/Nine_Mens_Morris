import NN_ebsl
import Mill_humans
import Mill_for_AIs
import ast


def game_human_vs_ai(network, human_player_color):
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pc_color = human_player_color * -1
    print("index board:\n", Mill_humans.print_index_board())
    if human_player_color == 1:
        move = True
        bruh = 1
    else:
        move = False
        bruh = 0

    # place stonens
    for i in range(8):
        if move:
            possible = False
            while not possible:
                x = int(input(Mill_humans.playercolor(human_player_color) + " Where do you wanna place your stone?\n"
                              + Mill_humans.print_board(board) + "\n?: "))
                if -1 < x < 24:
                    if board[x] == 0:
                        possible = True
            board[x] = human_player_color
            if Mill_humans.threeinarow(board, x):
                Mill_humans.take_stone(board, human_player_color)
            move = False
        else:
            board_change = Mill_for_AIs.best_board(network, pc_color,
                                                   Mill_for_AIs.possible_boards_placing(board, pc_color))[:]
            board = board_change[0][:]
            if Mill_for_AIs.three_line(board_change):
                board = Mill_for_AIs.best_board_takeing(network, Mill_for_AIs.poss_takements(board, pc_color), 1)
            else:
                board = board_change[0]
            move = True

    # moves
    for i in range(82):
        if Mill_humans.count_stones(board)[0] < 3 or Mill_humans.count_stones(board)[1] < 3:
            if Mill_humans.count_stones(board)[0] < 3 or len(Mill_for_AIs.poss_move(board, human_player_color)) == 0:
                print("Black wins")
            else:
                print("White Wins!")
            break
        if move:
            board = Mill_humans.move(human_player_color, board)
            move = False
        else:
            move = True
            poss_moves = Mill_for_AIs.poss_move(board, pc_color)
            if len(poss_moves) == 0 or Mill_for_AIs.count_stones(board)[bruh] < 3:
                print("Black Wins!")
                break
            board_change = Mill_for_AIs.best_board(network, pc_color, poss_moves)[:]
            if Mill_for_AIs.three_line(board_change):
                if len(Mill_for_AIs.poss_takements(board, pc_color)) != 0:
                    board = Mill_for_AIs.best_board_takeing(network, Mill_for_AIs.poss_takements(board, 1), 1)[:]
            else:
                board = board_change[0][:]
    print("End of the game. You suck! Just sayin!")


def load_nw(foldername, gen_folder, filename):
    try:
        nw_str = open("Trained Networks/" + foldername + "/" + gen_folder + "/" + filename, "r").readlines(-1)
    except FileNotFoundError:
        print("Once again you've given me the wrong name. STUPID ASS BITCH!!")
        return
    nw_list = []
    for nw in nw_str[1:]:
        nw_list.append(ast.literal_eval(nw))
    board = Mill_for_AIs.select_top(nw_list, 0)[0]
    props = open("Trained Networks/" + foldername + "/proprieties", "r").readlines(1)
    [a, b, c, d] = ast.literal_eval(props[0])
    board.insert(0, NN_ebsl.create_network(a, b, c, d)[0])
    return board


netz = load_nw("First Trained AI", "gen_2", "gen_2.100")
game_human_vs_ai(netz, 1)
