from .iring import * 
from morebs2.numerical_generator import prg_choose_n

class IsoRingedChain:

    def __init__(self,ir_list): 
        for ir in ir_list: assert type(ir) == IsoRing
        self.ir_list = ir_list  
        return

    def actual_vec_map(self): 
        D = dict()
        for ir in self.ir_list:
            D[ir.idn_tag()] = ir.actual_sec_vec() 
        return D 

    @staticmethod
    def prng__add_depANDcodep_to_IsoRingList(ir_list,prng,codep_ratio=0.0):
        assert len(ir_list) > 0 
        assert 0.0 <= codep_ratio <= 1.0 

        idns = [] 
        ir_dict = {} 
        for ir in ir_list:
            idns.append(ir.idn_tag()) 
            ir.clear_depANDcodep_sets()
            ir_dict[ir.idn_tag] = ir 
        
        oodc = IsoRingedChain.prng__idns_to_order_of_depANDcodep(idns,prng,codep_ratio)

        for j in range(len(oodc)): 
            depset = set() 
            for i in range(0,j): 
                depset |= oodc[i] 

            # add codep and dep for each in the set 
            codeps = oodc[j]
            for j_ in codeps: 
                cds = codeps - {j_} 
                ir = ir_dict[j_] 
                ir.assign_DC_set(depset,cds) 
    
    @staticmethod
    def prng__idns_to_order_of_depANDcodep(idns,prng,codep_ratio):
        assert len(set(idns)) == len(idns)

        def prg_(): 
            return int(prng())

        total_conn = len(idns) - 1 
        codep_conn = int(ceil(total_conn * codep_ratio))

        L = prg_seqsort(idns,prg_) 
        L_ = []

        while codep_conn > 0: 
            x = modulo_in_range(prg_(),[1,codep_conn+1]) 
            S = set() 
            i = prg_() % len(L)
            l = L.pop(i)
            S |= {l}

            for _ in range(x): 
                i = prg_() % len(L)
                l = L.pop(i)
                S |= {l} 
            L_.append(S) 
            codep_conn -= x 
        

        while len(L) > 0: 
            L_.append({L.pop(0)})

        L_ = prg_seqsort(L_,prg_)
        return L_

    # TODO: test this. 
    @staticmethod 
    def list_of_vectors_to_IsoRingedChain(vec_list,prng,num_blooms_range=[DEFAULT_NUM_BLOOMS,DEFAULT_NUM_BLOOMS+1],
        ratio_of_feedback_functions_type_1:float=1.0,codep_ratio=0.0):  

        def prg_(): return int(prng()) 

        # shuffle `vec_list`
        vec_list = prg_seqsort(vec_list,prg_)

        # generate the list of <Sec> instances 
        sec_list = [] 
        for (i,vec) in enumerate(vec_list): 
            num_optima = modulo_in_range(prg_(),DEFAULT_NUM_OPTIMA_RANGE)
            set_actual_as_max_pr = bool(prg_() % 2)
            sec = Sec.vec_to_bare_instance(vec,singleton_distance=DEFAULT_SINGLETON_DISTANCE_RANGE,\
                num_optima=num_optima,prng=prng,idn_tag=i,set_actual_as_max_pr=set_actual_as_max_pr)
            sec_list.append(sec) 

        # get the <Sec> indexes with feedback function type 1
        num_sec_ftype_1 = int(ceil(ratio_of_feedback_functions_type_1 * len(sec_list))) 
        index_list = [_ for _ in range(len(sec_list))] 
        ftype_1_indices = prg_choose_n(index_list,num_sec_ftype_1,prg_,is_unique_picker=True)

        for (i,sec) in enumerate(sec_list): 
            # transform each <Sec> into an <IsoRing> 
            feedback_function_type = 1 if i in ftype_1_indices else 0 
            ir = IsoRing.generate_IsoRing_from_one_secret(sec,prng,feedback_function_type,\
                num_blooms=DEFAULT_NUM_BLOOMS,dim_range=DEFAULT_BLOOM_VECTOR_DIM_RANGE,\
                sec_vec_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE,\
                optima_multiplier_range=DEFAULT_BLOOM_MULTIPLIER_RANGE)
            ir_list.append(ir)

        IsoRingedChain.prng__add_depANDcodep_to_IsoRingList(ir_list,prng,codep_ratio)
        irc = IsoRingedChain(ir_list) 
        return irc 