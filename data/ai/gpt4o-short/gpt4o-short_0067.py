import os
import random

ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # The possible players
NUM_PLAYERS = 4  # Set between 2 to 5 players

# Ensure that NUM_PLAYERS does not exceed the number of available players
assert 2 <= NUM_PLAYERS <= len(PLAYERS)

# Select the active players
active_players = PLAYERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(['A', 'B', 'C', 'D', 'E', 'F', 'G']))
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("-" * (COLUMNS * 4 + 1))

def is_valid_move(board, column):
    return board[0][column] == ' '

def make_move(board, player, column):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return

def check_winner(board, player):
    # Check horizontal, vertical, and diagonal for a win
    # Horizontal Check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Vertical Check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Diagonal (positive slope) Check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Diagonal (negative slope) Check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = create_board()
    current_player_index = random.choice(range(NUM_PLAYERS))
    clear_screen()
    
    while True:
        clear_screen()
        print_board(board)
        
        current_player = active_players[current_player_index]
        print(f"Player {current_player}'s turn.")

        move = input("Choose a column (A-G): ").strip().upper()
        if move not in "ABCDEFG"[:COLUMNS]:
            print("Invalid input. Please choose a column label between A-G.")
            input("Press Enter to continue...")
            continue

        column = "ABCDEFG".index(move)
        if not is_valid_move(board, column):
            print("That column is full. Choose another one.")
            input("Press Enter to continue...")
            continue

        make_move(board, current_player, column)

        if check_winner(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        input("Press Enter to continue...")

if __name__ == "__main__":
    play_game()
