from .iring import * 

class IsoRingedChain:

    def __init__(self,ir_list): 
        for ir in ir_list: assert type(ir) == IsoRing
        self.ir_list = ir_list  
        return

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

            codeps = oodc[j]
            # add codep 
            for j_ in codeps: 
                cds = codeps - {j_} 
                ir = ir_dict[j_] 
                ir.assign_DC_set(depset,cds) 
    
    @staticmethod
    def prng__idns_to_order_of_depANDcodep(idns,prng,codep_ratio):
        assert len(set(idns)) == len(idns)

        def prg_(): 
            return int(prng())

        total_conn = len(ir_list) - 1 
        codep_conn = int(ceil(total_conn * codep_ratio))

        L = prg_seqsort(idns,prg_) 
        L_ = []

        while codep_conn > 0: 
            x = modulo_in_range(prg_(),[1,codep_conn+1]) 
            S = set() 
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