import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2

# Mapping player index to checker symbol
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates and returns an empty board with the given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    columns_label = "  " + "   ".join(chr(i) for i in range(ord('A'), ord('A') + len(board[0])))
    print(columns_label)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def valid_move(board, column):
    """Checks if a move in the given column is valid."""
    return 0 <= column < len(board[0]) and board[0][column] == " "

def make_move(board, column, checker):
    """Places the checker in the correct position in the column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_winner(board, players):
    """Checks if there is a winner."""
    rows, cols = len(board), len(board[0])

    def check_four_in_a_row(checker):
        # Check horizontal
        for r in range(rows):
            for c in range(cols - 3):
                if all(board[r][c + i] == checker for i in range(4)):
                    return True
        
        # Check vertical
        for c in range(cols):
            for r in range(rows - 3):
                if all(board[r + i][c] == checker for i in range(4)):
                    return True
        
        # Check diagonals (bottom-left to top-right)
        for r in range(rows - 3):
            for c in range(cols - 3):
                if all(board[r + i][c + i] == checker for i in range(4)):
                    return True
        
        # Check diagonals (top-left to bottom-right)
        for r in range(3, rows):
            for c in range(cols - 3):
                if all(board[r - i][c + i] == checker for i in range(4)):
                    return True
        
        return False

    # Check all players
    for i in range(players):
        if check_four_in_a_row(CHECKERS[i]):
            return CHECKERS[i]

    return None

def check_draw(board):
    """Checks if the board is filled and it's a draw."""
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    num_players = NUM_PLAYERS
    current_player = random.randint(0, num_players - 1)
    
    clear_screen()
    print_board(board)
    
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        
        while True:
            try:
                column_letter = input().upper()
                column = ord(column_letter) - ord('A')
                if valid_move(board, column):
                    break
                else:
                    print("Invalid move, please try again.")
            except (IndexError, ValueError):
                print("Invalid input, please enter a valid column letter.")
        
        make_move(board, column, CHECKERS[current_player])
        clear_screen()
        print_board(board)
        
        winner = check_winner(board, num_players)
        if winner:
            print(f"Player {winner} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
