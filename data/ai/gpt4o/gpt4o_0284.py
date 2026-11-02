import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_COUNT = 2

# Initialize the board
def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))) + " ")
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

# Get a valid column from the player
def get_player_input(board, player):
    while True:
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        if column and column in [chr(65+i) for i in range(len(board[0]))]:
            column_index = ord(column) - 65
            if board[0][column_index] == ' ':
                return column_index
            else:
                print("Column is full. Please choose another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

# Place the checker in the correct spot
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

# Check for a win condition
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal (both directions)
    def check_direction(board, checker, start_row, start_col, delta_row, delta_col):
        count = 0
        for _ in range(4):
            if 0 <= start_row < len(board) and 0 <= start_col < len(board[0]):
                if board[start_row][start_col] == checker:
                    count += 1
                    if count == 4:
                        return True
                start_row += delta_row
                start_col += delta_col
            else:
                break
        return False

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == checker:
                # Horizontal, vertical, diagonal /
                if any(
                    check_direction(board, checker, row, col, delta_row, delta_col)
                    for delta_row, delta_col in [(0, 1), (1, 0), (1, 1), (1, -1)]
                ):
                    return True
    return False

# Check for a draw condition
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main function to run the game
def play_game():
    board = initialize_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYER_COUNT]
    current_player_index = random.randint(0, PLAYER_COUNT - 1)
    
    print_board(board)
    
    while True:
        current_player = players[current_player_index]
        column = get_player_input(board, current_player)
        place_checker(board, column, current_player)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % PLAYER_COUNT

if __name__ == '__main__':
    play_game()
