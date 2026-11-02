import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    # Create a board filled with empty spaces
    board = []
    for _ in range(ROWS):
        board.append([' ' for _ in range(COLS)])
    return board

def print_board(board):
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)])
    print(header)
    
    # Print the board rows with borders
    border = '+' + ('---+' * COLS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    print(border)

def get_valid_column(board, player):
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        col_index = ord(column) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + COLS - 1)}.")
            continue
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col_index

def place_checker(board, col_index, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = player
            return row  # Return the row where the checker was placed
    return -1  # Column is full (shouldn't happen due to prior validation)

def check_win(board, row, col, player):
    # Check horizontal
    count = 0
    for c in range(max(0, col - 3), min(COLS, col + 4)):
        if board[row][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(max(0, row - 3), min(ROWS, row + 4)):
        if board[r][col] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    for i in range(-3, 4):
        r, c = row + i, col + i
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    for i in range(-3, 4):
        r, c = row - i, col + i
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    
    return False

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    player_symbols = PLAYERS[:NUM_PLAYERS]
    
    while True:
        print_board(board)
        col_index = get_valid_column(board, player_symbols[current_player])
        row = place_checker(board, col_index, player_symbols[current_player])
        
        if check_win(board, row, col_index, player_symbols[current_player]):
            print_board(board)
            print(f"Player {player_symbols[current_player]} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
