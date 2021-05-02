from random import randint


# Function for random number from 1 to 6
def roll_dice():
    button = " "
    while not button == "":  # while not pressed Enter
        print("Press Enter to roll the dice.")
        button = input().upper()
    return randint(1, 6)


# Function which updates 2D list field:
# placing values of lists way and home to list field
def update_field(field, way, home):
    # half of field side
    half = int(len(way) / 8)

    # place way's values on field
    for i in range(len(way)):
        if 0 - 1 < i < half:
            field[half - i - 1][half - 1] = way[i]

        elif i == half:
            field[0][half] = way[i]

        elif half < i < half * 2:
            field[i - half - 1][half + 1] = way[i]
        elif half * 2 - 1 < i < half * 3:
            field[half - 1][i - half + 1] = way[i]

        elif i == half * 3:
            field[half][half * 2] = way[i]

        elif half * 3 < i < half * 4:
            field[half + 1][half * 3 - i] = way[i]
        elif half * 4 - 1 < i < half * 5:
            field[i - half * 3 + 1][half + 1] = way[i]

        elif i == half * 5:
            field[half * 2][half] = way[i]

        elif half * 5 < i < half * 6:
            field[half * 5 - i][half - 1] = way[i]
        elif half * 6 - 1 < i < half * 7:
            field[half + 1][half * 7 - i - 1] = way[i]

        elif i == half * 7:
            field[half][0] = way[i]

        elif half * 7 < i < half * 8:
            field[half - 1][i - half * 7 - 1] = way[i]

    # place home's values on field
    for i in range(len(home[0])):
        field[1 + i][half] = home[1][i]
        field[half][half * 2 - i - 1] = "ᴏ"
        field[half * 2 - i - 1][half] = home[0][i]
        field[half][1 + i] = "ᴏ"

    # place each row of list field to string variable [s] and print(s)
    for y in range(0, int(len(way) / 4 + 1) + 1):
        s = ""
        for x in range(0, int(len(way) / 4 + 1) + 1):
            if y == 0 and x == 0:
                s = "   "
            elif y == 0 and x > 0:
                s += " " + str(x - 10 * int(x / 10)) + " "
            elif x == 0 and y > 0:
                s += " " + str(y - 10 * int(y / 10)) + " "
            else:
                s += " " + str(field[y - 1][x - 1]) + " "
        print(s)


