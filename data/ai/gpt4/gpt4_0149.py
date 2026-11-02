import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print board
def print_board(board):
    os.system('clear')
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(NUM_COLS))
    print(col_labels)
    print("+---" * NUM_COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLS + "+")

# Check for win conditions
def check_win(board, marker):
    # Horizontal check
    for row in board:
        if any(row[c:c+4] == [marker] * 4 for c in range(NUM_COLS - 3)):
            return True
    
    # Vertical check
    for c in range(NUM_COLS):
        column = [board[r][c] for r in range(NUM_ROWS)]
        if any(column[r:r+4] == [marker] * 4 for r in range(NUM_ROWS - 3)):
            return True
    
    # Diagonal (\) and (/) check
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            if all(board[r+i][c+i] == marker for i in range(4)) or \
               all(board[r+3-i][c+i] == marker for i in range(4)):
                return True
    return False

# Check if board is full
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def connect4():
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_MARKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    while True:
        print(f"Player {players[current_player]}, please enter a column:")
        col_input = input().strip().upper()
        
        if len(col_input) != 1 or col_input < 'A' or col_input >= chr(65 + NUM_COLS):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col = ord(col_input) - 65
        if board[0][col] != " ":
            print("Column is full. Please choose another column.")
            continue

        # Drop the checker
        for row in range(NUM_ROWS-1, -1, -1):
            if board[row][col] == " ":
                board[row][col] = players[current_player]
                break

        print_board(board)

        # Check for win/draw
        if check_win(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect4()
