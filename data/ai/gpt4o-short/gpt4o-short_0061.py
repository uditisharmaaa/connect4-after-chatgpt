import random
import os

# Constants for players
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Set between 2 and 5

ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"

def print_board(board):
    os.system('clear')  # Use 'cls' instead of 'clear' for Windows
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("=" * (COLS * 2 + 1))

def drop_piece(board, column, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False

def is_win(board, player):
    # Check all directions: horizontal, vertical, and two diagonals
    for row in range(ROWS):
        for col in range(COLS):
            if (col <= COLS - 4 and all(board[row][c] == player for c in range(col, col + 4))) or \
               (row <= ROWS - 4 and all(board[r][col] == player for r in range(row, row + 4))) or \
               (row <= ROWS - 4 and col <= COLS - 4 and all(board[row + d][col + d] == player for d in range(4))) or \
               (row >= 3 and col <= COLS - 4 and all(board[row - d][col + d] == player for d in range(4))):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    players = PLAYERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        player = players[current_player_index]
        print(f"Player {player}'s turn.")
        
        try:
            col_input = input("Enter column (A-G): ").strip().upper()
            if col_input not in COLUMN_LABELS:
                raise ValueError
            column = COLUMN_LABELS.index(col_input)
        except ValueError:
            print("Invalid input. Choose a column between A-G.")
            continue
        
        if not drop_piece(board, column, player):
            print("Column full. Choose another one.")
            continue
        
        if is_win(board, player):
            print_board(board)
            print(f"Player {player} wins!")
            break
        elif is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
