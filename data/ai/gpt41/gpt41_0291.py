import os
import random
import string

# ---- Constants ----
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2  # use between 2-5
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

# ---- Utility Functions ----

def clear_screen():
    os.system('clear')

def print_board(board, columns):
    col_labels = "  " + "   ".join(string.ascii_uppercase[:columns])
    print()
    print(col_labels)
    print("+" + "---+" * columns)
    for row in board:
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
        print("+" + "---+" * columns)
    print()

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def is_valid_column(user_input, columns):
    if len(user_input) != 1:
        return False
    if user_input not in string.ascii_uppercase[:columns]:
        return False
    return True

def get_column_index(user_input):
    return string.ascii_uppercase.index(user_input)

def is_column_full(board, col):
    return all(board[row][col] != " " for row in range(ROWS))

def place_checker(board, col, checker):
    # Start from bottom row and go up to find the first empty spot
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Should not happen if checked before

def check_winner(board, checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + offset] == checker for offset in range(4)):
                return True

    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + offset][col] == checker for offset in range(4)):
                return True

    # Diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + offset][col + offset] == checker for offset in range(4)):
                return True

    # Diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - offset][col + offset] == checker for offset in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def select_first_player(num_players):
    return random.randint(0, num_players - 1)

# ---- Main Game ----
def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_TOKENS[:NUM_PLAYERS]
    player_names = [f"Player {token}" for token in players]

    current_player = select_first_player(NUM_PLAYERS)
    
    clear_screen()
    print_board(board, COLUMNS)
    print(f"{player_names[current_player]} ({players[current_player]}) starts!\n")

    while True:
        current_token = players[current_player]
        player_label = player_names[current_player]

        # Get a valid move
        while True:
            user_input = input(f"{player_label} ({current_token}), please enter a column: ").strip().upper()
            if not is_valid_column(user_input, COLUMNS):
                print(f"Invalid input. Please enter a letter from A to {string.ascii_uppercase[COLUMNS-1]}.")
                continue

            col = get_column_index(user_input)
            if is_column_full(board, col):
                print("Column is full. You lose your turn.")
                break  # Lose turn if column is full
            else:
                place = place_checker(board, col, current_token)
                break

        clear_screen()
        print_board(board, COLUMNS)
        
        # If the column was full and player lost the turn, don't check for win
        if is_column_full(board, col) and board[0][col] != current_token:
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Check if current move wins the game
        if check_winner(board, current_token):
            print(f"{player_label} ({current_token}) won!")
            break

        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
