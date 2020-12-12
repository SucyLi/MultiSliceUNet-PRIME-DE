# -*- coding: utf-8 -*-
import os, glob, subprocess

t1_path = '/data3/cnl/xli/unet_seg/data/monkey/manual_mask/t1_preprocessed/'
t1_list = os.listdir(t1_path)
t1_list.sort()

mask_path = '/data3/cnl/xli/unet_seg/data/monkey/manual_mask/mask/'

template_head_path = '/data3/cnl/xli/unet_seg/data/monkey/nmt2/t1w/monkey_t1w_bc_n4_cut.nii.gz'
template_brain_path = '/data3/cnl/xli/unet_seg/data/monkey/nmt2/monkey/brain_t1w.nii.gz'
template_mask_path = '/data3/cnl/xli/unet_seg/data/monkey/nmt2/monkey/masks/NMT_mask_cut.nii.gz'

working_dir = '/data3/cnl/xli/unet_seg/data/monkey/manual_mask/ants_refined_mask'

for img in t1_list:

    t1 = os.path.join(t1_path, img)
    basename = img[0:10]

    mask = glob.glob(mask_path+basename+'*')[0]
    print(t1)
    print(mask)

    try:
        os.chdir(working_dir)
        os.mkdir(basename)
        os.chdir(os.path.join(working_dir, basename))
        print(os.getcwd())

        cmd = ['ln', '-s', template_brain_path, 'NMT_SS_0.25mm.nii.gz']
        subprocess.check_output(cmd)

        cmd = ['ln', '-s', template_head_path, 'NMT_0.25mm.nii.gz']
        subprocess.check_output(cmd)

        # take WM, GM and CSF mask as brain mask
        cmd = ['fslmaths', mask, '-uthr', '3.5', '-thr', '0.5', '-bin', 'brain_mask_init.nii.gz']
        subprocess.check_output(cmd)
        
        cmd = ['fslmaths', t1, '-mul', 'brain_mask_init.nii.gz', 'brain.nii.gz']
        subprocess.check_output(cmd)

        # unet masked brain in native space to template brain
        cmd = ['flirt','-v','-dof','6','-in','brain.nii.gz','-ref','NMT_SS_0.25mm.nii.gz','-o','brain_rot2atl','-omat','brain_rot2atl.mat','-interp','sinc']
        subprocess.check_output(cmd)

        # head in native space to template head
        cmd = ['flirt','-in',t1,'-ref','NMT_0.25mm.nii.gz','-o','head_rot2atl','-applyxfm','-init','brain_rot2atl.mat']
        subprocess.check_output(cmd)

        # binarize template brain
        cmd = ['fslmaths','NMT_SS_0.25mm.nii.gz','-bin','templateBrainMask.nii.gz']
        subprocess.check_output(cmd)
        
        # template head to native head in template space 
        cmd = ['ANTS','3','-m','CC[head_rot2atl.nii.gz,NMT_0.25mm.nii.gz,1,5]','-t','SyN[0.25]','-r','Gauss[3,0]','-o','atl2T1rot','-i','60x50x20','--use-Histogram-Matching','--number-of-affine-iterations','10000x10000x10000x10000x10000','--MI-option','32x16000']
        subprocess.check_output(cmd)

        # template brain mask to head in template space
        cmd = ['antsApplyTransforms','-d','3','-i','templateBrainMask.nii.gz','-t','atl2T1rotWarp.nii.gz','atl2T1rotAffine.txt','-r','head_rot2atl.nii.gz','-o','brain_rot2atl_mask.nii.gz'] 
        subprocess.check_output(cmd)

        # template WM/GM/CSF/skull/skin/eye mask to head in template space
        for label, tissue in enumerate(['wm','gm','csf','skull','skin','eye']):

            cmd = ['fslmaths', template_mask_path, '-thr', str(0.5+label), '-uthr', str(1.5+label), '-bin', 'NMT_'+tissue+'_0.25mm.nii.gz']
            subprocess.check_output(cmd)

            cmd = ['antsApplyTransforms','-d','3','-i','NMT_'+tissue+'_0.25mm.nii.gz','-t','atl2T1rotWarp.nii.gz','atl2T1rotAffine.txt','-r','head_rot2atl.nii.gz','-o',tissue+'_rot2atl_mask.nii.gz'] 
            subprocess.check_output(cmd)

        # mask in template space to template 
        cmd = ['convert_xfm','-omat','brain_rot2native.mat','-inverse','brain_rot2atl.mat']
        subprocess.check_output(cmd)

        # template mask to native mask
        cmd = ['flirt','-in','brain_rot2atl_mask.nii.gz','-ref','brain.nii.gz','-o','brain_mask.nii.gz','-applyxfm','-init','brain_rot2native.mat']
        subprocess.check_output(cmd)

        # template WM/GM/CSF/skull/skin/eye mask to native mask
        for tissue in ['wm','gm','csf','skull','skin','eye']:

            cmd = ['flirt','-in',tissue+'_rot2atl_mask.nii.gz','-ref','brain.nii.gz','-o',tissue+'_mask.nii.gz','-applyxfm','-init','brain_rot2native.mat']
            subprocess.check_output(cmd)

        # threshold and binarize brain mask
        cmd = ['fslmaths','brain_mask.nii.gz','-thr','.5','-bin','brain_mask_refined.nii.gz']
        subprocess.check_output(cmd)

        # threshold and binarize WM/GM/CSF/skull/skin/eye mask
        for tissue in ['wm','gm','csf','skull','skin','eye']:

            cmd = ['fslmaths',tissue+'_mask.nii.gz','-thr','.5','-bin',tissue+'_mask_refined.nii.gz']
            subprocess.check_output(cmd)

    except OSError as e:
        pass