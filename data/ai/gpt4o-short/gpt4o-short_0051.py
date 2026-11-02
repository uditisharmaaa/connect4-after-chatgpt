import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Adjust as needed for 2-5 players
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print(' ' + ' '.join(COLUMN_LABELS))
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLUMNS)

def is_valid_input(choice):
    return choice in COLUMN_LABELS

def get_available_row(board, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def make_move(board, col, player):
    row = get_available_row(board, col)
    if row is not None:
        board[row][col] = player
        return True
    return False

def check_direction(board, start_row, start_col, delta_row, delta_col, player):
    count = 0
    for i in range(4):
        row = start_row + i * delta_row
        col = start_col + i * delta_col
        if 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == player:
            count += 1
        else:
            break
    return count == 4

def check_winner(board, player):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (check_direction(board, row, col, 0, 1, player) or  # Horizontal
                check_direction(board, row, col, 1, 0, player) or  # Vertical
                check_direction(board, row, col, 1, 1, player) or  # Diagonal /
                check_direction(board, row, col, 1, -1, player)): # Diagonal \
                return True
    return False

def is_full(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def connect_4_game():
    board = create_board()
    turn = 0
    random.shuffle(PLAYERS)
    num_players = len(PLAYERS)
    
    while True:
        print_board(board)
        current_player = PLAYERS[turn % num_players]
        print(f"Player {current_player}'s turn. Choose column A-G:")

        choice = input().strip().upper()
        if not is_valid_input(choice):
            print("Invalid input. Try again.")
            continue
        
        col = COLUMN_LABELS.index(choice)
        if not make_move(board, col, current_player):
            print("Column is full. Try another column.")
            continue

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        
        if is_full(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        turn += 1

if __name__ == '__main__':
    connect_4_game()
