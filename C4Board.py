import copy

class Board:
    board = []
    board_score = 0

    def __init__(self):

        self.board = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]

        self.ai_board = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]

    def add_chip(self, column, player_number):

        return_flg = 0

        for position, value in enumerate(self.board[column]):

            if value == 0:
                self.board[column][position] = player_number

                return_flg = 1
                break

        self.board_score = self.score()
        return return_flg

    def printList(self, list):

        print("Printing list ... ")

        for node in list:
            node.print()
            print("Score: ", node.board_score)

        input("Viewing list, press enter to continue.")

    def print(self):

        for row in range(6, 0, -1):
            print("| ", end="")

            for column in range(7):
                if self.board[column][row - 1] != 0:
                    print(self.board[column][row - 1], "", end="")

                else:
                    print("  ", end="")

            print('|')

        print("| ------------- |")
        print("| 1 2 3 4 5 6 7 |")

    def valid_locations(self):
        locations = []

        for column in range(7):
            for row in range(6):
                if self.board[column][row] == 0:
                    locations.insert(len(locations), column)
                    break
        return locations

    def child_nodes(self, player):
        children = []
        locations = self.valid_locations()

        for location in locations:
            child = copy.deepcopy(self)
            child.add_chip(location, player)
            children.insert(0, child)

        if player == 1:
            children.sort(key=self.get_score)
        else:
            children.sort(key=self.get_score, reverse=True)

        #self.printList(children)
        return children

    def get_score(self, e):
        return e.board_score

    def compare(self, new_board):

        for column in range(7):
            for row in range(6):
                if self.board[column][row] != new_board.board[column][row]:
                    return column

        return -1

    # This function returns the player number if there is a win, otherwise 0
    def evaluate(self):

        for column in range(7):
            for row in range(6):
                if (self.board[column][row] == 0):
                    pass  # No sense in checking a 0 value.

                else:

                    if column < 4:
                        # evaluate right
                        if self.board[column][row] == self.board[column + 1][row] \
                                and self.board[column][row] == self.board[column + 2][row] \
                                and self.board[column][row] == self.board[column + 3][row]:
                            return self.board[column][row], [[column, row], [column + 1, row],
                                                             [column + 2, row], [column + 3, row]]

                    if row < 3:
                        # evaluate up
                        if self.board[column][row] == self.board[column][row + 1] \
                                and self.board[column][row] == self.board[column][row + 2] \
                                and self.board[column][row] == self.board[column][row + 3]:
                            return self.board[column][row], [[column, row], [column, row + 1],
                                                             [column, row + 2], [column, row + 3]]

                    if column < 4 and row < 3:
                        # evaluate diag up right
                        if self.board[column][row] == self.board[column + 1][row + 1] \
                                and self.board[column][row] == self.board[column + 2][row + 2] \
                                and self.board[column][row] == self.board[column + 3][row + 3]:
                            return self.board[column][row], [[column, row], [column + 1, row + 1],
                                                             [column + 2, row + 2], [column + 3, row + 3]]

                    if column < 4 and row > 2:
                        # evaluate diag down right
                        if self.board[column][row] == self.board[column + 1][row - 1] \
                                and self.board[column][row] == self.board[column + 2][row - 2] \
                                and self.board[column][row] == self.board[column + 3][row - 3]:
                            return self.board[column][row], [[column, row], [column + 1, row - 1],
                                                             [column + 2, row - 2], [column + 3, row - 3]]

        return 0, [[], [], [], []]

    # This function returns the score of the current board
    def score(self):
        score = 0

        for column in range(7):
            for row in range(6):

                if (self.board[column][row] == 0):

                    pass  # No sense in checking rows above if we already found 0 in this row.

                else:

                    # EVALUATE RIGHT OF POSITION
                    if column < 4:
                        if self.board[column][row] == self.board[column + 1][row] \
                                and self.board[column][row] == self.board[column + 2][row] \
                                and self.board[column][row] == self.board[column + 3][row]:

                            if self.board[column][row] == 2:
                                return 10000
                            else:
                                return -10000

                        elif self.board[column + 1][row] == 0 \
                                and self.board[column][row] == self.board[column + 2][row] \
                                and self.board[column][row] == self.board[column + 3][row]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column + 1][row] \
                                and self.board[column + 2][row] == 0 \
                                and self.board[column][row] == self.board[column + 3][row]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column + 1][row] \
                                and self.board[column][row] == self.board[column + 2][row] \
                                and self.board[column + 3][row] == 0:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column + 1][row] \
                                and self.board[column + 2][row] == 0 \
                                and self.board[column + 3][row] == 0:

                            if self.board[column][row] == 2:
                                score = score + 25
                            else:
                                score = score - 50

                    # EVALUATE LEFT OF POSITION
                    if column > 2:
                        if self.board[column][row] == self.board[column - 1][row] \
                                and self.board[column][row] == self.board[column - 2][row] \
                                and self.board[column][row] == self.board[column - 3][row]:

                            if self.board[column][row] == 2:
                                return 10000
                            else:
                                return -10000

                        elif self.board[column - 1][row] == 0 \
                                and self.board[column][row] == self.board[column - 2][row] \
                                and self.board[column][row] == self.board[column - 3][row]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column - 1][row] \
                                and self.board[column - 2][row] == 0 \
                                and self.board[column][row] == self.board[column - 3][row]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column - 1][row] \
                                and self.board[column][row] == self.board[column - 2][row] \
                                and self.board[column - 3][row] == 0:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column - 1][row] \
                                and self.board[column - 2][row] == 0 \
                                and self.board[column - 3][row] == 0:

                            if self.board[column][row] == 2:
                                score = score + 25
                            else:
                                score = score - 50

                    # EVALUATE UP OF POSITION
                    if row < 3:
                        if self.board[column][row] == self.board[column][row + 1] \
                                and self.board[column][row] == self.board[column][row + 2] \
                                and self.board[column][row] == self.board[column][row + 3]:

                            if self.board[column][row] == 2:
                                return 10000
                            else:
                                return -10000

                        elif self.board[column][row + 1] == 0 \
                                and self.board[column][row] == self.board[column][row + 2] \
                                and self.board[column][row] == self.board[column][row + 3]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row + 1] == self.board[column][row + 1] \
                                and self.board[column][row] == 0 \
                                and self.board[column][row] == self.board[column][row + 3]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column][row + 1] \
                                and self.board[column][row] == self.board[column][row + 2] \
                                and self.board[column][row + 3] == 0:
                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column][row + 1] \
                                and self.board[column][row + 2] == 0 \
                                and self.board[column][row + 3] == 0:

                            if self.board[column][row] == 2:
                                score = score + 25
                            else:
                                score = score - 50

                    # EVALUATE DIAG UP RIGHT OF POSITION
                    if column < 4 and row < 3:
                        if self.board[column][row] == self.board[column + 1][row + 1] \
                                and self.board[column][row] == self.board[column + 2][row + 2] \
                                and self.board[column][row] == self.board[column + 3][row + 3]:

                            if self.board[column][row] == 2:
                                return 10000
                            else:
                                return -10000

                        elif self.board[column + 1][row + 1] == 0 \
                                and self.board[column][row] == self.board[column + 2][row + 2] \
                                and self.board[column][row] == self.board[column + 3][row + 3]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column + 1][row + 1] \
                                and self.board[column + 2][row + 2] == 0 \
                                and self.board[column][row] == self.board[column + 3][row + 3]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column + 1][row + 1] \
                                and self.board[column][row] == self.board[column + 2][row + 2] \
                                and self.board[column + 3][row + 3] == 0:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column + 1][row + 1] \
                                and self.board[column + 2][row + 2] == 0 \
                                and self.board[column + 3][row + 3] == 0:

                            if self.board[column][row] == 2:
                                score = score + 25
                            else:
                                score = score - 50

                    # EVALUATE DIAG UP LEFT OF POSITION
                    if column > 2 and row < 3:
                        if self.board[column][row] == self.board[column - 1][row + 1] \
                                and self.board[column][row] == self.board[column - 2][row + 2] \
                                and self.board[column][row] == self.board[column - 3][row + 3]:

                            if self.board[column][row] == 2:
                                return 10000
                            else:
                                return -10000

                        elif self.board[column - 1][row + 1] == 0 \
                                and self.board[column][row] == self.board[column - 2][row + 2] \
                                and self.board[column][row] == self.board[column - 3][row + 3]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column - 1][row + 1] \
                                and self.board[column - 2][row + 2] == 0 \
                                and self.board[column][row] == self.board[column - 3][row + 3]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column - 1][row + 1] \
                                and self.board[column][row] == self.board[column - 2][row + 2] \
                                and self.board[column - 3][row + 3] == 0:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column - 1][row + 1] \
                                and self.board[column - 2][row + 2] == 0 \
                                and self.board[column - 3][row + 3] == 0:

                            if self.board[column][row] == 2:
                                score = score + 25
                            else:
                                score = score - 50

                    # EVALUATE DIAG DOWN RIGHT OF POSITION
                    if column < 4 and row > 2:

                        if self.board[column][row] == self.board[column + 1][row - 1] \
                                and self.board[column][row] == self.board[column + 2][row - 2] \
                                and self.board[column][row] == self.board[column + 3][row - 3]:

                            if self.board[column][row] == 2:
                                return 10000
                            else:
                                return -10000

                        elif self.board[column + 1][row - 1] == 0 \
                                and self.board[column][row] == self.board[column + 2][row - 2] \
                                and self.board[column][row] == self.board[column + 3][row - 3]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column + 1][row - 1] \
                                and self.board[column + 2][row - 2] == 0 \
                                and self.board[column][row] == self.board[column + 3][row - 3]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column + 1][row - 1] \
                                and self.board[column][row] == self.board[column + 2][row - 2] \
                                and self.board[column + 3][row - 3] == 0:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column + 1][row - 1] \
                                and self.board[column + 2][row - 2] == 0 \
                                and self.board[column + 3][row - 3] == 0:

                            if self.board[column][row] == 2:
                                score = score + 25
                            else:
                                score = score - 50

                    # EVALUATE DIAG DOWN LEFT OF POSITION
                    if column > 2 and row > 2:

                        if self.board[column][row] == self.board[column - 1][row - 1] \
                                and self.board[column][row] == self.board[column - 2][row - 2] \
                                and self.board[column][row] == self.board[column - 3][row - 3]:

                            if self.board[column][row] == 2:
                                return 10000
                            else:
                                return -10000

                        elif self.board[column - 1][row - 1] == 0 \
                                and self.board[column][row] == self.board[column - 2][row - 2] \
                                and self.board[column][row] == self.board[column - 3][row - 3]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column - 1][row - 1] \
                                and self.board[column - 2][row - 2] == 0 \
                                and self.board[column][row] == self.board[column - 3][row - 3]:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column - 1][row - 1] \
                                and self.board[column][row] == self.board[column - 2][row - 2] \
                                and self.board[column - 3][row - 3] == 0:

                            if self.board[column][row] == 2:
                                score = score + 75
                            else:
                                score = score - 100

                        elif self.board[column][row] == self.board[column - 1][row - 1] \
                                and self.board[column - 2][row - 2] == 0 \
                                and self.board[column - 3][row - 3] == 0:

                            if self.board[column][row] == 2:
                                score = score + 25
                            else:
                                score = score - 50

        return score
