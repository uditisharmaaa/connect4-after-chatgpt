import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")

def is_valid_input(col_input, board):
    """Check if the input column is valid."""
    if len(col_input) != 1 or not col_input.isalpha():
        return False
    col_index = ord(col_input.upper()) - 65
    return 0 <= col_index < COLS and board[0][col_index] == ' '

def get_column_choice(player, board):
    """Get a valid column choice from the player."""
    while True:
        choice = input(f"Player {player}, please enter a column: ").strip().upper()
        if is_valid_input(choice, board):
            return ord(choice) - 65
        print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col, checker):
    """Place the checker in the chosen column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full and the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    current_player = PLAYERS[current_player_index]

    print_board(board)
    
    while True:
        col = get_column_choice(current_player, board)
        if drop_checker(board, col, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            
            # Move to the next player
            current_player_index = (current_player_index + 1) % len(PLAYERS)
            current_player = PLAYERS[current_player_index]
        else:
            print("Column is full. Please choose another column.")

if __name__ == "__main__":
    main()
