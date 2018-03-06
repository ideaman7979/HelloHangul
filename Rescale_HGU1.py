import os

"""
Rescaling method.
"""
def rescaling_img(o_list):
    o_h=len(o_list)
    o_w=len(o_list[0])
    n_h=64
    n_w=64
    n_list = [[0 for col in range(n_w)] for row in range(n_h)]
    
    for i in range(n_w):
        n_list[0][i]=255
        n_list[n_h - 1][i]=255
        
    for n_y in range(1,n_h - 1):
        o_y = int(n_y * o_h / n_h) 
        n_list[n_y][0] = 255
        n_list[n_y][n_w - 1] = 255
        for n_x in range(1,n_w-1):
            o_x = int(n_x * o_w / n_w)
            n_list[n_y][n_x] = o_list[o_y][o_x]
    return n_list


def scaling_files(origin_path, dest_path, data_name):
   
    n_h=64
    n_w=64
    # read files 
    file_list=os.listdir(origin_path+data_name)
    
    for fine_no in range(len(file_list)):
    # file open
        EOF=False
        myfile=file_list[fine_no]
        f = open(origin_path+data_name+ myfile, 'rb')
        r_f = open(dest_path+data_name+'r_'+myfile, 'wb+')
        file_header = f.read(8)
        r_f.write(file_header)
    
    # Read Images
    
        while EOF==False : 
        # read code & check EoF
            code = f.read(2)
       
            if (len(code) < 2) :
                break
    
            width=f.read(1)[0]
            height = f.read(1)[0]
            buffer=[]
            reserved = f.read(2)
            for i in range(height):
                buffer2=[]
                for j in range(width):
                    data=int.from_bytes(f.read(1), byteorder='big')
                    buffer2.append(data)
                    #print(data, end=' ')
                buffer.append(buffer2)
                #print(buffer)
        
            s_image=rescaling_img(buffer)
            r_f.write(code)
            r_f.write(n_h.to_bytes(1, byteorder='big',signed=False))
            r_f.write(n_w.to_bytes(1, byteorder='big',signed=False))
            r_f.write(reserved)
            for i in range(n_h):
                for j in range(n_w):
                    r_f.write(s_image[i][j].to_bytes(1, byteorder='big',signed=False))
        # Reading file done
        f.close()
        r_f.close()
        #print("File "+str(fine_no)+" is rescaled")
        # Read Next file
    print(data_name+"are done!!")
