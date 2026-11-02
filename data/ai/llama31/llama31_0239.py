import os
import random
import string

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
MIN_PLAYERS = 2
MAX_PLAYERS = 5
MAX_CHECKERS = 26

def create_board():
    """Create an empty board with the specified dimensions."""
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLUMNS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board, players_turn):
    """Print the current state of the board."""
    os.system('clear')
    print("  ", end="")
    for col in range(BOARD_COLUMNS):
        print(string.ascii_uppercase[col], end="   ")
    print()
    for row in range(BOARD_ROWS):
        print("+---" * BOARD_COLUMNS + "+")
        print("|", end="")
        for col in range(BOARD_COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * BOARD_COLUMNS + "+")
    print(f"Player {players_turn}, please enter a column:")

def get_valid_move(board, column):
    """Get the lowest available row in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return -1  # Column is full

def check_win(board, player_checker, row, col):
    """Check if the current player has won."""
    # Check horizontal locations for win
    count = 0
    for c in range(max(0, col - 3), min(BOARD_COLUMNS, col + 4)):
        if board[row][c] == player_checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check vertical locations for win
    count = 0
    for r in range(max(0, row - 3), min(BOARD_ROWS, row + 4)):
        if board[r][col] == player_checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check positively sloped diagonals
    count = 0
    for r, c in zip(range(max(0, row - 3), min(BOARD_ROWS, row + 4)), range(max(0, col - 3), min(BOARD_COLUMNS, col + 4))):
        if board[r][c] == player_checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check negatively sloped diagonals
    count = 0
    for r, c in zip(range(max(0, row - 3), min(BOARD_ROWS, row + 4)), range(max(0, col - 3), min(BOARD_COLUMNS, col + 4))):
        if board[r][BOARD_COLUMNS - c - 1] == player_checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= " " for row in board for cell in row)

def main():
    # Initialize the board and players
    board = create_board()
    players = ["X", "O", "V", "H", "M"][:random.randint(MIN_PLAYERS, MAX_PLAYERS)]
    players_turn = players[0]

    # Randomly select the first player
    first_player = random.choice(players)
    players.remove(first_player)
    players.insert(0, first_player)

    while True:
        print_board(board, players_turn)
        while True:
            column = input().strip().upper()
            if column not in string.ascii_uppercase[:BOARD_COLUMNS]:
                print("Invalid column. Please try again.")
                continue
            column = string.ascii_uppercase.index(column)
            row = get_valid_move(board, column)
            if row == -1:
                print("Column is full. Please try again.")
                continue
            board[row][column] = players_turn
            break

        # Check for a win
        if check_win(board, players_turn, row, column):
            print_board(board, players_turn)
            print(f"Player {players_turn} won!")
            break

        # Check for a draw
        if check_draw(board):
            print_board(board, players_turn)
            print("It's a draw!")
            break

        # Switch to the next player
        players_turn = players[(players.index(players_turn) + 1) % len(players)]

if __name__ == "__main__":
    main()
