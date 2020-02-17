import os
import numpy as np
import nibabel as nib

bmsk_dir = '/Users/xinhui.li/Documents/monkey-segmentation/data/human_init_test/train/mask/965367_final_contr.nii.gz'
bmsk_nii = nib.load(os.path.join(bmsk_dir))
bmsk=np.array(bmsk_nii.get_data(), dtype=np.int64)
print(bmsk.shape)

import pdb;pdb.set_trace()

a = bmsk==3
a = a * 1
tmsk_nii = bmsk * a
print(tmsk_nii.shape)

output_img = nib.Nifti1Image(tmsk_nii, affine=bmsk_nii.get_affine())
out_file = os.path.join(os.getcwd(), 'test_mask_3.nii.gz')
output_img.to_filename(out_file)

