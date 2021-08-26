"""
Author: Kartikay Chiranjeev Gupta.
Last Modified: 8/26/2021
"""
import random
import copy


def generate_board(n):
    """
    Generates a 2-D list containing all zeroes.
    :param n: Number of rows/columns
    :return: 2-D list.
    """
    board = [[0 for _ in range(n)] for _ in range(n)]
    return board


def __remove__zeros(lis):
    """
    Removes all zero from list and returns the number of zeros removed.
    :param lis: list object.
    :return: number of zeroes removed, new list with no zeros.
    """
    n = lis.count(0)
    for _ in range(n):
        lis.remove(0)
    return n, lis


def sum_rows(board, direction):
    """
    Sums all rows in board as per game rule and places zero according to direction.
    :param board: 2-D list.
    :param direction: Direction of placing the sums (values: 'left' or 'right').
    :return: New board with summed values.
    """
    for x, row in enumerate(board):
        n, row = __remove__zeros(row)
        temp = copy.deepcopy(row)
        for i in range(len(row) - 1):
            if row[i] == row[i + 1]:
                temp[i + 1] = temp[i] + temp[i + 1]
                temp[i] = 0
        m, temp = __remove__zeros(temp)
        if direction == 'left':
            [temp.append(0) for _ in range(n + m)]
        elif direction == 'right':
            [temp.insert(0, 0) for _ in range(n + m)]
        board[x] = temp
    return board


def __transpose__(board):
    """
    Returns matrix transpose of board.
    :param board: 2-D list.
    :return: transpose of board.
    """
    temp = []
    for i in range(len(board)):
        temp.append([])
        for j in range(len(board[i])):
            temp[i].append(board[j][i])
    return temp


def sum_cols(board, direction):
    """
    Sums all columns in board as per game rule and places zero according to direction.
    :param board: 2-D list.
    :param direction: Direction of placing the sums (values: 'left' or 'right').
    :return: New board with summed values.
    """
    board = __transpose__(board)
    board = sum_rows(board, direction)
    board = __transpose__(board)
    return board


def generate_random_two(board, n):
    """
    Generates 2 at random place in board.
    :param board: 2-D list.
    :param n: Number of rows/columns.
    :return: New Board with 2 randomly placed.
    """
    while True:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if board[i][j] == 0:
            board[i][j] = 2
            return board


def represent_board(board, n):
    """
    Represents board in pretty format.
    :param board: 2-D list.
    :param n: Number of rows/columns in board.
    :return: None
    """
    print('+' + '-----+' * n)
    for i in range(n):
        for j in range(n):
            print(f'  {board[i][j]}  |' if j < n-1 else f'  {board[i][j]}  ', end='')
        print('\n+' + '-----+' * n)
    return None


def win(board):
    """
    Checks if 2048 is present in board.
    :param board: 2-D list.
    :return: Bool.
    """
    for row in board:
        if 2048 in row:
            print(board)
            return True
    return False


def lost(board):
    """
    Checks if there is any zero left in board.
    :param board: 2-D list.
    :return: Bool.
    """
    for row in board:
        for i in row:
            if i == 0:
                return False
    return True


def take_move():
    """
    Asks and verify if the input given by user is valid.
    :return: Valid string entered by user.
    """
    move = input('Enter Move (W, S, A, D): ')
    while move not in ('w', 'a', 's', 'd', 'W', 'A', 'S', 'D'):
        print('Invalid move!')
        move = input('Enter Move (W, S, A, D): ')
    return move


def main_game():
    """
    Main Game function.
    :return: None
    """
    n = int(input('Enter board dimension: '))
    board = generate_board(n)
    while not win(board) and not lost(board):
        board = generate_random_two(board, n)
        represent_board(board, n)
        move = take_move()
        if move == 'W' or move == 'w':
            board = sum_cols(board, 'left')
        elif move == 'A' or move == 'a':
            board = sum_rows(board, 'left')
        elif move == 'S' or move == 's':
            board = sum_cols(board, 'right')
        elif move == 'D' or move == 'd':
            board = sum_rows(board, 'right')
    if lost(board):
        print('YOU LOST!')
    else:
        print("You WON!")


# Start the game with 3 rows/columns if you are new to this game :)
main_game()
