from enum import Enum
from map import Map
from animals import dog_dict
import solution

class AnimalType( Enum ):
    dog = 1,
    cat = 2

animal_type_mapping = {
    "dog": AnimalType.dog,
    "cat": AnimalType.cat
}

class Puzzle():
    def __init__( self, json ):
        self.map = Map( json["footprint"], json["layers"] )
        self.animal_type = animal_type_mapping[ json["animalType"] ]
        self.animals = list()

        for animal_name in json[ "animals" ]:
            if self.animal_type == AnimalType.dog:
                self.animals.append( dog_dict[animal_name] )
            # TODO: cats here

    def solve( self ):
        if not self.valid():
            print( "No valid solutions!" )
            return []

        return solution.find_all_solutions( self.map, self.animals )

    def valid( self ):
        spaces_to_fill = len( self.map.available_positions() )

        animal_spaces = 0
        for animal in self.animals:
            animal_spaces = animal_spaces + len( animal.available_positions() )
        
        return spaces_to_fill == animal_spaces