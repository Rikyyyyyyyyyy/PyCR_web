from scipy.io import savemat 
import matlab.engine

def main():
    path = '/Users/wenwenli/Desktop/output_urain1/matlab_plot'
    eng = matlab.engine.start_matlab()
    eng.plot(matlab.double([1,2,3,4]))  
    eng.savefig(path+"foo.fig",visible= 'off')   
    eng.close()    

main()