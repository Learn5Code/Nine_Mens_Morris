def threeinarow(board, where):
    if board[where] == board[nexus[where][0][0]] == board[nexus[where][0][1]] or \
            board[where] == board[nexus[where][1][0]] == board[nexus[where][1][1]]:
        return True
    else:
        return False


def print_board(board):
    temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(board)):
        if board[i] == 1:
            temp[i] = "W"
        elif board[i] == -1:
            temp[i] = "B"
    str_board = " " + str(temp[0]) + " -------- " + str(temp[1]) + " -------- " + str(temp[2]) + "\n |    " + \
                str(temp[3]) + " --- " + str(temp[4]) + " --- " + str(temp[5]) + "    |\n |    |   " + \
                str(temp[6]) + " " + str(temp[7]) + " " + str(temp[8]) + "   |    |\n " + str(temp[9]) + " -- " + \
                str(temp[10]) + " - " + str(temp[11]) + "   " + str(temp[12]) + " - " + str(temp[13]) + " -- " + \
                str(temp[14]) + "\n |    |   " + str(temp[15]) + " " + str(temp[16]) + " " + str(temp[17]) + \
                "   |    |\n |    " + str(temp[18]) + " --- " + str(temp[19]) + " --- " + str(temp[20]) + "    |\n " \
                + str(temp[21]) + " -------- " + str(temp[22]) + " -------- " + str(temp[23])
    return str_board


def print_index_board():
    str_board = "0 ----------- 1 ----------- 2\n |     3 ----- 4 ----- 5     |\n |     |    6  7  8    |     |\n " \
                "9 --- 10 - 11    12 - 13 -- 14\n |     |    15 16 17   |     |\n |     18 ---- 19 ---- 20    |\n" \
                " 21 ---------- 22 ---------- 23\n"

    return str_board


def playercolor(player):
    if player == 1:
        return "White"
    return "Black"


def take_stone_possible(board, which):
    if threeinarow(board, which):
        return False
    return True


def steineplacen():
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    player = 1
    possible = False
    for placestone in range(18):
        while not possible:
            x = int(input(playercolor(player) + " Where do you wanna place your stone?\n"
                          + print_board(board) + "\n?: "))
            if board[x] == 0:
                possible = True
        possible = False
        board[x] = player
        if threeinarow(board, x):
            take_stone(board, player)
        player *= -1
    return board


def take_stone(board, who):
    possible = False
    while not possible:
        x = int(input(playercolor(who) + " Which stone do you wanna take? "))
        if board[x] == -1 * who and take_stone_possible(board, x):
            possible = True
    board[x] = 0
    return board


# who = whose move (1 = white, -1 = black)
def possiblemoves(board, who):
    if who == 1:
        who1 = 0
    else:
        who1 = 1
    poss_moves = []
    zug_nummer = 0
    from_where = to = 0
    # if you have exactly three stones
    if count_stones(board)[who1] == 3:
        for chip in board:
            if chip == who:
                for emptyfield in board:
                    if emptyfield == 0:
                        poss_moves.append([zug_nummer, from_where, to])
                        zug_nummer += 1
                    to += 1
                to = 0
            from_where += 1
        return poss_moves
    # if you have more than three stones
    for chip in board:
        if chip == who:
            for to in connected_points[from_where]:
                if board[to] == 0:
                    poss_moves.append([zug_nummer, from_where, to])
                    zug_nummer += 1
        from_where += 1
    return poss_moves


def count_stones(board):
    white = black = 0
    for field in board:
        if field == 1:
            white += 1
        elif field == -1:
            black += 1
    return white, black


def move(player, board):
    all_moves = possiblemoves(board, player)
    for poss_move in all_moves:
        print(poss_move)
    print(print_board(board))
    while True:
        move_index = int(input(playercolor(player) + " Which one of the listet moves do you choose?\n" +
                                                     "First number = move number, second number = from, "
                                                     "third number = to: "))
        if -1 < move_index < len(all_moves):
            break
    board[all_moves[move_index][1]] = 0
    board[all_moves[move_index][2]] = player
    if threeinarow(board, all_moves[move_index][2]):
        board = take_stone(board, player)
    return board


def complete_game_humans():
    print("indexboard:\n", print_index_board())
    board = steineplacen()
    move_number = 18
    # tie after 100 mooves
    player = 1
    while count_stones(board)[0] != 2 and count_stones(board)[1] != 2 and move_number <= 100 and len(
            possiblemoves(board, player)) != 0:
        board = move(player, board)
        move_number += 1
        player *= -1
    if move_number > 100:
        print("Tie" + print_board(board))
    elif count_stones(board)[0] < 3:
        print("Black wins" + print_board(board))
    elif count_stones(board)[1] < 3:
        print("White wins" + print_board(board))


connected_points = [[1, 9], [0, 2, 4], [1, 14],  # 0, 1, 2
                    [10, 4], [1, 3, 5, 7], [4, 13],  # 3, 4, 5
                    [7, 11], [4, 6, 8], [7, 12],  # 6, 7, 8
                    [0, 10, 21], [3, 9, 11, 18], [6, 10, 15],  # 9, 10, 11
                    [8, 13, 17], [5, 12, 14, 20], [2, 13, 23],  # 12, 13, 14
                    [11, 16], [15, 17, 19], [12, 16],  # 15, 16, 17
                    [10, 19], [16, 18, 20, 22], [13, 19],  # 18, 19, 20
                    [9, 22], [19, 21, 23], [14, 22]]  # 21, 22, 23

nexus = [[[1, 2], [9, 21]], [[0, 2], [4, 7]], [[0, 1], [14, 23]],  # 0,  1,  2
         [[4, 5], [10, 18]], [[1, 7], [3, 5]], [[3, 4], [13, 20]],  # 3,  4,  5
         [[7, 8], [11, 15]], [[1, 4], [6, 8]], [[6, 7], [12, 17]],  # 6,  7,  8
         [[0, 21], [10, 11]], [[3, 18], [9, 11]], [[6, 15], [9, 10]],  # 9,  10, 11
         [[8, 17], [13, 14]], [[5, 20], [12, 14]], [[2, 23], [12, 13]],  # 12, 13, 14
         [[6, 11], [16, 17]], [[15, 17], [19, 22]], [[8, 12], [15, 16]],  # 15, 16, 17
         [[3, 10], [19, 20]], [[16, 22], [18, 20]], [[5, 13], [18, 19]],  # 18, 19, 20
         [[0, 9], [22, 23]], [[16, 19], [21, 23]], [[2, 14], [21, 22]]]  # 21, 22, 23
