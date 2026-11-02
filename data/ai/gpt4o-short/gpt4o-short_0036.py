import os
import random

# Game configuration constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUMBER_OF_PLAYERS = 3  # Change this value to set the number of players from 2 to 5

# Initialize the board
def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Draw the board
def draw_board(board):
    os.system('clear')
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|'.join(row))
        print('-' * (2 * COLUMNS - 1))

# Get player input
def get_player_input(current_player):
    while True:
        column = input(f"Player {current_player}, choose a column (A-G): ").upper()
        if column in COLUMN_LABELS:
            column_index = COLUMN_LABELS.index(column)
            if board[0][column_index] == ' ':
                return column_index
            else:
                print("The column is full. Please choose another column.")
        else:
            print("Invalid input. Please enter a column label between A to G.")

# Place the piece on the board
def place_piece(board, column, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return

# Check for win condition
def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

# Check for draw condition
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def main():
    board = initialize_board()
    current_player = random.choice(PLAYERS[:NUMBER_OF_PLAYERS])
    
    while True:
        draw_board(board)
        column = get_player_input(current_player)
        place_piece(board, column, current_player)
        
        if check_win(board, current_player):
            draw_board(board)
            print(f"Player {current_player} wins!")
            break
        
        if check_draw(board):
            draw_board(board)
            print("The game is a draw!")
            break
        
        # Cycle to the next player
        current_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_index + 1) % NUMBER_OF_PLAYERS]

if __name__ == "__main__":
    main()
