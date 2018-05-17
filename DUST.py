def calculateDustScore (read):
    dec={}
    if(len(read)<3):
        return 0.0
    for i in range(0,len(read)-3):
        s=read[i:i+3]
        if s not in dec:
            dec[s]=1
        else:
            dec[s]=dec[s]+1
    sum_val=0.0
    for i in range(0,len(dec)):
        tc=float(dec.values()[i])
        score= (tc*(tc-1))/2.0
        sum_val=sum_val+score
        
    return sum_val/(len(read)-2)       




def maxDustWindow (read,window_size,min_window_size):
    max_score=0.0
    for i in range(0,len(read)-1):
        r=len(read)-i
        if r< window_size:
            w=r
        else:
            w=window_size
        if(w >= min_window_size):
            s=calculateDustScore(read[i:i+w])
            if(s>max_score):
                max_score=s

    return max_score

score=maxDustWindow("AAAAATTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",64,64)
print score
