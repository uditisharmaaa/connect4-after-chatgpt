import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']
COLUMNS = [chr(i) for i in range(ord('A'), ord('A') + COLS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join(COLUMNS[:len(board[0])])
    divider = "+---" * len(board[0]) + "+"
    print(header)
    for row in board:
        print(divider)
        print("| " + " | ".join(row) + " |")
    print(divider)

def is_valid_input(column, board):
    return column in COLUMNS[:len(board[0])] and board[0][COLUMNS.index(column)] == " "

def place_checker(board, column, player):
    col_index = COLUMNS.index(column)
    for row in reversed(board):  # Start from bottom row
        if row[col_index] == " ":
            row[col_index] = player
            break

def check_for_win(board, player):
    # Horizontal Check
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == row[col+1] == row[col+2] == row[col+3] == player:
                return True
    
    # Vertical Check
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if (board[row][col] == board[row+1][col] == 
                board[row+2][col] == board[row+3][col] == player):
                return True
    
    # Diagonal Check (left-to-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if (board[row][col] == board[row+1][col+1] == 
                board[row+2][col+2] == board[row+3][col+3] == player):
                return True

    # Diagonal Check (right-to-left)
    for row in range(len(board) - 3):
        for col in range(3, len(board[0])):
            if (board[row][col] == board[row+1][col-1] == 
                board[row+2][col-2] == board[row+3][col-3] == player):
                return True
    
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    # Set up the game
    board = create_board(ROWS, COLS)
    num_players = 2  # Change this to test with more players
    player_symbols = PLAYERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    
    print_board(board)
    print(f"Player {player_symbols[current_player_index]} starts!")
    
    while True:
        player = player_symbols[current_player_index]
        valid_turn = False
        
        while not valid_turn:
            column = input(f"Player {player}, please enter a column ({COLUMNS[0]}-{COLUMNS[len(board[0])-1]}): ").strip().upper()
            if column in COLUMNS[:len(board[0])] and is_valid_input(column, board):
                place_checker(board, column, player)
                valid_turn = True
            else:
                print("Invalid input. Please try again.")
        
        print_board(board)
        
        # Check for win or draw
        if check_for_win(board, player):
            print(f"Player {player} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
