import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the game board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ... G
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

# Check if the column is valid
def is_valid_column(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

# Place the player's checker in the selected column
def place_checker(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return True
    return False

# Check for a win
def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    return (check_horizontal(board, player) or
            check_vertical(board, player) or
            check_diagonal(board, player))

# Check horizontal win
def check_horizontal(board, player):
    for row in board:
        count = 0
        for cell in row:
            count = count + 1 if cell == player else 0
            if count >= 4:
                return True
    return False

# Check vertical win
def check_vertical(board, player):
    for col in range(COLS):
        count = 0
        for row in board:
            count = count + 1 if row[col] == player else 0
            if count >= 4:
                return True
    return False

# Check diagonal win
def check_diagonal(board, player):
    # Check for diagonals with positive slope
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row + 1][col + 1] == player and
                board[row + 2][col + 2] == player and
                board[row + 3][col + 3] == player):
                return True
    
    # Check for diagonals with negative slope
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row - 1][col + 1] == player and
                board[row - 2][col + 2] == player and
                board[row - 3][col + 3] == player):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    game_over = False

    while not game_over:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()

        if col_input.isalpha() and len(col_input) == 1:
            col = ord(col_input) - 65
            if is_valid_column(board, col):
                place_checker(board, col, current_player)
                
                if check_win(board, current_player):
                    print_board(board)
                    print(f"Player {current_player} won!")
                    game_over = True
                elif check_draw(board):
                    print_board(board)
                    print("The game is a draw!")
                    game_over = True
                else:
                    current_player_index = (current_player_index + 1) % len(PLAYERS)
            else:
                print("Invalid column, please try again.")
        else:
            print("Invalid input, please enter a letter corresponding to a column (A-G).")

if __name__ == "__main__":
    main()
