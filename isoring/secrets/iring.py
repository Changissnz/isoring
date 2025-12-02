from .bloominstein import * 
from morebs2.numerical_generator import prg_seqsort
from morebs2.matrix_methods import euclidean_point_distance 

def prng_point_distance_funtion(prng): 

    def f(x0,x1):
        return euclidean_point_distance(x0,x1) + prng()   
    return f 

class IsoRing:

    """
    sec_list := list, every element is a <Sec> 
    feedback_function := function, F: (vector,vector) -> float 
    """
    def __init__(self,sec_list,feedback_function,actual_sec_index=0): 
        assert len(sec_list) > 0 
        assert len(sec_list) > actual_sec_index >= 0 
        idn_tag = set() 
        for s in sec_list: 
            assert type(s) == Sec 
            idn_tag |= {s.idn_tag}
        assert len(idn_tag) == 1
        self.sec_list = sec_list 
        self.feedback_function = feedback_function
        self.actual_sec_index = actual_sec_index
        self.current_sec_index = actual_sec_index
        return

    def provide_feedback_distance_vec(self,i):
        s = self.iso_repr() 
        opt_points = s.optima_points() 

        V = [] 
        for o in opt_points: 
            try: 
                v = self.feedback_function(i,o) 
                V.append(v) 
            # case: different dim. 
            except:
                return None 
        return np.array(V)  
    
    def provide_feedback_pr(self,stringized_opt_point:str): 
        s = self.iso_repr() 
        if stringized_opt_point not in s.opm: return -1 
        return s.opm[stringized_opt_point]

    def idn_tag(self): 
        return self.sec_list[0].idn_tag 

    def set_iso_repr(self,i):
        assert 0 <= i < len(self.sec_list) 
        self.current_sec_index = i 

    def iso_repr(self): 
        return self.sec_list[self.current_sec_index]

    def reset_iso_repr(self): 
        self.current_sec_index = self.actual_sec_index

    def assign_DC_set(self,ds,cds):
        assert type(ds) == set 
        for s in self.sec_list:
            s.ds = ds
            s.cds = cds 

    def clear_depANDcodep_sets(self): 
        for s in self.sec_list:
            s.ds.clear()
            s.cds.clear() 

    def actual_sec_vec(self): 
        return self.sec_list[self.actual_sec_index].seq 

    """
    feedback_function_type := 0 for euclidean point distance, 1 for prng noise added. 
    """
    @staticmethod 
    def generate_IsoRing_from_one_secret(sec,prng,feedback_function_type,\
        num_blooms=DEFAULT_NUM_BLOOMS,dim_range=DEFAULT_BLOOM_VECTOR_DIM_RANGE,\
        sec_vec_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE,optima_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE): 

        assert feedback_function_type in {0,1}

        bos = BloomOfSecret(sec,prng,num_blooms=DEFAULT_NUM_BLOOMS,dim_range=DEFAULT_BLOOM_VECTOR_DIM_RANGE,\
        sec_vec_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE,optima_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE)

        while True: 
            if type(next(bos)) == type(None): break 

        def prg_(): 
            return int(prng())

        l = [i for i in range(bos.num_blooms + 1)]
        l = prg_seqsort(l,prg_)
        sec_list = [bos.all_sec[l[i]] for i in l] 
        actual_sec_index = l[0] 

        if feedback_function_type: 
            feedback_function = prng_point_distance_funtion(prng)
        else: 
            feedback_function = euclidean_point_distance

        return IsoRing(sec_list,feedback_function,actual_sec_index=actual_sec_index)