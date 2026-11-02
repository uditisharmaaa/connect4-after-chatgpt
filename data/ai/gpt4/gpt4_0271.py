import os
import random

# Global constants for board size and players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Default is 2 players; can adjust in other implementations

def create_board():
    """Creates a new empty game board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board with column labels."""
    os.system('clear')
    print("\n  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    """Checks if a column input is valid."""
    if len(column) != 1 or not column.isalpha():
        return False
    col_idx = ord(column.upper()) - 65
    return 0 <= col_idx < COLUMNS and board[0][col_idx] == " "

def drop_checker(board, column, checker):
    """Places a player's checker in the selected column."""
    col_idx = ord(column.upper()) - 65
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx

def check_winner(board, row, col, checker):
    """Checks if the latest move wins the game."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for step in range(1, 4):  # Check in one direction
            r, c = row + dr * step, col + dc * step
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                count += 1
            else:
                break
        for step in range(1, 4):  # Check in the opposite direction
            r, c = row - dr * step, col - dc * step
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                count += 1
            else:
                break
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Checks if the board is completely filled."""
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    random.shuffle(players)
    turn = 0
    winner = None

    print_board(board)
    print(f"Player {players[0]} goes first!\n")

    while not winner and not is_draw(board):
        current_player = players[turn % NUM_PLAYERS]
        while True:
            column = input(f"Player {current_player}, please enter a column: ").strip()
            if is_valid_column(column, board):
                break
            print("Invalid input. Try again.")

        row, col = drop_checker(board, column, current_player)
        print_board(board)

        if check_winner(board, row, col, current_player):
            winner = current_player
        else:
            turn += 1

    if winner:
        print(f"Player {winner} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
