import os
import random
import string

# Constant variables
BOARD_COLUMNS = 7
BOARD_ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(columns, rows):
    """Create an empty board with the specified columns and rows."""
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board

def print_board(board):
    """Print the current state of the board."""
    columns = string.ascii_uppercase[:BOARD_COLUMNS]
    print("  " + "   ".join(columns))
    print("+---" * BOARD_COLUMNS + "+")
    for row in board:
        print("|   " * BOARD_COLUMNS + "|")
        print("| " + " | ".join(row) + " |")
        print("+---" * BOARD_COLUMNS + "+")

def get_player_input(player):
    """Get the column input from the player and validate it."""
    while True:
        column = input(f"Player {player}, please enter a column: ")
        if column in string.ascii_uppercase[:BOARD_COLUMNS]:
            return column
        print("Invalid input. Please enter a letter between A and G.")

def drop_checker(board, column, player):
    """Drop the checker into the specified column."""
    column_index = string.ascii_uppercase.index(column)
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = player
            break
    else:
        print("Column is full. Please try again.")
        return False
    return True

def check_win(board):
    """Check if there is a winner on the board."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i]!= " " and row[i] == row[i+1] == row[i+2] == row[i+3]:
                return row[i]

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col]!= " " and board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col]:
                return board[i][col]

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col]!= " " and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                return board[row][col]

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col]!= " " and board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                return board[row][col]

    return None

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= " " for row in board for cell in row)

def game():
    """Run the game."""
    os.system('clear')
    board = create_board(BOARD_COLUMNS, BOARD_ROWS)
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        column = get_player_input(current_player)
        if drop_checker(board, column, current_player):
            winner = check_win(board)
            if winner:
                print_board(board)
                print(f"Player {winner} won!")
                break
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    game()
