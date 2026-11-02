import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # For 2 players

# Initialize the board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Clear console screen
def clear_screen():
    os.system('clear')

# Print the current state of the board
def print_board(board):
    clear_screen()
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

# Check for a win condition
def check_for_winner(board, player):
    def check_direction(delta_row, delta_col):
        for row in range(ROWS):
            for col in range(COLS):
                if all(0 <= row + i * delta_row < ROWS and 
                       0 <= col + i * delta_col < COLS and 
                       board[row + i * delta_row][col + i * delta_col] == player
                       for i in range(4)):
                    return True
        return False
        
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    return any(check_direction(dr, dc) for dr, dc in directions)

# Check if the board is full
def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Place the checker on the board
def place_checker(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

# Validate player's input
def valid_input(board, input_char):
    if len(input_char) != 1 or not input_char.isalpha():
        return False
    col = ord(input_char.upper()) - 65
    return 0 <= col < COLS and board[0][col] == ' '

# Main game function
def connect_4():
    board = create_board(ROWS, COLS)
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        player_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        if not valid_input(board, player_input):
            print("Invalid input. Please try again.")
            continue
        
        col = ord(player_input) - 65
        if not place_checker(board, col, current_player):
            print("Column is full. You lose this turn.")
        else:
            print_board(board)
            if check_for_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

# Start the game
if __name__ == "__main__":
    connect_4()
