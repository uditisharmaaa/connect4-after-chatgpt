import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Default player tokens
NUMBER_OF_PLAYERS = 3  # Set the number of players to play (adjust this between 2 and 5)

# Initialize board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Display the board
def print_board(board):
    os.system('clear')
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print(" " + "--" * COLUMNS)

# Select a random player to start
def select_first_player():
    return random.choice(PLAYERS[:NUMBER_OF_PLAYERS])

# Validate player input
def get_valid_column():
    while True:
        column = input(f"Choose a column ({', '.join(COLUMN_LABELS)}): ").strip().upper()
        if column in COLUMN_LABELS:
            column_index = COLUMN_LABELS.index(column)
            if any(row[column_index] == ' ' for row in board):
                return column_index
            else:
                print("That column is full. Try another one.")
        else:
            print("Invalid column. Try again with a valid column.")

# Place the player's token in the chosen column
def drop_piece(board, column, token):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = token
            break

# Check for a win
def check_win(board, token):

    def check_direction(delta_x, delta_y):
        for x in range(ROWS):
            for y in range(COLUMNS):
                if all(
                    (0 <= x + i * delta_x < ROWS) and
                    (0 <= y + i * delta_y < COLUMNS) and
                    (board[x + i * delta_x][y + i * delta_y] == token)
                    for i in range(4)
                ):
                    return True
        return False

    return (
        check_direction(0, 1) or     # Horizontal
        check_direction(1, 0) or     # Vertical
        check_direction(1, 1) or     # Diagonal /
        check_direction(1, -1)       # Diagonal \
    )

# Check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def play_game():
    board = create_board()
    current_player = select_first_player()
    print(f"Player {current_player} starts!")

    while True:
        print_board(board)
        print(f"Player {current_player}'s turn.")
        column = get_valid_column()
        drop_piece(board, column, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Move to the next player
        current_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_index + 1) % NUMBER_OF_PLAYERS]

if __name__ == "__main__":
    play_game()
