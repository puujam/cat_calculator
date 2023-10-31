from . import mongoAnimal

def get_puzzles_by_animal_type( db, animal_type ):
    data = db.cat_calculator.puzzles.find( { "animalType": animal_type } )

    return [ Puzzle( db, item ) for item in data ]

class Puzzle:
    def __init__( self, db, data ):
        self.db = db
        self.data = data
    
    @property
    def footprint( self ):
        return self.data[ "footprint" ]

    @property
    def animal_type( self ):
        return self.data[ "animalType" ]

    @property
    def layers( self ):
        return self.data[ "layers" ]
    
    @property
    def number( self ):
        return self.data[ "number" ]
    
    @property
    def animals( self ):
        if not hasattr( self, "_animals" ):
            self._animals = list()

            for animal_name in self.data[ "animals" ]:
                self._animals.append( mongoAnimal.get_animal_by_name_and_type( self.db, animal_name, self.animal_type ) )
        
        return self._animals
    
    @property
    def all_available_coordinates( self ):
        results = list()

        for y_index in range( self.footprint ):
            # Note: assumes footprints are defined in fully rectangular dimensions (I think they must be though?)
            for x_index in range( self.footprint[0] ):
                if self.footprint[y_index][x_index]:
                    for z_index in range( self.layers ):
                        results.append( tuple( x_index, y_index, z_index ) )
        
        return results
    
    @property
    def solutions( self ):
        if not hasattr( self, "_solutions" ):
            if "solutions" in self.data:
                self._solutions = list()

                for solution_data in self.data[ "solutions" ]:
                    self._solutions.append( { "name": solution_data["name"], "positions": { tuple( item ) for item in solution_data["positions"] } } )
            else:
                return None
        
        return self._solutions