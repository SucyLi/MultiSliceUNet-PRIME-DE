import os, subprocess

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



