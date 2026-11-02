import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    # Check if the input is a valid column
    if len(column) == 1 and column.isalpha():
        col_index = ord(column.upper()) - 65
        if 0 <= col_index < COLUMNS and board[0][col_index] == " ":
            return True
    return False

def place_checker(board, col, checker):
    col_index = ord(col.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False

def check_winner(board, row, col, checker):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_last_position(board, column):
    col_index = ord(column.upper()) - 65
    for r in range(ROWS):
        if board[r][col_index] != " ":
            return r, col_index
    return ROWS - 1, col_index

def main():
    board = create_board()
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player_index = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    print(f"Player {players[current_player_index]} starts!")
    
    while True:
        current_player = players[current_player_index]
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        column = input().strip().upper()
        
        # Validate input
        while not is_valid_column(column, board):
            print("Invalid column. Try again:")
            column = input().strip().upper()
        
        # Place checker
        place_checker(board, column, current_player)
        
        # Check for a winner
        row, col = get_last_position(board, column)
        if check_winner(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
