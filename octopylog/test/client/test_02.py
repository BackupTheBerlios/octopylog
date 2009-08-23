




"8 cars........"

lobj = []



def gen_str_hc(number, step=16):
    l = list()
    for i in range(number):
        s = ""
        for j in range(i):
            t = "%d" % (step*j)
            t = t.ljust(step, ".")
            s += t
        l.append(s)    
            
            
        print "%4d :: %s" % (len(s), s)
    
    


gen_str_hc(32, 32)



