from isoring.secrets.secret import * 
import unittest

### lone file test 
"""
python3 -m tests.test_secret 
"""
###
class SecClass(unittest.TestCase):

    def test__Sec__generate_bare_instance__case1(self):
        singleton_range = [-10**6,10**6]
        dimension = 6 
        num_optima = 8 
        prng = prg__LCG(67,81,23,2121) 

        for _ in range(10): 
            s = Sec.generate_bare_instance(singleton_range,dimension,num_optima,prng,idn_tag=0,set_actual_as_max_pr=False)
            ##print(s) 
            assert type(s) == Sec 
            assert len(s.opm) == 8 
            assert s.optima_points().shape == (8,6)
        
        assert (s.seq == np.array([-997994.0,-998687.0,-999674.0,-999023.0,-999317.0,-999800.0])).all()


if __name__ == '__main__':
    unittest.main()
