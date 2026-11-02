import os
import random

# Constants for the game
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen.
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)  # Print top border
    
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print each row
        print("+" + "---+" * COLS)  # Print border after each row

def get_column_input(player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").upper()
        if len(col_input) == 1 and 'A' <= col_input <= chr(65 + COLS - 1):
            col = ord(col_input) - 65
            return col
        print("Invalid input. Please enter a column letter from A to " + chr(65 + COLS - 1))

def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    # Check horizontal, vertical and diagonal (both directions) for a win
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                if check_direction(board, r, c, 0, 1, checker) or \
                   check_direction(board, r, c, 1, 0, checker) or \
                   check_direction(board, r, c, 1, 1, checker) or \
                   check_direction(board, r, c, 1, -1, checker):
                    return True
    return False

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    for i in range(4):
        r = start_row + delta_row * i
        c = start_col + delta_col * i
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            break
    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board()
    players = PLAYERS[:2]  # Adjust this for 2 players
    current_player = random.choice(players)  # Randomly select first player
    
    print_board(board)
    
    while True:
        col = get_column_input(current_player)
        
        if drop_checker(board, col, current_player):
            print_board(board)  # Print board after dropping the checker
            
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if check_draw(board):
                print("The game is a draw!")
                break
            
            # Switch players
            current_player = players[(players.index(current_player) + 1) % len(players)]
        else:
            print("Column is full, please try another column.")

if __name__ == '__main__':
    main()
