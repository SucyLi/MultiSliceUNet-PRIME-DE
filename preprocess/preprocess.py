import os, subprocess

# local
data_path = '/Users/xinhui.li/Documents/research/data/hcp/t1w_tbd'
data_path2 = '/Users/xinhui.li/Documents/research/data/hcp/n4'

# aws
# data_path = '/media/ebs/t1w'
# data_path2 = '/media/ebs/preprocessed'

# Lisa
# data_path = '/home/xli/Documents/t1w'
# data_path2 = '/home/xli/Documents/preprocessed'

file_list = os.listdir(data_path)
file_list.sort()

for n, i in enumerate(file_list):
    print n, i

    file_path = os.path.join(data_path, i)

    cwd = os.getcwd()
    os.chdir(data_path2)

    cmd = ['DenoiseImage', '-i', file_path, '-o', i[0:i.rindex('.nii.gz')]+'_bc.nii.gz']
    subprocess.check_output(cmd)

    cmd1 = ['N4BiasFieldCorrection', '-i', i[0:i.rindex('.nii.gz')]+'_bc.nii.gz', '-d', '3', '-s', '2', '-o', i[0:i.rindex('.nii.gz')]+'_bc_n4.nii.gz']
    subprocess.check_output(cmd1)

    os.chdir(cwd)


# DenoiseImage -i -o
# N4BiasFieldCorrection -i -d 3 -s 2 -o 