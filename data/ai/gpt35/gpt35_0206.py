import os
import random

# Constants - change these if needed but for submission use 6 rows, 7 cols and 2 players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board

def print_board(board):
    clear_screen()
    # Print column headers A, B, C, ...
    header = "  "
    for i in range(len(board[0])):
        header += "  " + chr(ord('A') + i) + " "
    print(header)

    separator = '+' + '---+' * len(board[0])
    for row in board:
        print(separator)
        line = '|'
        for cell in row:
            line += " " + cell + " |"
        print(line)
    print(separator)

def valid_column_input(inp, cols):
    if len(inp) != 1:
        return False
    if not inp.isalpha():
        return False
    col = ord(inp) - ord('A')
    if col < 0 or col >= cols:
        return False
    return True

def column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    """
    Place checker in the lowest available position in column col.
    Return True if placed, False if column full.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Check diagonal (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Check diagonal (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def board_full(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print("Randomly selected first player:", players[current_player_index])

    while True:
        player_checker = players[current_player_index]
        print("Player {}, please enter a column:".format(player_checker))
        inp = input().strip().upper()
        if not valid_column_input(inp, COLS):
            # invalid input - keep asking same player
            continue
        col = ord(inp) - ord('A')

        if column_full(board, col):
            # column full, player loses turn, move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue
        
        placed = place_checker(board, col, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print("Player {} won!".format(player_checker))
            break

        if board_full(board):
            print("Draw!")
            break

        # next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
