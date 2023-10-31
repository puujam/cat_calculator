from . import mongoSpace

def get_all_animals( db, animal_type ):
    all_animal_data = db.cat_calculator.animals.find( { "type": animal_type } )

    return [ mongoAnimal( data ) for data in all_animal_data ]

def get_animal_by_name_and_type( db, name, type ):
    animal_data = db.cat_calculator.animals.find( { "type": animal_type, "name": name } )

    return mongoAnimal( animal_data )

class mongoAnimal():
    def __init__( self, data ):
        self.data = data

    @property
    def type( self ):
        return self.data[ "type" ]

    @property
    def name( self ):
        return self.data[ "name" ]

    @property
    def unique_positions( self ):
        if not hasattr( self, "_unique_positions" ):
            if "unique_positions" in self.data:
                self._unique_positions = list()

                for position_list in self.data[ "unique_positions" ]:
                    current_positions = { tuple( position ) for position in position_list }
                    
                    self._unique_positions.append( current_positions )
            else:
                self._unique_positions = None
        
        return self._unique_positions
    
    @property
    def footprint( self ):
        return self.data[ "footprint" ]

    @property
    def base_positions( self ):
        if not hasattr( self, "_base_positions" ):
            self._base_positions = list()

            footprint = self.footprint

            for x_index in range( len( footprint ) ):
                for y_index in range( len( footprint[0] ) ):
                    if footprint[ x_index ][ y_index ]:
                        # Z position is always 0
                        self._base_positions.append( ( x_index, y_index, 0 ) )
        
        return self._base_positions
    
    def assign_unique_positions( self, db_handle, unique_positions ):
        db_handle.cat_calculator.animals.update_one(
            filter = { "name": self.name,
            "type": self.type },
            update = {
                "$set": {
                    "unique_positions": [ list( unique_position_list ) for unique_position_list in unique_positions ]
                }
            }
        )