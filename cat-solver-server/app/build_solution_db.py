from lib import db
from lib import mongoPuzzle
from lib import mongoSpace

import multiprocessing
import copy

db_handle = db.get_db_handle()

for puzzle_data in db_handle.puzzles.find():
    puzzle = mongoPuzzle.Puzzle( puzzle_data )

    if puzzle.solutions:
        print( "{} puzzle {} already has solutions calculated. It has {} solutions.".format( puzzle.animal_type, puzzle.number, len( puzzle.solutions ) ) )
    else:
        print( "Finding solutions for {} puzzle {}...".format( puzzle.animal_type, puzzle.number ), end = "" )
        # We create a process per animal for multithreading
        for animal in puzzle.animals:

def find_solutions( placed_animals, animals_to_place, available_spaces ):
    for space in available_spaces:
        for animal in animals_to_place:
           for occupied_positions in animal.unique_positions:
               offset_positions = { mongoSpace.offset_position(  ) } 