from .hypothesis import * 
from ..secrets.big_secret import * 


class BackgroundInfo:

    """
    info := dict, <Isoring> identifier -> <Sec> index -> <HypStruct> 
    suspected_isoring_to_sec_idn := dict, <IsoRing> -> index of <Sec> most likely to be solution. 
    order_of_cracking := list, of sets of <IsoRing> identifiers, specifying the 
                         order that a <Cracker> will attempt cracking an <IsoRingedChain>. 
    """
    # NOTE: `suspected_isoring_to_sec_idn` can be incomplete w.r.t. `info`. In these cases, 
    # <BackgroundInfo> uses method<default_most_likely_Sec_index_for_IsoRing> to decide 
    # the best <HypStruct>. 
    def __init__(self,info:dict,suspected_isoring_to_sec_idn:dict,order_of_cracking:list): 
        assert BackgroundInfo.verify_valid_info(info) 

        q = set(info.keys()) 
        c = set() 
        for o in order_of_cracking: c |= o 
        assert o == c 

        self.info = info 
        self.suspected_isoring_to_sec_idn = suspected_isoring_to_sec_idn
        self.order_of_cracking = order_of_cracking
        return

    @staticmethod
    def verify_valid_info(info): 
        for k,v in info.items(): 
            if not type(k) == int: return False 
            for k2,v2 in v.items(): 
                if not type(k2) == int: return False 
                if not type(v2) == HypStruct: return False 
        return True 

    """
    chooses the <Sec> index with a <HypStruct> of highest probability marker. 
    """
    def default_most_likely_Sec_index_for_IsoRing(self,ir_idn): 
        if ir_idn not in self.info: return None 

        d = self.info[ir_idn] 
        if len(d) == 0: return None 

        secindex_pr = [] 
        for k,v in d.items(): 
            secindex_pr.append((k,v.probability_marker)) 
        
        secindex_pr = sorted(secindex_pr,key=lambda x:x[1],reverse=True)
        return secindex_pr[0][0]