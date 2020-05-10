import os
import numpy as np
import nibabel as nb

# read unet masks and brain tissue masks
unet_path='/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/site-mountsinai-P/unet'
unet_list=os.listdir(unet_path)
unet_list.sort()

brain_path='/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/site-mountsinai-P/seg'
brain_list=os.listdir(brain_path)
brain_list.sort()

out_path='/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/site-mountsinai-P/final'


# loop each monkey
for i,unet in enumerate(unet_list):
    
    sub=unet[0:10]
    print(sub)
    # load unet mask
    unet=nb.load(os.path.join(unet_path,unet))
    affine=unet.affine
    unet=unet.get_fdata()

    # load brain tissue mask
    brain=nb.load(os.path.join(brain_path,brain_list[i])).get_fdata()

    final_mask=np.zeros(brain.shape)

    for x in range(final_mask.shape[0]):
        for y in range(final_mask.shape[1]):
            for z in range(final_mask.shape[2]):
                if brain[x,y,z] in [1,2,3]:
                    final_mask[x,y,z] = brain[x,y,z]
                elif unet[x,y,z] in [4,5,6]:
                    final_mask[x,y,z] = unet[x,y,z]

    img=nb.Nifti1Image(final_mask, affine)
    img.to_filename(os.path.join(out_path,sub+"_pre_mask.nii.gz"))
