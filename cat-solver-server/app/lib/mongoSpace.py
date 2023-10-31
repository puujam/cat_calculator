from enum import IntEnum

import copy

# Rotation as clockwise mutliples of 90 degrees
class ClockRotation(IntEnum):
    twelve = 0
    three = 1,
    six = 2,
    nine = 3

def orientation_from_order( order ):
    if order > 63 or order < 0:
        raise Exception( "Invalid parameter. Accepts values from 0 to 63" )

    x = ClockRotation( order % 4 )
    y = ClockRotation( ( order % 16 ) // 4 )
    z = ClockRotation( order // 16 )

    return ( x, y, z )

def get_all_orientations():
    return [ orientation_from_order( i ) for i in range( 0, 64 ) ]

class CardinalDirections(IntEnum):
    pos_x = 0,
    pos_y = 1,
    pos_z = 2,
    neg_x = 3,
    neg_y = 4,
    neg_z = 5

start_directions = ( CardinalDirections.pos_x, CardinalDirections.pos_y, CardinalDirections.pos_z )

x_set = set( [ CardinalDirections.pos_x, CardinalDirections.neg_x ] )
y_set = set( [ CardinalDirections.pos_y, CardinalDirections.neg_y ] )
negative_set = set( [ CardinalDirections.neg_x, CardinalDirections.neg_y, CardinalDirections.neg_z ] )

z_rotation_dict = {
    CardinalDirections.neg_y: CardinalDirections.pos_x,
    CardinalDirections.pos_x: CardinalDirections.pos_y,
    CardinalDirections.pos_y: CardinalDirections.neg_x,
    CardinalDirections.neg_x: CardinalDirections.neg_y
}

y_rotation_dict = {
    CardinalDirections.pos_z: CardinalDirections.pos_x,
    CardinalDirections.pos_x: CardinalDirections.neg_z,
    CardinalDirections.neg_z: CardinalDirections.neg_x,
    CardinalDirections.neg_x: CardinalDirections.pos_z
}

x_rotation_dict = {
    CardinalDirections.pos_z: CardinalDirections.neg_y,
    CardinalDirections.neg_y: CardinalDirections.neg_z,
    CardinalDirections.neg_z: CardinalDirections.pos_y,
    CardinalDirections.pos_y: CardinalDirections.pos_z
}

def rotate_all_axes( start_axes, orientation ):
    result = start_axes

    for axis_dict, axis_rotation in [ ( x_rotation_dict, orientation[0] ), ( y_rotation_dict, orientation[1] ), ( z_rotation_dict, orientation[2] ) ]:
        result = rotate_axis( result, axis_dict, axis_rotation )

    return result

# Directions list always in x, y, z order
def rotate_axis( start_directions, rotation_dict, rotation_amount ):
    if ( rotation_amount == 0 ):
        return start_directions

    result = list()

    for start_direction in start_directions:
        if start_direction in rotation_dict:
            # If this axis is affected, store the result
            result.append( rotation_dict[ start_direction ] )
        else:
            # Otherwise return it unmodified
            result.append( start_direction )
    
    return rotate_axis( result, rotation_dict, rotation_amount - 1 )
    
def rotate_occupied_coords( start_coords, new_axis_positions ):
    results = list()

    for coord in start_coords:
        new_coord = []

        for axis in new_axis_positions:
            if axis in x_set:
                coord_index = 0
            elif axis in y_set:
                coord_index = 1
            else:
                coord_index = 2

            if axis in negative_set:
                multiplier = -1
            else:
                multiplier = 1

            new_coord.append( multiplier * coord[ coord_index ] )
        
        results.append( tuple( new_coord ) )
    
    return results

def shift_coords_to_all_positive( start_coords ):
    results = list()
    offsets = list()

    for axis_index in range( 3 ):
        # Find the lowest value for each axis with a ceiling of 0
        offsets.append( min( [ min( [ coord[ axis_index ] for coord in start_coords ] ), 0 ] ) * -1 )
    
    for coord in start_coords:
        new_coord = list()

        for axis_index in range( 3 ):
            new_coord.append( coord[ axis_index ] + offsets[ axis_index ] )

        results.append( tuple( new_coord ) )
    
    return results

def get_all_possible_axis_positions():
    encountered_axis_sets = set()
    results = list()

    for rotation in get_all_orientations():
        positions_for_rotation = tuple( rotate_all_axes( start_directions, rotation ) )

        if positions_for_rotation not in encountered_axis_sets:
            encountered_axis_sets.add( positions_for_rotation )
            results.append( positions_for_rotation )
        
    return results

def offset_coordinate( initial, offset ):
    result = list()

    for axis in range( len( initial ) ):
        result.append( initial[ axis ] + offset[ axis ] )
    
    return tuple( result )