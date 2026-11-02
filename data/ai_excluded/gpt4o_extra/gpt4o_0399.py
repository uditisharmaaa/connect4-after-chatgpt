import random
import os

# Constants for the game settings
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
MAX_COLUMN = chr(ord('A') + NUM_COLS - 1)
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Initialize the board
def create_board():
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# Print the current state of the board
def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(c) for c in range(ord('A'), ord('A') + NUM_COLS))
    print(header)
    for row in board:
        print("+---" * NUM_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * NUM_COLS + "+")

# Check for a valid column input
def is_valid_column(column):
    return len(column) == 1 and 'A' <= column <= MAX_COLUMN

# Check if a column is not full
def is_column_not_full(board, col):
    return board[0][col] == " "

# Drop the checker into the specified column
def drop_checker(board, col, checker):
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            break

# Check for a horizontal win
def check_horizontal_win(board, player_checkers):
    for row in board:
        for col in range(NUM_COLS - 3):
            if all(row[col+i] in player_checkers for i in range(4)):
                return True
    return False

# Check for a vertical win
def check_vertical_win(board, player_checkers):
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if all(board[row+i][col] in player_checkers for i in range(4)):
                return True
    return False

# Check for a diagonal win
def check_diagonal_win(board, player_checkers):
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row+i][col+i] in player_checkers for i in range(4)):
                return True
        for col in range(3, NUM_COLS):
            if all(board[row+i][col-i] in player_checkers for i in range(4)):
                return True
    return False

# Check for a win condition
def check_win(board, player_checkers):
    return (
        check_horizontal_win(board, player_checkers) or 
        check_vertical_win(board, player_checkers) or 
        check_diagonal_win(board, player_checkers)
    )

# Check for a draw condition
def check_draw(board):
    return all(board[0][col] != " " for col in range(NUM_COLS))

# Main game loop
def play_game():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    player_checkers = [CHECKERS[i] for i in range(NUM_PLAYERS)]

    print_board(board)
    
    while True:
        current_player_checker = player_checkers[current_player_index]
        print(f"Player {current_player_checker}, please enter a column: ", end="")
        column_input = input().strip().upper()

        if not is_valid_column(column_input):
            print("Invalid input. Please select a valid column.")
            continue

        column_index = ord(column_input) - ord('A')

        if not is_column_not_full(board, column_index):
            print("This column is full. You lose your turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        drop_checker(board, column_index, current_player_checker)
        print_board(board)

        if check_win(board, player_checkers):
            print(f"Player {current_player_checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
