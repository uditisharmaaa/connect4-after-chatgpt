import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYER_NAMES = ['X', 'O', 'V', 'H', 'M']
EMPTY_SPACE = ' '

# Initialize the board
def create_board():
    return [[EMPTY_SPACE] * COLUMNS for _ in range(ROWS)]

# Print the board
def print_board(board):
    print('  A B C D E F G')
    for row in board:
        print('  ' + ' '.join(row))
    print()

# Clear the console screen
def clear_screen():
    os.system('clear')

# Check if a move is valid
def is_valid_move(board, col):
    return board[0][col] == EMPTY_SPACE

# Place a piece in the board
def make_move(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY_SPACE:
            board[row][col] = player
            return

# Check for a win
def check_winner(board, player):
    # Check horizontal locations
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical locations
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

# Check if the board is full
def is_draw(board):
    return all(board[0][col] != EMPTY_SPACE for col in range(COLUMNS))

# Convert column letter to index
def column_letter_to_index(letter):
    return ord(letter.upper()) - ord('A')

# Main game function
def play_game(number_of_players):
    board = create_board()
    current_player_index = random.randint(0, number_of_players - 1)
    
    while True:
        clear_screen()
        print_board(board)
        print(f"Player {PLAYER_NAMES[current_player_index]}'s turn")

        # Get valid move from player
        move = input("Choose a column (A-G): ").upper()
        
        if len(move) != 1 or move not in 'ABCDEFG':
            print("Invalid input. Please enter a letter between A and G.")
            continue

        col = column_letter_to_index(move)

        if not is_valid_move(board, col):
            print("Column full. Please choose another column.")
            continue

        # Make move and check game status
        make_move(board, col, PLAYER_NAMES[current_player_index])

        if check_winner(board, PLAYER_NAMES[current_player_index]):
            clear_screen()
            print_board(board)
            print(f"Player {PLAYER_NAMES[current_player_index]} wins!")
            break
        
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % number_of_players

# Set number of players
NUMBER_OF_PLAYERS = 3  # Change this to 2, 3, 4, or 5

# Start the game
play_game(NUMBER_OF_PLAYERS)
