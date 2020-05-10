import os, glob, subprocess

template = '/usr/local/fsl/data/standard/MNI152_T1_1mm.nii.gz'
t1_path = '/Users/xinhui.li/Documents/monkey-segmentation/data/raw_hcp_test/t1w/'
t1_list = os.listdir(t1_path)
t1_list.sort()

out_path1 = '/Users/xinhui.li/Documents/monkey-segmentation/data/hcp_test/t1w_mni/'

tissue = ['wm','gm','csf','skull','skin','eye']

for i, t in enumerate(t1_list): 
    
    # cmd = ['flirt', '-in', t1_path+t, '-ref', template, '-out', out_path1+t[0:t.rindex('.nii.gz')]+'_mni.nii.gz', '-omat', out_path1+t[0:t.rindex('_3T')]+'.mat']
    # subprocess.check_output(cmd)

    for j, ti in enumerate(tissue):
        print('Running ' + t + ' ' + ti)
        fnfp_path = glob.glob('/Users/xinhui.li/Documents/monkey-segmentation/data/out/colab/FNFP/'+ti+'/*')
        fnfp_path.sort()

        out_path2 = '/Users/xinhui.li/Documents/monkey-segmentation/data/out/colab/FNFP_aligned/'+ti+'/'

        cmd1 = ['flirt', '-in', fnfp_path[i], '-ref', template, '-applyxfm', '-init', out_path1+t[0:t.rindex('_3T')]+'.mat', '-out', out_path2+t[0:t.rindex('.nii.gz')]+'_pre_mask_fnfp_aligned_'+str(j)+'.nii.gz', '-interp', 'nearestneighbour']
        subprocess.check_output(cmd1)
   
    # flirt -in -ref -out -omat 
    # flirt -in -ref -applyxfm -init -out -interp nearestneighbour

