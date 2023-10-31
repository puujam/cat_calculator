from map import Map
import space

def get_all_dogs( db ):
    dogs_data = db.cat_calculator.animals.find( { "type": "dog" } )

    return [ Animal( dog ) for dog in dogs_data ]

class Animal(Map):
    def __init__( self, data ):
        self._data = data

        if not self._data["footprint"][0][0]:
            raise Exception( "[0][0] of all animals MUST be occupied due to an optimization in the algorithm, you fuckwit. Rotate the animal data to make this true or fuck clean off." )

        self.name = self._data[ "name" ]

        # Animals are always 1 layer deep
        super().__init__( self._data[ "footprint" ], 1 )
    
    @property
    def unique_orientations( self ):
        return [ unique_orientation in self._data[ "unique_orientations" ]:
            

    def orient( self, tdo ):
        return OrientedAnimal( self.layers, self.name, tdo )
    
    def find_unique_orientations( self ):
        self.unique_orientations = dict()
        unique_position_sets = list()

        for orientation in space.all_orientations:
            oriented = self.orient( orientation )

            # We now have to shift the output points so that they all fit within the positive x, y, and z
            min_coords = list()
            for attr in [ "x", "y", "z" ]:
                min_coords.append( min( [ getattr( p, attr ) for p in oriented.occupied_positions ] ) )

            coord_shifts = list()
            for min_val in min_coords:
                if min_val < 0:
                    coord_shifts.append( -1 * min_val )
                else:
                    coord_shifts.append( 0 )

            shifted_positions = list()
            for position in oriented.occupied_positions:
                shifted_positions.append( position.offset( coord_shifts[0], coord_shifts[1], coord_shifts[2] ) )
            
            shifted_set = set( shifted_positions )
            if shifted_set in unique_position_sets:
                # This orientation is not unique, skip it
                continue
            
            unique_position_sets.append( shifted_set )

            # Store the occupied positions
            self.unique_orientations[ orientation ] = oriented
        
        print( "{} has {} unique orientations!".format( self.name, len( self.unique_orientations ) ) )

class OrientedAnimal(Animal):
    def __init__( self, layers, name, tdo ):
        self.layers = layers
        self.name = name
        self.tdo = tdo

        self._get_occupied_positions()

    # Return a list of all TDPs occupied by this animal in its chosen position
    def _get_occupied_positions( self ):
        # Some comments to aid in understanding all of this:
        # Example with the blue dog:
        #       0   1   2   3   <-- Column
        #   0       *       
        #   1   *   *
        #   2       *   *   *
        #   ^- Row
        #
        # To place this 2D map into 3D space, we use orientation as a set of 90 degree 
        # rotations on all 3 axes. We then offset those positions by a set of 3D
        # coordinates as a start position. We parse the orientation to figure out
        # what axis to increment/decrement as the row/column increment through the 2D
        # map. This code is a mess and probably very inefficient, but it's the best
        # thing I could come up with.

        # First index represents "row" axis, second represents "column"
        axes = [ space.CardinalDirections.pos_y, space.CardinalDirections.pos_x ]

        for rotation, axis in [ ( self.tdo.x, space.x_rotation_dict ), ( self.tdo.y, space.y_rotation_dict ), ( self.tdo.z, space.z_rotation_dict ) ]:
            axes = space.rotate_axes( axes, axis, rotation )
        
        # Axes now represent where the rows and columns will extend
        self.occupied_positions = list()
        origin_tdp = space.TDP( 0, 0, 0 )

        row_axis = axes[0]
        column_axis = axes[1]

        #print( "Row Axis: {}".format( row_axis ) )
        #print( "Column Axis: {}".format( column_axis ) )
        #print( "Origin Point: {}".format( self.tdp ) )

        for row_index in range( 0, len( self.layers[0] ) ):

            # Reset our position for every row
            row_start = origin_tdp.single_axis_translate( row_axis, row_index )
            #print( "Row Index: {} Row Start: {}".format( row_index, row_start ) )

            for column_index in range( 0, len( self.layers[0][row_index] ) ):
                #print( "Row: {} Column: {}".format( row_index, column_index ) )

                # If we occupy this space
                if self.layers[0][row_index][column_index]:
                    self.occupied_positions.append( row_start.single_axis_translate( column_axis, column_index ) )

    def position( self, tdp ):
        return PositionedAnimal( self.layers, self.name, tdp, self.tdo, self.occupied_positions )

class PositionedAnimal(Animal):
    def __init__( self, layers, name, tdp, tdo, origin_positions ):
        self.layers = layers
        self.name = name
        self.tdp = tdp
        self.tdo = tdo

        # Pre-cache our occupied positions
        self.occupied_positions = [ p.offset( tdp.x, tdp.y, tdp.z ) for p in origin_positions ]

dogs = [
    Animal( "aqua", [
        [ True,     False,  False,  False   ],
        [ True,     True,   True,   True    ],
        [ True,     True,   True,   True    ],
        [ True,     False,  False,  True    ]
    ] ),
    Animal( "blue", [
        [ True,     True,   True,   False   ],
        [ False,    False,  True,   True    ],
        [ False,    False,  True,   False   ]
    ] ),
    Animal( "dark gray", [
        [ True,     True,   True    ],
        [ True,     False,  False   ]
    ] ),
    Animal( "orange", [
        [ True,     True,   False,  False   ],
        [ False,    True,   True,   True    ],
        [ False,    True,   True,   True    ]
    ] ),
    Animal( "navy", [
        [ True,     True    ],
        [ True,     True    ]
    ] ),
    Animal( "red", [
        [ True,     False,  False    ],
        [ True,     True,   True    ],
        [ True,     True,   True    ]
    ] ),
    Animal( "light gray", [
        [ True,     True    ]
    ] ),
    Animal( "maroon", [
        [ True,     True    ],
        [ True,     False   ]
    ] ),
    Animal( "forest green", [
        [ True,     True,   False   ],
        [ True,     True,   True    ],
        [ True,     True,   True    ]
    ] ),
    Animal( "lime green", [
        [ True,     True,   True    ]
    ] )
]

dog_dict = dict()

for dog in dogs:
    dog_dict[dog.name] = dog