# all game process is going here
def game(out, way, home, players, state, current_player, refs, home_list_top):
    # switch player every cycle
    current_player[0] = 1 - current_player[0]
    print("Current player:", players[current_player[0]])
    print("Outside figures: ", players[0], "=", out[0], " ", players[1], "=", out[1])

    # ********************************************************* start *************************************************
    if state[current_player[0]] == 0:
        button = " "
        while not button == "":
            print("Press Enter for put player", players[current_player[0]], "on game field.")
            button = input().upper()

        # if start position is occupied by other player's figure
        if way[refs[current_player[0]]] == players[1 - current_player[0]]:
            out[1 - current_player[0]] += 1  # then it goes outside
            state[1 - current_player[0]] = 0  # and reset state
            print("**************************************************************")
            print("Collision. Player", players[1 - current_player[0]], "goes out.")

        way[refs[current_player[0]]] = players[current_player[0]]
        state[current_player[0]] = 1  # changing state of figure
        out[current_player[0]] -= 1  # decrease figure outside
        return False

    # ********************************************************* going on the way **************************************
    elif state[current_player[0]] == 1:
        # roll the dice - random number
        dice_num = roll_dice()
        print("Player", players[current_player[0]], "dice:", dice_num)

        # take current and next positions
        cur_pos = way.index(players[current_player[0]])
        next_pos = cur_pos + dice_num

        # if next position at the beginning of the list [way] . Make loop
        if next_pos > len(way) - 1:
            next_pos = next_pos - len(way)

        # if next position inside home
        if (cur_pos < refs[current_player[0]] <= next_pos) or \
                (next_pos < cur_pos < refs[current_player[0]]):

            # calculate position at home list
            pos_at_home = dice_num - (refs[current_player[0]] - cur_pos)

            # if calculated position more than length of home then players skips move
            if pos_at_home > home_list_top[current_player[0]]:
                print("******************** Player", players[current_player[0]], "skips move ************************")
                return False
            else:  # insert figure to home
                print("******************** Player", players[current_player[0]], "added figure to home **********")
                state[current_player[0]] = 2  # state at home
                way[cur_pos] = "*"
                home[current_player[0]][pos_at_home] = players[current_player[0]]
                # if position is top of list
                if pos_at_home == home_list_top[current_player[0]]:
                    state[current_player[0]] = 0  # reset state
                    home_list_top[current_player[0]] -= 1  # decrease top
                    # if this is last figure then player wins
                    if out[current_player[0]] == 0:
                        way[cur_pos] = "*"
                        home[current_player[0]][pos_at_home] = players[current_player[0]]
                        print("******************** Player", players[current_player[0]],"wins **************************")
                        return True
            return False

        # if next position is occupied by other player's figure
        if way[next_pos] == players[1 - current_player[0]]:
            print("************ Collision. Player", players[1 - current_player[0]], "goes out ************")
            out[1 - current_player[0]] += 1  # then goes out
            state[1 - current_player[0]] = 0  # and state reset

        # next position is free, do replace
        way[cur_pos], way[next_pos] = way[next_pos], way[cur_pos]
        way[cur_pos] = "*"
        return False

    # ********************************************************* going on the home *************************************
    elif state[current_player[0]] == 2:
        # roll the dice - random number
        dice_num = roll_dice()
        print("Player", players[current_player[0]], "dice:", dice_num)

        # take current and next positions
        cur_pos = home[current_player[0]].index(players[current_player[0]])
        next_pos = cur_pos + dice_num

        # if calculated position more than length of home then players skips move
        if next_pos > home_list_top[current_player[0]]:
            print("******************** Player", players[current_player[0]], "skips move ************************")
            return False
        else:
            home[current_player[0]][cur_pos], home[current_player[0]][next_pos] = home[current_player[0]][next_pos], home[current_player[0]][cur_pos]
            # if position is top of list
            if next_pos == home_list_top[current_player[0]]:
                state[current_player[0]] = 0  # reset state
                home_list_top[current_player[0]] -= 1
                # if this is last figure then player wins
                if out[current_player[0]] == 0:
                    home[current_player[0]][cur_pos] = "ᴏ"
                    home[current_player[0]][next_pos] = players[current_player[0]]
                    print("******************** Player", players[current_player[0]], "wins **************************")
                    return True
        return False


# main starting function
def run():
    players = ["A", "B"]    # letters for player's figures
    player_state = [0, 0]   # states of player's figures
    current_player = [1]    # current player in while cycle
    empty_way_cell = "*"    # sign for empty game way position
    empty_home_cell = "ᴏ"   # sign for empty home position
    center_symbol = "x"     # sign for center of game field

    # asking the size of game field
    size = 0
    print("Input size of game field.")
    while not (size % 2 == 1 and size >= 5):
        print("Size should be odd and more or equal to 5.")
        size = int(input())

    # calculate game way list length
    way_len = size * 4 - 4
    way = [empty_way_cell for i in range(way_len)]
    print("Way length:", way_len)

    # calculate home list length
    home_len = int((size - 3) / 2)
    home = [[empty_home_cell for cell in range(home_len)] for player in range(4)]
    print("Home size:", home_len)

    # in this list indexes of list [home] which are upper and free
    home_list_top = [home_len - 1 for cell in range(4)]

    # number of figures limited by 4
    out_num = home_len
    if home_len > 4:
        out_num = 4

    # list of numbers of figures which outside game field
    player_figures_out = [out_num for i in range(2)]

    # instantiate 2D list of game field. all values  = " "
    field = [[" " for y in range(int(len(way) / 4 + 1))] for x in range(int(len(way) / 4 + 1))]
    field[int((size - 1) / 2)][int((size - 1) / 2)] = center_symbol  # center of game field. it will not be changing

    half = int(len(way) / 8)

    refs = [half * 5 + 1, half * 1 + 1]    # start positions of players
    update_field(field, way, home)         # show created empty field

    have_winner = False  # flag if was winner
    # infinity cycle works until have_winner = False
    # function game() returns True if there is have winner
    while not have_winner:
        have_winner = game(player_figures_out, way, home, players, player_state, current_player, refs, home_list_top)
        update_field(field, way, home)


run()
