import os
import random

# Constants for board size and players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players allowed

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A B C ...
    header = '  '
    for i in range(len(board[0])):
        header += chr(ord('A') + i) + '   '
    print(header)
    # Print the board with borders
    for row in range(len(board)):
        print('+' + '---+' * len(board[0]))
        line = '|'
        for col in range(len(board[0])):
            line += ' ' + board[row][col] + ' |'
        print(line)
    print('+' + '---+' * len(board[0]))

def valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    ch = input_str[0]
    if 'A' <= ch <= chr(ord('A') + cols - 1):
        return True
    return False

def get_next_open_row(board, col):
    # Return the index of the lowest empty row in the column or -1 if full
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == ' ':
            return r
    return -1

def is_winning_move(board, checker, row, col):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(max(col-3,0), min(col+4,cols)):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(max(row-3,0), min(row+4,rows)):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check diagonal (/)
    count = 0
    start_row = row + min(3, cols - 1 - col)
    start_col = col - min(3, cols - 1 - col)
    for i in range(7):
        r = start_row - i
        c = start_col + i
        if 0 <= r < rows and 0 <= c < cols:
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    # Check diagonal (\)
    count = 0
    start_row = row - min(3, col)
    start_col = col - min(3, col)
    for i in range(7):
        r = start_row + i
        c = start_col + i
        if 0 <= r < rows and 0 <= c < cols:
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

    return False

def is_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current_player_index]} starts!")

    while True:
        player = players[current_player_index]
        prompt = f"Player {player}, please enter a column: "

        # Input validation loop
        while True:
            choice = input(prompt).upper()
            if not valid_column(choice, COLUMNS):
                print("Invalid input. Please enter a valid column letter.")
                continue
            col = ord(choice) - ord('A')
            row = get_next_open_row(board, col)
            if row == -1:
                # Column full, turn lost
                print("Column full, turn lost.")
                break
            else:
                board[row][col] = player
                break

        print_board(board)

        if row != -1:
            if is_winning_move(board, player, row, col):
                print(f"Player {player} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
