import os, glob, subprocess

data_path = '/media/ebs/data/hcp/validation'
os.chdir(data_path)

# U-Net to Cerebrum
t1_path = data_path + '/t1w'
mask_path = data_path + '/mask'
t1_list = os.listdir(t1_path)

for t1 in t1_list:
    sub=t1[0:6]
    
    t1 = os.path.join(t1_path, t1)

    try: 
        mask = glob.glob(os.path.join(mask_path, sub)+'*')[0]
        
        os.mkdir(sub)
        cmd="mv %s ./%s" % (t1, sub)
        os.system(cmd)

        cmd="mv %s ./%s" % (mask, sub)
        os.system(cmd)        
    except IndexError as e:
        print(sub, " mask not found ***")

cmd="rm -rf ./t1w"
os.system(cmd)

cmd="rm -rf ./mask"
os.system(cmd)


# Cerebrum to U-Net



"""
# human
data_path = '/Users/xinhui.li/Documents/research/data/HCPdata'
file_path = os.listdir(data_path)

os.chdir(data_path)
cmd1 = ['mkdir', 't1w']
cmd2 = ['mkdir', 't2w']
cmd3 = ['mkdir', 'mask']
subprocess.check_output(cmd1)
subprocess.check_output(cmd2)
subprocess.check_output(cmd3)

for f in file_path:
    print(f)
    cwd = os.getcwd()
    os.chdir(os.path.join(data_path, f))

    cmd4 = ['mv', f+'_3T_T1w_MPR1.nii.gz', '../t1w']
    subprocess.check_output(cmd4)

    cmd5 = ['mv', f+'_3T_T2w_SPC1.nii.gz', '../t2w']
    subprocess.check_output(cmd5)

    cmd6 = ['mv', f+'_final_contr.nii.gz', '../mask']
    subprocess.check_output(cmd6)

    os.chdir(cwd)
"""