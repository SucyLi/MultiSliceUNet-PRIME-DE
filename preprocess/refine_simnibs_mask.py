import os
import subprocess

data_path = '/Users/xinhui.li/Documents/monkey-segmentation/data/hcp_test/mask'
os.chdir(data_path)
file_list = os.listdir(data_path)
# 1: WM, 2: GM, 3: CSF, 4: Skull, 5: Skin, 6: Eye
tissue_list = ['wm', 'gm', 'csf', 'skull', 'skin', 'eye']

for i in file_list:
    sub = i[0:6]
    mask = os.path.join(data_path, i)
    for j, t in enumerate(tissue_list):
        mask_tissue = sub+'_'+t+'.nii.gz'
        cmd = ['fslmaths', mask, '-thr', str(j)+'.5', '-uthr', str(j+1)+'.5', mask_tissue]
        subprocess.check_output(cmd)

        if j==3 or j==4:
            mask_filled = sub+'_'+t+'_filled.nii.gz'
            cmd1="3dmask_tool -input %s -prefix %s -dilate_input 3 -3 -quiet" % (mask_tissue, mask_filled)
            os.system(cmd1)