from isoring.brute_forcer.leak_functions import * 
from morebs2.search_space_iterator import * 
import unittest

def SearchSpaceIterator_for_bounds(bounds,hop_size): 
    startPoint = np.copy(bounds[:,0])
    columnOrder = [i for i in range(bounds.shape[0])]  
    cycleOn = False   
    cycleIs = 0 
    ssi = SearchSpaceIterator(bounds, startPoint, columnOrder, hop_size,cycleOn, cycleIs)
    return ssi 


### lone file test 
"""
python3 -m tests.test_leak_functions
"""
###
class LeakFunctions(unittest.TestCase):

    def test__prng__search_space_bounds_for_vector__case1(self): 
        prng = prg__LCG(67,43,101,2112)

        vec = np.array([5.654,67.01,55.32])
        hop_size = 6 
        bound_length = 1.0 
        bounds = prng__search_space_bounds_for_vector(vec,hop_size,bound_length,prng=prng)

        ssi = SearchSpaceIterator_for_bounds(bounds,hop_size) 
        while not ssi.reached_end(): 
            q = next(ssi) 
            if euclidean_point_distance(q,vec) < 0.01: 
                return 
        assert False

    def test__prng__search_space_bounds_for_vector__case2(self): 
        prng = prg__LCG(671,432,9,2112)

        vec = np.array([56.5114,67.11201,551.2132,712.3413])
        hop_size = 9 
        bound_length = 1.0 
        bounds = prng__search_space_bounds_for_vector(vec,hop_size,bound_length,prng=prng)

        ssi = SearchSpaceIterator_for_bounds(bounds,hop_size) 
        while not ssi.reached_end(): 
            q = next(ssi) 
            if euclidean_point_distance(q,vec) < 0.01: 
                return 
        assert False

    def test__prng__search_space_bounds_for_vector__case3(self): 
        prng = prg__LCG(671,432,9,2112)

        vec = np.array([11.1,311.24141,56.5114,67.11201,551.2132,712.3413])
        hop_size = 3 
        bound_length = 1.0 
        bounds = prng__search_space_bounds_for_vector(vec,hop_size,bound_length,prng=prng)

        ssi = SearchSpaceIterator_for_bounds(bounds,hop_size) 
        while not ssi.reached_end(): 
            q = next(ssi) 
            if euclidean_point_distance(q,vec) < 0.01: 
                return 
        assert False

if __name__ == '__main__':
    unittest.main()
