import random
import os

# Constants for the game
ROWS =6COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create a new board with the given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)) + "  ")
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_column(board, player):
"Get a valid column input from the player."  while True:
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(column) != 1 or not 'A' <= column <= chr(64 + COLS):
            print("Invalid column. Please try again.")
        else:
            col_index = ord(column) - 65
            if board[0][col_index] != " ":
                print("Column is full. Please try again.")
            else:
                return col_index

def drop_checker(board, col_index, player):
    """Drop a checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player
            return row, col_index

def check_win(board, last_row, last_col, player):
    """Check if the last move resulted in a win."""
    # Check horizontal
    for col in range(max(0, last_col - 3), min(COLS -3, last_col + 1)):
        if all(board[last_row][col + i] == player for i in range(4)):
            return True

    # Check vertical
    for row in range(max(0, last_row - 3), last_row):
        if all(board[row + i][last_col] == player for i in range(4)):
            return True

    # Check diagonal (bottom-left to top-right)
    for row, col in zip(range(last_row, min(ROWS, last_row + 4)), range(last_col, min(COLS, last_col + 4))):
        if all(board[row - i][col - i] == player for i in range(4) if 0<= row - i < ROWS and 0<= col - i < COLS):
            return True

    # Check diagonal (top-left to bottom-right)
    for row, col in zip(range(last_row, max(-1, last_row - 4), -1), range(last_col, min(COLS, last_col + 4))):
        if all(board[row + i][col - i] == player for i in range(4) if 0<= row + i < ROWS and 0<= col - i < COLS):
            return True

    return False

def check_draw(board):
    """Check if the board is full resulting in a draw."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    """Main function to run the Connect4game."
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        player = players[current_player_index]
        col_index = get_valid_column(board, player)
        last_row, last_col = drop_checker(board, col_index, player)
        print_board(board)
        
        if check_win(board, last_row, last_col, player):
            print(f"Player {player} won!")
            break
        
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
