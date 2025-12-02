
from .leak_functions import * 
from morebs2.matrix_methods import is_proper_bounds_vector

class HypStruct:

    def __init__(self,seq_idn:int,suspected_subbound,hop_size,probability_marker):
        assert type(seq_idn) == int 
        assert is_proper_bounds_vector(suspected_subbound) 
        assert type(hop_size) == int and hop_size > 1 
        assert type(probability_marker) in {type(None),float}
        if type(probability_marker) == float: 
            assert 0 <= probability_marker <= 1 

        self.seq_idn = seq_idn 
        self.suspected_subbound = suspected_subbound
        self.hop_size = hop_size
        self.probability_marker = probability_marker
        return

    """
    method is port for receiving feedback information from <IsoRing> 
    """
    def register_pointANDpr(self,point,pr): 

        if not point_in_bounds(self.suspected_subbound,point): 
            return False 

        if pr != self.probability_marker: 
            return False 

        return True 