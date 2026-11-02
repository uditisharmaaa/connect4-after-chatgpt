import os
import random

# Constants representing the players
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Function to clear the screen
def clear_screen():
    os.system('clear')

# Initialize the game board
def create_board():
    return [[' ' for _ in range(7)] for _ in range(6)]

# Display the board
def display_board(board):
    clear_screen()
    print('  A   B   C   D   E   F   G')
    print('+---+---+---+---+---+---+---+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---+---+---+---+---+---+---+')

# Check for a win
def check_win(board, player):
    # Check horizontal
    for row in range(6):
        for col in range(4):
            if all(board[row][col+i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(7):
        for row in range(3):
            if all(board[row+i][col] == player for i in range(4)):
                return True

    # Check positive diagonal
    for row in range(3):
        for col in range(4):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True

    # Check negative diagonal
    for row in range(3, 6):
        for col in range(4):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Get the column index from user input
def get_column():
    while True:
        col = input("Choose a column (A-G): ").strip().upper()
        if col in 'ABCDEFG':
            return ord(col) - ord('A')
        print("Invalid input. Please choose a column from A to G.")

# Place the player's piece on the board
def make_move(board, player):
    col = get_column()
    for row in reversed(range(6)):
        if board[row][col] == ' ':
            board[row][col] = player
            return
    print("Column full. Choose another column.")
    make_move(board, player)

def play_game():
    # Determine number of players
    while True:
        num_players = input("Enter the number of players (2 to 5): ").strip()
        if num_players.isdigit() and 2 <= int(num_players) <= 5:
            num_players = int(num_players)
            break
        print("Invalid number of players. Please enter a number between 2 and 5.")

    board = create_board()
    current_player = random.choice(PLAYERS[:num_players])
  
    while True:
        display_board(board)
        print(f"Player {current_player}'s turn")
        make_move(board, current_player)

        if check_win(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            break
        if check_draw(board):
            display_board(board)
            print("The game is a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    play_game()
