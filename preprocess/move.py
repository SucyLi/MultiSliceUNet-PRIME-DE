import os, subprocess

data_path = '/Users/xinhui.li/Documents/research/data/hcp/t1w'
data_path2 = '/Users/xinhui.li/Documents/research/data/hcp/t1w_done'

file_list = os.listdir(data_path)
# file_list2 = os.listdir(data_path2)

for n, i in enumerate(file_list):
    print n, i

    file_path = os.path.join(data_path, i)
    file_path2 = os.path.join(data_path2, i)

    cmd = ['mv', file_path, file_path2]
    subprocess.check_output(cmd)