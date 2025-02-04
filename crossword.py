"""
Clue Objects contain the answer, clue, and indices of each word
in the crossword and are stored in the Crossword Object via a
dictionary. The dictionary has a portion which is written over by
the guesses of the user
"""

import csv

CROSSWORD_DIMENSION = 5

GUESS_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"


class Clue:
    def __init__(self, indices, down_across, answer, clue):
        """
        Puzzle clue constructor
        :param indices: row,column indices of the first letter of the answer
        :param down_across: A for across, D for down
        :param answer: The answer to the clue
        :param clue: The clue description
        """
        self.indices = indices
        self.down_across = down_across
        self.answer = answer
        self.clue = clue

    def __str__(self):
        """
        Return a representation of the clue (does not include the answer)
        :return: String representation of the clue
        """
        return f"{self.indices} {'Across' if self.down_across == 'A' else 'Down'}: {self.clue}"

    def __repr__(self):
        """
        Return a representation of the clue including the answer
        :return: String representation of the clue
        """
        return str(self) + f" --- {self.answer}"

    def __lt__(self, other):
        """
        Returns true if self should come before other in order. Across clues come first,
        and within each group clues are sorted by row index then column index
        :param other: Clue object being compared to self
        :return: True if self comes before other, False otherwise
        """
        return ((self.down_across,) + self.indices) < ((other.down_across,) + other.indices)


class Crossword:
    def __init__(self, filename):
        """
        Crossword constructor
        :param filename: Name of the csv file to load from. If a file with
        this name cannot be found, a FileNotFoundError will be raised
        """
        self.clues = dict()
        self.board = [['■' for _ in range(CROSSWORD_DIMENSION)] for __ in range(CROSSWORD_DIMENSION)]
        self._load(filename)

    def _load(self, filename):
        """
        Load a crossword puzzle from a csv file
        :param filename: Name of the csv file to load from
        """
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                indices = tuple(map(int, (row['Row Index'], row['Column Index'])))
                down_across, answer = row['Down/Across'], row['Answer']
                clue_description = row['Clue']
                clue = Clue(indices, down_across, answer, clue_description)

                key = indices + (down_across,)
                self.clues[key] = clue

                i = 0
                while i < len(answer):
                    if down_across == 'A':
                        self.board[indices[0]][indices[1] + i] = '_'
                    else:
                        self.board[indices[0] + i][indices[1]] = '_'
                    i += 1

    def __str__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        board_str = '     ' + '    '.join([str(i) for i in range(CROSSWORD_DIMENSION)])
        board_str += "\n  |" + "-"*(6*CROSSWORD_DIMENSION - 3) + '\n'
        for i in range(CROSSWORD_DIMENSION):
            board_str += f"{i} |"
            for j in range(CROSSWORD_DIMENSION):
                board_str += f"  {self.board[i][j]}  "
            board_str += '\n'

        return board_str

    def __repr__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        return str(self)

    def change_guess(self, clue, new_guess):
        """
        Adds the user's guess to the specific column and row while assuring the
        guess is valid without errors.
        :param clue: The specific location that will be written over
        :param new_guess: String that will be written
        :return: Modified crossword or errors if encountered
        """
        if len(new_guess) != len(clue.answer):
            raise RuntimeError("Guess length does not match the length of the clue.\n")

        for letter in new_guess:
            if letter not in GUESS_CHARS:
                raise RuntimeError("Guess contains invalid characters.\n")

        i = 0
        while i < len(clue.answer):
            if clue.down_across == 'A':
                self.board[clue.indices[0]][clue.indices[1] + i] = new_guess[i]
            else:
                self.board[clue.indices[0] + i][clue.indices[1]] = new_guess[i]
            i += 1

        return

    def reveal_answer(self, clue):
        """
        uses the crossword object's clues dictionary to find the specific clue and answer
        and overwrites the answer to the proper indexes
        :param clue: The location that will be written over
        :return: Modified crossword
        """

        i = 0
        while i < len(clue.answer):
            if clue.down_across == 'A':
                self.board[clue.indices[0]][clue.indices[1] + i] = clue.answer[i]
            else:
                self.board[clue.indices[0] + i][clue.indices[1]] = clue.answer[i]
            i += 1
        return

    def find_wrong_letter(self, clue):
        """
        Compares the clues answer to the answer provided in the crossword to determine
        where the letters are not correct
        :param clue: The clue object that will be written over
        :return: The index of the first letter error in the word position
        """
        i = 0
        while i < len(clue.answer):
            if clue.down_across == 'A':
                if self.board[clue.indices[0]][clue.indices[1] + i] != clue.answer[i]:
                    return i

            else:
                if self.board[clue.indices[0] + i][clue.indices[1]] != clue.answer[i]:
                    return i
            i += 1
        return -1


    def is_solved(self):
        """
        goes through the rows of the columns to determine if the puzzle has any errors
        :return: True if the puzzle is completed without errors, else return false
        """
        for item in self.clues:
            i = 0
            while i < len(self.clues[item].answer):
                if self.clues[item].down_across == 'A':
                    if self.board[self.clues[item].indices[0]][self.clues[item].indices[1] + i] != self.clues[item].answer[i]:
                        return False
                elif self.clues[item].down_across == 'D':
                    if self.board[self.clues[item].indices[0] + i][self.clues[item].indices[1]] != self.clues[item].answer[i]:
                        return False
                i += 1
        return True