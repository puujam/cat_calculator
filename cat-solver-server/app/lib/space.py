from enum import IntEnum

# Rotation as clockwise mutliples of 90 degrees
class ClockRotation(IntEnum):
    twelve = 0
    three = 1,
    six = 2,
    nine = 3
    
class CardinalDirections(IntEnum):
    pos_x = 0,
    pos_y = 1,
    pos_z = 2,
    neg_x = 3,
    neg_y = 4,
    neg_z = 5

# Three Dimensional Orientation
class TDO():
    def __init__( self, x, y, z ):
        self.x = x
        self.y = y
        self.z = z

    # Gives the next possible rotation in order, 0-63
    @staticmethod
    def from_order( order ):
        if order > 63 or order < 0:
            raise Exception( "Invalid parameter. Accepts values from 0 to 63" )

        x = ClockRotation( order % 4 )
        y = ClockRotation( ( order % 16 ) // 4 )
        z = ClockRotation( order // 16 )

        return TDO( x, y, z )

    def __str__( self ):
        return "X: {} Y: {} Z: {}".format( self.x * 90, self.y * 90, self.z * 90 )

all_orientations = [ TDO.from_order( x ) for x in range( 0, 64 ) ]

# Three Dimensional Position
class TDP():
    def __init__( self, x, y, z ):
        self.x = x
        self.y = y
        self.z = z

    def __str__( self ):
        return "[ {}, {}, {} ]".format( self.x, self.y, self.z )
    
    def get_position_in_map( self, map ):
        return map[self.z][self.y][self.x]
    
    # Create a new position that is offset from this one by a given x, y, z
    def offset( self, x, y, z ):
        return TDP( self.x + x, self.y + y, self.z + z )

    def single_axis_translate( self, direction, distance ):
        if direction == CardinalDirections.pos_x:
            return self.offset( distance, 0 , 0 )
        elif direction == CardinalDirections.pos_y:
            return self.offset( 0, distance, 0 )
        elif direction == CardinalDirections.pos_z:
            return self.offset( 0, 0, distance )
        elif direction == CardinalDirections.neg_x:
            return self.offset( -1 * distance, 0, 0 )
        elif direction == CardinalDirections.neg_y:
            return self.offset( 0, -1 * distance, 0 )
        else:
            return self.offset( 0, 0, -1 * distance )

    def __eq__( self, other ):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__( self ):
        # Requires we never encounter sizes greater than 99 in any dimension, feels pretty safe for now
        return hash( "{:02d}{:02d}{:02d}".format( self.x, self.y, self.z ) )

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

def rotate_axes( start_directions, rotation_dict, rotation_amount ):
    for unused in range( 0, rotation_amount.value ):
        for direction_index in range( 0, len( start_directions ) ):
            if start_directions[direction_index] in rotation_dict:
                start_directions[direction_index] = rotation_dict[start_directions[direction_index]]
        
    return start_directions