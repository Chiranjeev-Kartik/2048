"""
Author: Kartikay Chiranjeev Gupta.
Last Modified: 8/27/2021
"""
import random
import copy
import pygame
from pygame import *
import sys

WIN = pygame.display.set_mode((600, 600))
pygame.display.set_caption('2048 - The Game')
pygame.font.init()
CLOCK = pygame.time.Clock()
FPS = 30


def draw_lines_and_fill(board, n):
    """
    Draws lines and fill value from board.
    :param board: 2-D list.
    :param n: Number of rows/column.
    :return: None
    """
    pygame.draw.rect(WIN, (0, 0, 0), pygame.Rect(20, 20, 560, 560), width=4)
    x = 560 // n
    for i in range(1, n):
        start_pos = (20 + x * i, 20)
        stop_pos = (20 + x * i, 580)
        pygame.draw.line(WIN, (0, 0, 0), start_pos, stop_pos, width=2)
    for i in range(1, n):
        start_pos = (20, 20 + x * i)
        stop_pos = (580, 20 + x * i)
        pygame.draw.line(WIN, (0, 0, 0), start_pos, stop_pos, width=2)
    size = 200 // n
    off_x = 80//n
    off_y = 160//n
    font_ = pygame.font.SysFont('candara', size, False, False)
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                num = font_.render(' ', True, (0, 0, 0))
            else:
                num = font_.render(str(board[i][j]), True, (0, 0, 0))
            WIN.blit(num, (20 + off_x + x * i, 20 + off_y + x * j))


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


def game_end(msg, board):
    """
    Displays the message (WIN, OR LOST) and exits the game at event.QUIT.
    :param msg: Message to be displayed.
    :param board: 2-D list.
    :return: None
    """
    while True:
        CLOCK.tick(FPS)
        WIN.fill((92, 222, 222))
        draw_lines_and_fill(board, len(board))
        msg_t = pygame.font.SysFont('candara', 50, False, False)
        msg_t = msg_t.render(msg, True, (0, 0, 0))
        WIN.blit(msg_t, (200, 200))
        pygame.display.update()
        for event_ in pygame.event.get():
            if event_.type == QUIT:
                sys.exit()


def main_game():
    """
    Main Game function.
    :return: None
    """
    n = int(input('Enter board dimension: '))
    board = generate_board(n)
    board = generate_random_two(board, n)
    while not win(board) and not lost(board):
        CLOCK.tick(FPS)
        WIN.fill((92, 222, 222))
        draw_lines_and_fill(board, n)
        for event_ in pygame.event.get():
            if event_.type == KEYDOWN:
                if event_.key == K_UP:
                    board = sum_rows(board, 'left')
                    board = generate_random_two(board, n)
                elif event_.key == K_DOWN:
                    board = sum_rows(board, 'right')
                    board = generate_random_two(board, n)
                elif event_.key == K_RIGHT:
                    board = sum_cols(board, 'right')
                    board = generate_random_two(board, n)
                elif event_.key == K_LEFT:
                    board = sum_cols(board, 'left')
                    board = generate_random_two(board, n)
            elif event_.type == QUIT:
                sys.exit()
        pygame.display.update()
    if lost(board):
        game_end('YOU LOST', board)
    else:
        game_end('YOU WON', board)


# Start the game with 3 rows/columns if you are new to this game :)
main_game()
