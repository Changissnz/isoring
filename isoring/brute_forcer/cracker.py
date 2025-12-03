from .crackling import * 

"""
Container to store cracked <Sec> instances from target <IsoRingedChain>.
"""
class CrackerSoln: 

    def __init__(self): 
        # IsoRing idn -> Sec index -> 
        #    (optima index, vector solution, ?does Crackling accept solution based on feedback Pr. value?) 
        self.D = dict() 

    def add_cracked_soln(self,cr:Crackling): 
        assert type(cr.cracked_soln) != type(None)
        assert type(cr.soln_pr) != None 
        if cr.target_ir not in self.D: 
            self.D[cr.target_ir] = dict() 
        
        assert cr.ir_sec_index not in self.D[cr.target_ir], "solution already acquired." 
        self.D[cr.target_ir][cr.ir_sec_index] = (cr.sec_opt_index,cr.cracked_soln,cr.soln_pr)
        return

"""
<Cracker> is a structure that uses its given <BackgroundInfo> to conduct 
cracking on an <IsoRingedChain> in a brute-force environment. <Cracker> 
has the capacity to deploy at most `crackling_capacity` <Crackling>s at 
once. 

NOTE: 
<Cracker> may deploy more than 1 <Crackling> per <IsoRing>, although this 
is wasteful in an immobile brute-force environment such that <Crackling>s 
do not have to chase after their target <IsoRing>s. Mobile brute-force 
environments are not implemented in this program. Recall that the 
<BackgroundInfo> map is 
    <Isoring> identifier -> <Sec> index -> <HypStruct>. 
This means that every <Sec> for <IsoRing> is associated with at most 1 
<HypStruct>. Every <Crackling> that targets a <Sec> of an <IsoRing> will 
use the same <HypStruct>. 
"""
class Cracker: 

    def __init__(self,bi:BackgroundInfo,crackling_capacity:int):
        assert type(bi) == BackgroundInfo 
        assert type(crackling_capacity) == int and crackling_capacity > 0 
        self.bi = bi 
        self.crackling_capacity = crackling_capacity

        self.csoln = CrackerSoln() 
        self.active_cracklings = [] 
        self.ooci = 0 
        self.target_ir_set = None 
        return

    def next_target_IsoRing_set(self):
        S = self.next_target_IsoRing_set_() 
        if len(S) == 0: return False 
        self.target_ir_set = S 

    def next_target_IsoRing_set_(self): 
        if len(self.bi.order_of_cracking) <= self.ooci: 
            return set() 
        return self.bi.order_of_cracking[self.ooci] 

    def active_target_ir_size(self): 
        if type(self.target_ir_set) == type(None):
            return -1 
        return len(self.target_ir_set) 

    """
    instantiate Cracklings based on info given by the two dict arguments. 

    return: 
    - ?deployment is successful? 
    """
    def deploy_cracklings(self,target_ir_to_isorepr_map:dict,target_ir_to_num_cracklings_map:dict): 
        assert type(self.target_ir_set) != type(None) 

        # ensure crackling capacity can accomodate for number of cracklings
        #else: 
        target_irset = set(target_ir_to_num_cracklings_map.keys()) 
        assert set(target_ir_to_isorepr_map.keys()) == target_irset 
        assert target_irset.issubset(self.target_ir_set) 

        sum_wanted_cracklings = sum(target_ir_to_num_cracklings_map.values()) 

        # case: invalid Crackling allocation, error 
        if self.crackling_capacity - len(self.active_cracklings) < sum_wanted_cracklings: 
            return False 

        for k,v in target_ir_to_num_cracklings_map.items(): 
            assert v > 0 
            for _ in range(v): 
                # case: no hypothesis for (IsoRing,Sec) exists, error 
                if not self.bi.hypothesis_exists_for_IsoRingANDSec(k,target_ir_to_isorepr_map[k]): 
                    self.active_cracklings.clear() 
                    return False 

                hs = self.bi.info[k][target_ir_to_isorepr_map[k]] 
                c = Crackling(k,target_ir_to_isorepr_map[k],hs.opt_index)
                self.active_cracklings.append(c)
        return True 

    def check_active_cracklings(self): 
        finished_ir_for_cracklings = set() 

        l = 0 

        # iterate through and check each Crackling 
        while l < len(self.active_cracklings): 
            c = self.active_cracklings[0] 

            # case: extra Crackling for cracked (IsoRing,Sec)
            if c.target_ir in finished_ir_for_cracklings: 
                self.active_cracklings.pop(0) 
                continue 

            # case: solution acquired 
            if c.has_soln(): 
                finished_ir_for_cracklings |= {c.target_ir}
                self.csoln.add_cracked_soln(c) 
                self.active_cracklings.pop(0) 
                continue 

            l += 1

        # remove the finished IsoRing idns from `target_ir_set`
        self.target_ir_set -= finished_ir_for_cracklings 
