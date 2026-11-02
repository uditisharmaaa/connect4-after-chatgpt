import os
import random

# Game configuration
NUM_ROWS = 6
NUM_COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Maximum number of players is 5, ensure game only runs with 2-5 players
assert 2 <= len(PLAYERS) <= 5, "You must have between 2 to 5 players."

# Initialize the game board
board = [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board(board):
    os.system('clear') # Clear the console
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|'.join(row) + '|')
    print('-' * (NUM_COLUMNS * 2 - 1))

def drop_piece(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return True
    return False

def is_valid_move(board, col):
    return 0 <= col < NUM_COLUMNS and board[0][col] == ' '

def check_winner(board, player):
    # Check horizontal locations for win
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] == player and all(board[row][col+i] == player for i in range(4)):
                return True

    # Check vertical locations for win
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] == player and all(board[row+i][col] == player for i in range(4)):
                return True

    # Check positively sloped diagonals
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] == player and all(board[row+i][col+i] == player for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] == player and all(board[row-i][col+i] == player for i in range(4)):
                return True

    return False

def is_board_full(board):
    return all(board[0][col] != ' ' for col in range(NUM_COLUMNS))

def play_game():
    # Randomize the starting player
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    total_turns = 0

    while True:
        print_board(board)

        # Display whose turn it is
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}'s turn.")

        # Ask for player input
        move = input(f"Choose a column (A-G) to drop your piece: ").upper()

        if move in COLUMN_LABELS:
            col = COLUMN_LABELS.index(move)
            if is_valid_move(board, col):
                drop_piece(board, col, current_player)
                total_turns += 1

                # Check for a win
                if check_winner(board, current_player):
                    print_board(board)
                    print(f"Player {current_player} wins!")
                    break

                # Check for a draw
                if is_board_full(board):
                    print_board(board)
                    print("It's a draw!")
                    break

                # Switch to next player
                current_player_index = (current_player_index + 1) % len(PLAYERS)
            else:
                print("Column is full. Choose another column.")
        else:
            print("Invalid input. Please choose a column from A to G.")

if __name__ == "__main__":
    play_game()
