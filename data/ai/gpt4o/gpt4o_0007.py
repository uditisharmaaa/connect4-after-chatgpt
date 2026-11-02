import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = ' ' + '   '.join(chr(65 + i) for i in range(COLUMNS))
    print(column_labels)
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def is_valid_input(user_input):
    return user_input.isalpha() and len(user_input) == 1 and 'A' <= user_input <= chr(65 + COLUMNS - 1)

def get_next_open_row(board, column):
    for r in range(ROWS-1, -1, -1):
        if board[r][column] == ' ':
            return r
    return None

def place_checker(board, column, player_symbol):
    row = get_next_open_row(board, column)
    if row is not None:
        board[row][column] = player_symbol
        return True
    return False

def check_win(board, player_symbol):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLUMNS-3):
            if board[r][c] == player_symbol and board[r][c+1] == player_symbol and board[r][c+2] == player_symbol and board[r][c+3] == player_symbol:
                return True

    # Check vertical locations
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == player_symbol and board[r+1][c] == player_symbol and board[r+2][c] == player_symbol and board[r+3][c] == player_symbol:
                return True

    # Check positively sloped diagonals
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            if board[r][c] == player_symbol and board[r+1][c+1] == player_symbol and board[r+2][c+2] == player_symbol and board[r+3][c+3] == player_symbol:
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            if board[r][c] == player_symbol and board[r-1][c+1] == player_symbol and board[r-2][c+2] == player_symbol and board[r-3][c+3] == player_symbol:
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board(ROWS, COLUMNS)
    num_players = 2
    players = PLAYER_SYMBOLS[:num_players]
    turn = random.randint(0, num_players - 1)

    print_board(board)
    
    while True:
        player_symbol = players[turn]
        user_input = input(f"Player {player_symbol}, please enter a column: ").upper()

        if not is_valid_input(user_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        column = ord(user_input) - 65
        
        if not place_checker(board, column, player_symbol):
            print(f"Column {user_input} is full. Please choose another column.")
            continue
        
        print_board(board)

        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break
        
        if check_draw(board):
            print("Game is a draw!")
            break
        
        turn = (turn + 1) % num_players

if __name__ == "__main__":
    main()
