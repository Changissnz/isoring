from isoring.secrets.big_secret import * 
import unittest

### lone file test 
"""
python3 -m tests.test_big_secret  
"""
###
class IsoRingedChainClass(unittest.TestCase):

    def test__IsoRingedChain__prng__idns_to_order_of_depANDcodep__case1(self):
        prng = default_std_Python_prng(integer_seed=302,output_range=[0,1000],rounding_depth=3)
        X = [6,1,3,10,12,43,56,13,31,42,113,57,65,78,110,95,93,91,16]

        Y = IsoRingedChain.prng__idns_to_order_of_depANDcodep(X[:],prng,0)
        for y in Y: 
            assert len(y) == 1 

        Y2 = IsoRingedChain.prng__idns_to_order_of_depANDcodep(X[:],prng,0.5)

        s = 0 
        for y in Y2: 
            if len(y) == 1: continue 
            s += len(y) - 1 
        assert s == ceil(0.5 * (len(X) - 1)) 
        return 


if __name__ == '__main__':
    unittest.main()
