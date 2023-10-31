if __name__ == "__main__":
    import puzzle
    import io
    import json

    # For profiling
    import cProfile

    p = puzzle.Puzzle( json.load( io.open( "1.json", "r" ) ) )

    cProfile.run( "solutions = p.solve()" )
    #solutions = p.solve()

    index = 1

    for solution in solutions:
        print( "Solution {}:".format( index ) )
        for animal in solution.animals:
            print( "\t{} at {} in orientation {}".format( animal.name, animal.tdp, animal.tdo ) )

        index = index + 1