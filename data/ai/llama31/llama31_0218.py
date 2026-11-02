import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board(columns, rows):
    """Create a 2D board with specified columns and rows."""
    board = []
    for _ in range(rows):
        row = []
        for _ in range(columns):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A B C D E F G")
    for i, row in enumerate(board):
        print(f"+---+---+---+---+---+---+---+")
        print(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} |")
    print(f"+---+---+---+---+---+---+---+")

def get_player_input(player):
    """Get a valid column input from the current player."""
    while True:
        column = input(f"Player {player}, please enter a column (A-G): ").strip().upper()
        if column in "ABCDEFG":
            return column
        print("Invalid input. Please enter a letter between A and G.")

def place_checker(board, column, player):
    """Place the checker in the specified column."""
    column_index = ord(column) - ord("A")
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = player
            return
    print("Column is full. You lost your turn.")

def check_win(board):
    """Check if there is a winner."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3]!= " ":
                return row[i]
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col]!= " ":
                return board[i][col]
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]!= " ":
                return board[row][col]
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]!= " ":
                return board[row][col]
    return None

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board(BOARD_COLUMNS, BOARD_ROWS)
    num_players = 2
    players = PLAYERS[:num_players]
    current_player = random.choice(players)
    while True:
        print_board(board)
        column = get_player_input(current_player)
        place_checker(board, column, current_player)
        winner = check_win(board)
        if winner:
            print_board(board)
            print(f"Player {winner} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    main()
