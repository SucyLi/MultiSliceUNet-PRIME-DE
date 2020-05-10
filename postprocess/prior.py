import numpy as np
import nibabel as nb
import scipy.ndimage as snd
from scipy.spatial import distance

def write_nifti(data, aff, shape, out_path):
    data=data[0:shape[0],0:shape[1],0:shape[2]]
    img=nb.Nifti1Image(data, aff)
    img.to_filename(out_path)

tpm_path = '/Users/xinhui.li/Documents/monkey-segmentation/data/hcp_test/tpm/tpm_mni_unet_order.nii.gz'
unet_tpm_path = '/Users/xinhui.li/Documents/monkey-segmentation/data/out/test/prior/927359_tpm_mni.nii.gz'
unet_raw_mask_path = '/Users/xinhui.li/Documents/monkey-segmentation/data/out/test/prior/927359_3T_T1w_MPR1_pre_mask_mni.nii.gz'
gt_mask_path = '/Users/xinhui.li/Documents/monkey-segmentation/data/hcp_test/mask_mni/927359_final_contr_mni.nii.gz'
out_path = '/Users/xinhui.li/Documents/monkey-segmentation/data/out/test/prior/927359_3T_T1w_MPR1_pre_mask_mni_updated.nii.gz'

# read standard TPM
tpm = nb.load(tpm_path).get_fdata()

# read U-Net TPM
unet_tpm = nb.load(unet_tpm_path).get_fdata()

# take argmax
unet_updated_tpm = np.zeros(tpm.shape)
for x in range(tpm.shape[0]):
    for y in range(tpm.shape[1]):
        for z in range(tpm.shape[2]):
            for t in range(tpm.shape[3]):
                unet_updated_tpm[x,y,z,t] = max(tpm[x,y,z,t], unet_tpm[x,y,z,t])

# import pdb;pdb.set_trace() 
unet_updated_mask = np.argmax(unet_updated_tpm, axis=3)

# load U-Net raw mask and GT 
unet_raw_mask = nb.load(unet_raw_mask_path).get_fdata()
gt_file = nb.load(gt_mask_path)
gt_mask = gt_file.get_fdata()

# calculate dice between U-Net raw mask and GT
for i in range(tpm.shape[3]):
    d1 = gt_mask == i
    d2 = unet_raw_mask == i
    d3 = unet_updated_mask == i
    t1 = d1 * 1
    t2 = d2 * 1
    t3 = d3 * 1
    
    dice = distance.dice(t2.flatten(), t1.flatten())
    print(i, " dice between U-Net raw mask and GT :", 1-dice)

    # calculate dice between U-Net updated mask and GT
    dice = distance.dice(t3.flatten(), t1.flatten())
    print(i, " dice between U-Net updated mask and GT :", 1-dice)

write_nifti(np.array(unet_updated_mask, dtype=np.float32), gt_file.affine, gt_file.shape, out_path)