from ..secrets.iring import * 

def prng__search_space_bounds_for_vector(vec,hop_size,bound_length,prng=None):

    # case: prng is None 
    if type(prng) == type(None): 
        bounds = np.array([vec,vec + bound_length])
        return bounds.T 

    X = bound_length / hop_size

    def hop_from_x(x,num_hops,is_back_hop:int):
        assert type(x) in {int,float,np.float32,np.float64} 

        X_ = X if not is_back_hop else -X 

        for _ in range(num_hops):
            x += X_ 
            #x = round(x,5) 
        return round(x,5) 

    # case: calculate a bound such that iterating over it using a search 
    #       space iterator yields the point `vec`. 
    #       bound is calculated using prng 
    V = [] 
    for i in range(len(vec)): 
        left_hops = int(prng()) % hop_size
        right_hops = hop_size - left_hops 

        v0 = hop_from_x(vec[i],left_hops,True) 
        v1 = hop_from_x(vec[i],right_hops,False) 
        V.append([v0,v1]) 
    return np.array(V)

def SearchSpaceIterator_for_bounds(bounds,hop_size): 
    startPoint = np.copy(bounds[:,0])
    columnOrder = [i for i in range(bounds.shape[0])]  
    cycleOn = False   
    cycleIs = 0 
    ssi = SearchSpaceIterator(bounds, startPoint, columnOrder, hop_size,cycleOn, cycleIs)
    return ssi 