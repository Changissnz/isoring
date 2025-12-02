from isoring.brute_forcer.leak_functions import * 
import unittest

def SecANDprng_sample_X(): 
    prng = prg__LCG(66,3,7,3212) 
    sec = Sec.generate_bare_instance([-60.,1112.],5,6,prng,idn_tag=0,set_actual_as_max_pr=False)
    return sec,prng 


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

    def test__prng_leak_Secret__case1(self): 
        sec,prng = SecANDprng_sample_X() 

        bounds,hop_size,pr_value = prng_leak_Secret(sec,prng,is_actual_sec_vec=True,is_valid_bounds=True)
        ssi = SearchSpaceIterator_for_bounds(bounds,hop_size)
        i = 0 
        while True: 
            q = next(ssi) 
            i += 1 
            if euclidean_point_distance(q,sec.seq) < 0.05:
                break 

        assert i == 2208,"got {}".format(i)

    def test__prng_leak_Secret__case2(self): 
        sec,prng = SecANDprng_sample_X() 
        bounds,hop_size,pr_value = prng_leak_Secret(sec,prng,is_actual_sec_vec=True,is_valid_bounds=False)
        ssi = SearchSpaceIterator_for_bounds(bounds,hop_size)
        stat0,stat1 = False,False
        while not ssi.reached_end(): 
            q = next(ssi) 
            if euclidean_point_distance(q,sec.seq) < 0.05:
                stat0 = True 
            
            q_ = vector_to_string(q,float) 
            if q_ in sec.opm: 
                stat1 = True 

        assert not stat0 and not stat1
        return

    def test__prng_leak_Secret__case3(self): 
        sec,prng = SecANDprng_sample_X() 
        bounds,hop_size,pr_value = prng_leak_Secret(sec,prng,is_actual_sec_vec=False,is_valid_bounds=True)
        ssi = SearchSpaceIterator_for_bounds(bounds,hop_size)

        stat0,stat1 = False,False
        while not ssi.reached_end(): 
            q = next(ssi) 
            if euclidean_point_distance(q,sec.seq) < 0.05:
                stat0 = True 
            
            q_ = vector_to_string(q,float) 
            if q_ in sec.opm: 
                stat1 = True 

        assert not stat0 and stat1 
        return

if __name__ == '__main__':
    unittest.main()
