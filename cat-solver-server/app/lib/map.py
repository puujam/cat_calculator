import copy

from space import TDP

class Map():
    def __init__( self, first_layer, depth ):
        # Find the extreme left and right dimensions
        leftmost = 99
        rightmost = 0
        uppermost = 99
        lowermost = 0

        row_index = 0

        for row in first_layer:
            column_index = 0

            if any( row ):
                if row_index < uppermost:
                    uppermost = row_index
                
                if row_index > lowermost:
                    lowermost = row_index

            for column in row:
                if column:
                    if column_index > rightmost:
                        rightmost = column_index
                    
                    if column_index < leftmost:
                        leftmost = column_index

                column_index = column_index + 1

            row_index = row_index + 1
        
        rows = list()

        row_index = uppermost

        while row_index <= lowermost:
            this_row = list()
            column_index = leftmost

            while column_index <= rightmost:
                this_row.append( first_layer[row_index][column_index] )

                column_index = column_index + 1

            rows.append( this_row )
            row_index = row_index + 1
        
        self.layers = list()

        for index in range( 0, depth ):
            self.layers.append( copy.deepcopy( rows ) )

    def all_positions( self ):
        result = list()

        for z in range( 0, len( self.layers ) ):
            for y in range( 0, len( self.layers[0] ) ):
                for x in range( 0, len( self.layers[0][0] ) ):
                    result.append( TDP( x, y, z ) )
        
        return result

    def available_positions( self ):
        result = list()

        for z in range( 0, len( self.layers ) ):
            for y in range( 0, len( self.layers[0] ) ):
                for x in range( 0, len( self.layers[0][0] ) ):
                    if self.layers[z][y][x]:
                        result.append( TDP( x, y, z ) )

        return result

    # Implement deepcopying of this class
    def __deepcopy__( self, memo ):
        # Create a new instance of this class without calling the constructor
        cls = self.__class__
        result = cls.__new__( cls )

        # Add ourselves to the memo so we know we've been copied to prevent recusion
        memo[id(self)] = result

        result.layers = copy.deepcopy( self.layers )
        
        return result

    # Try to apply an animal to this map. If it succeeds, return a deep copy of this map after the animal is applied. If not, return None.
    def apply_positions( self, positions ):
        # Test to see if this will fit in our map
        for tdp in positions:
            if  ( tdp.z < 0 or tdp.z >= len( self.layers )
                or tdp.y < 0 or tdp.y >= len( self.layers[0] )
                or tdp.x < 0 or tdp.x >= len( self.layers[0][0] ) ):
                return None

            if not self.layers[tdp.z][tdp.y][tdp.x]:
                return None

        # We know it can fit, so now we deepcopy when we know we need to
        test_map = copy.deepcopy( self )
   
        for tdp in positions:
            test_map.layers[tdp.z][tdp.y][tdp.x] = False
        
        return test_map