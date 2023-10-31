import copy
import space
import time
import threading
import queue

class Solution():
    def __init__( self, map, animals ):
        self.map = map
        self.animals = animals
    
    def add( self, positioned_animal ):
        new_map = self.map.apply_positions( positioned_animal.occupied_positions )

        if not new_map:
            # Animal didn't fit
            return None
        
        new_animals = copy.copy( self.animals )
        new_animals.append( positioned_animal )

        return Solution( new_map, new_animals )

class PartialSolution():
    def __init__( self, solution, remaining_animals ):
        self.solution = solution
        self.remaining_animals = remaining_animals

def solver_worker( input_queue, output_queue ):
    while True:
        partial = input_queue.get()

        if partial is None:
            break

        #print( ", ".join( [ a.name for a in partial.remaining_animals ] ) )

        for animal in partial.remaining_animals:
            for position in partial.solution.map.available_positions():
                for oriented_animal in animal.unique_orientations.values():
                    positioned_animal = oriented_animal.position( position )
                    new_solution = partial.solution.add( positioned_animal )

                    #print( "Placing {} at {} in orientation {}".format( positioned_animal.name, positioned_animal.tdp, positioned_animal.tdo ) )

                    if new_solution:
                        # Addition was valid
                        if len( partial.remaining_animals ) == 1:
                            # This solution is complete
                            #print( "found solution!" )
                            output_queue.put( new_solution )
                        else:
                            new_animal_list = copy.copy( partial.remaining_animals )
                            new_animal_list.remove( animal )

                            input_queue.put( PartialSolution( new_solution, new_animal_list ) )
        
        input_queue.task_done()

def find_all_solutions( map, animals ):
    worker_threads = 32
    threads = list()

    partial_solution_queue = queue.Queue()
    complete_solution_queue = queue.Queue()

    for unused in range( worker_threads ):
        new_thread = threading.Thread( target = solver_worker, args = ( partial_solution_queue, complete_solution_queue ) )
        new_thread.start()
        threads.append( new_thread )

    # Seed our first partial solution and let the threads take over
    partial_solution_queue.put( PartialSolution( Solution( map, list() ), animals ) )

    #while True:
        #if partial_solution_queue.empty():
            #print( "Queue might be empty...." )
            #time.sleep( 2 )

            #if partial_solution_queue.empty():
                #print( "Queue is really empty!" )
                #break

        #print( "Approximate Queue Size: {}".format( partial_solution_queue.qsize() ) )
        #time.sleep( 2 )

    # Wait for the queue to empty
    partial_solution_queue.join()
    
    # Tell the threads to exit
    for thread in threads:
        partial_solution_queue.put( None )

    # Make sure they actually did
    for thread in threads:
        thread.join()

    results = list()
    while not complete_solution_queue.empty():
        results.append( complete_solution_queue.get() )

    return results