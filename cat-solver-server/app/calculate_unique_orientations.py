from lib import mongoAnimal
from lib import mongoSpace
from lib import db

mongo = db.get_db_handle()
all_possible_axis_positions = mongoSpace.get_all_possible_axis_positions()
all_possible_rotations = mongoSpace.get_all_orientations()

for animal_type in [ "dog", "cat" ]:
    for animal in mongoAnimal.get_all_animals( mongo, animal_type ):
        if not animal.unique_positions:
            unique_position_sets = list() # List of unique position sets

            for axis_positions in all_possible_axis_positions:
                occupied_positions = mongoSpace.rotate_occupied_coords( animal.base_positions, axis_positions )

                all_positive = mongoSpace.shift_coords_to_all_positive( occupied_positions )
                occupied_set = set( tuple( all_positive ) )

                if occupied_set not in unique_position_sets:
                    unique_position_sets.append( occupied_set )
            
            print( "{} {} was calculated to have {} unique orientations!".format( animal.name, animal_type, len( unique_position_sets ) ) )

            animal.assign_unique_positions( mongo, unique_position_sets )
        else:
            print( "{} {} already has orientations calculated. It has {} unique orientations.".format( animal.name, animal_type, len( animal.unique_positions ) ) )