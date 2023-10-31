from flask import Flask, request
from flask_restplus import Api, Resource, fields
from puzzle import Puzzle

flask_app = Flask( __name__ )
app = Api( app = flask_app,
        version = "1.0",
        title = "Cat Calculator REST API",
        description = "Provides solutions to Cat Stax and Dog Pile puzzles." )

name_space = app.namespace( "main", description = "Main APIs" )

model = app.model( "Puzzle Model",
            {
                "footprint": fields.List( fields.List( fields.Boolean() ),
                                        required = True,
                                        description = "The footprint of the puzzle as a two dimensional array of booleans" ),
                "animalType": fields.String( required = True,
                                        description = "The type of animal to be solved (dog/cat)" ),
                "animals": fields.List( fields.String(),
                                        required = True,
                                        description = "The list of animals included in the puzzle" ),
                "layers": fields.Integer( required = True,
                                        description = "The number of layers in the puzzle" )
            } )

@name_space.route("/")
class MainClass( Resource ):
    @app.doc(   responses = {   200: "OK",
                                400: "Invalid Argument" } )
    @app.expect( model )
    def post( self ):
        try:
            puzzle = Puzzle( request.json )

            solutions = puzzle.solve()
        
        except Exception as e:
            name_space.abort( 400, e.__doc__, status = "Could not parse provided puzzle", statusCode = "400" )
