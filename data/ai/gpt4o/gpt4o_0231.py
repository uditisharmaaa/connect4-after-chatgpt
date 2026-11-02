import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def column_to_index(char):
    return ord(char) - 65

def is_valid_input(col):
    return col.isalpha() and len(col) == 1 and 0 <= column_to_index(col) < COLUMNS

def place_checker(player, col):
    col_idx = column_to_index(col)
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = player
            return True
    return False

def check_win():
    # Check horizontal win
    for row in board:
        for i in range(COLUMNS - 3):
            if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                return True
    
    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] != ' ' and board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]:
                return True
    
    # Check diagonal (bottom-left to top-right) win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] != ' ' and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                return True
    
    # Check diagonal (top-left to bottom-right) win
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] != ' ' and board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                return True
    
    return False

def check_draw():
    return all(cell != ' ' for row in board for cell in row)

def main():
    num_players = 2  # Adjust if needed for more players
    players = PLAYERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    print_board()
    
    while True:
        player = players[current_player_index]
        print(f"Player {player}, please enter a column:")
        while True:
            col = input().strip().upper()
            if is_valid_input(col) and place_checker(player, col):
                break
            print("Invalid input. Try again.")
        
        print_board()
        
        if check_win():
            print(f"Player {player} won!")
            break
        
        if check_draw():
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
