import os,glob
import numpy as np
import nibabel as nb

# read unet masks and brain tissue masks
unet_path='/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/data/unet_mask'
unet_list=os.listdir(unet_path)
unet_list.sort()

brain_path='/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/data/brain_mask1'
site_list=os.listdir(brain_path)
site_list.sort()

out_path='/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/data/union_mask'

# loop each monkey
for i,site in enumerate(site_list):

    site_path = os.path.join(brain_path,site)
    os.chdir(site_path)
    sub_list = os.listdir(site_path)

    for j,sub in enumerate(sub_list):

        # load unet mask
        unet_file=glob.glob(unet_path+'/'+sub+'*')[0]
        unet=nb.load(unet_file)
        affine=unet.affine
        unet=unet.get_fdata()

        # load brain tissue mask
        ses=unet_file[unet_file.rindex('/')+12:unet_file.rindex('/')+19]
        sub_path = os.path.join(brain_path,site,sub,ses)
        os.chdir(sub_path)

        wm=nb.load("wm.nii.gz").get_fdata()
        gm=nb.load("gm.nii.gz").get_fdata()
        csf=nb.load("csf.nii.gz").get_fdata()

        final_mask=np.zeros(unet.shape)

        for x in range(final_mask.shape[0]):
            for y in range(final_mask.shape[1]):
                for z in range(final_mask.shape[2]):
                    if wm[x,y,z] == 1:
                        final_mask[x,y,z] = 1
                    elif gm[x,y,z] == 1:
                        final_mask[x,y,z] = 2
                    elif csf[x,y,z] == 1:
                        final_mask[x,y,z] = 3
                    elif unet[x,y,z] in [4,5,6]:
                        final_mask[x,y,z] = unet[x,y,z]

        print(site,sub)
        img=nb.Nifti1Image(final_mask, affine)
        img.to_filename(os.path.join(out_path,sub+'_'+ses+"_pre_mask.nii.gz"))