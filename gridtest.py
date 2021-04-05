import log_likelihood as log_lklhd

#filename = 'options_trial/clean_05-03-21-155231.json'

def gridtest(filename):
    min = 10000000
    w_opt = 50
    a_opt = 50
    c_opt = 50
    for w in range(50):
        for a in range(50):
            for c in range(50):
                wc_scale = 0.1
                a_scale = 0.02
                likelihood = log_lklhd.computeLikelihood(filename,w*wc_scale, a*a_scale, c*wc_scale)
                if likelihood < min: 
                    min = likelihood
                    w_opt = w*wc_scale
                    a_opt = a*a_scale
                    c_opt = c*wc_scale
    print("min_likelihood: ", min)
    print("w: ", w_opt)
    print("a: ", a_opt)
    print("c: ", c_opt)
    
#gridtest(filename)