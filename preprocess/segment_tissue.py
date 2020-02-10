import os
import subprocess

data_path = '/Users/xinhui.li/Documents/research/data/HCPdata/mask'
path_csf = '/Users/xinhui.li/Documents/research/data/HCPdata/mask_csf'
path_gm = '/Users/xinhui.li/Documents/research/data/HCPdata/mask_gm'
path_wm = '/Users/xinhui.li/Documents/research/data/HCPdata/mask_wm'

file_list = os.listdir(data_path)
# 1: WM, 2: GM, 3: CSF
for i in file_list:
    mask = os.path.join(data_path, i)
    mask_csf = os.path.join(path_csf, i)
    mask_gm = os.path.join(path_gm, i)
    mask_wm = os.path.join(path_wm, i)

    cmd = ['fslmaths', mask, '-thr', '2.5', '-uthr', '3.5', mask_csf]
    subprocess.check_output(cmd)

    cmd1 = ['fslmaths', mask, '-thr', '1.5', '-uthr', '2.5', mask_gm]
    subprocess.check_output(cmd1)

    cmd2 = ['fslmaths', mask, '-thr', '0.5', '-uthr', '1.5', mask_wm]
    subprocess.check_output(cmd2)

