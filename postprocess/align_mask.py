import os, glob, subprocess

template = '/usr/local/fsl/data/standard/MNI152_T1_1mm.nii.gz'
# moving_path = '/Users/xinhui.li/Documents/monkey-segmentation/data/out/colab/hnu_test_hnu_train_pT1/'
moving_path = '/Users/xinhui.li/Documents/monkey-segmentation/data/hcp_test/mask/'
moving_list = os.listdir(moving_path)
moving_list.sort()
mat_path = '/Users/xinhui.li/Documents/monkey-segmentation/data/hcp_test/t1w_to_mni_mat/'
# output_path = '/Users/xinhui.li/Documents/monkey-segmentation/data/out/colab/hnu_test_hnu_train_pT1_mni/'
output_path = '/Users/xinhui.li/Documents/monkey-segmentation/data/hcp_test/mask_mni/'

for i, t in enumerate(moving_list): 
    print('Running ' + str(i) + ' ' + t)
    
    cmd1 = ['flirt', '-in', moving_path+t, '-ref', template, '-applyxfm', '-init', mat_path+t[0:6]+'.mat', '-out', output_path+t[0:t.rindex('.nii.gz')]+'_mni.nii.gz', '-interp', 'nearestneighbour']
    subprocess.check_output(cmd1)