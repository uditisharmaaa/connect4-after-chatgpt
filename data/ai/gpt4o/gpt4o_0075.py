import os
import random

# Constants
ROWS, COLS, MAX_COLS = 6, 7, 26
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_CHECKERS = CHECKERS[:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    headers = '  '.join(chr(c + 65) for c in range(len(board[0])))
    print(f"  {headers}")
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def is_valid_move(column, board):
    if not ('A' <= column <= chr(65 + len(board[0]) - 1)):
        return False
    col_index = ord(column) - 65
    return board[0][col_index] == ' '

def place_checker(checker, column, board):
    col_index = ord(column) - 65
    for row in range(len(board) - 1, -1, -1):  # Start at the bottom
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return

def check_winner(checker, board):
    return (check_horizontal(checker, board) or
            check_vertical(checker, board) or
            check_diagonal(checker, board))

def check_horizontal(checker, board):
    for row in board:
        for col in range(len(row) - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True
    return False

def check_vertical(checker, board):
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    return False

def check_diagonal(checker, board):
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
        for col in range(3, len(board[0])):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    random.seed()
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)
    while True:
        player_checker = PLAYER_CHECKERS[current_player]
        print(f"Player {player_checker}, please enter a column:")
        column = input().strip().upper()

        while not is_valid_move(column, board):
            print("Invalid move, please enter another column:")
            column = input().strip().upper()

        place_checker(player_checker, column, board)
        print_board(board)

        if check_winner(player_checker, board):
            print(f"Player {player_checker} won!")
            break
        if is_draw(board):
            print("Game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
