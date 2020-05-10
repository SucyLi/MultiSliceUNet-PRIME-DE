import os, glob
import numpy as np
import nibabel as nb
import scipy.io as sio
from scipy.spatial import distance
from scipy.stats import pearsonr

"""
file1 = '/Users/xinhui.li/Documents/research/data/out/aws/monkey/wm/head_in_brain_pre_mask.nii.gz'
file2 = '/Users/xinhui.li/Documents/research/data/monkey/test/segment_wm_rpi.nii.gz'

img1 = nb.load(file1)
data1 = img1.get_fdata()

img2 = nb.load(file2)
data2 = img2.get_fdata()

dice = distance.dice(data1.flatten(), data2.flatten())
print('Dice coefficient: ' + str(1-dice))

corr, _ = pearsonr(data1.flatten(), data2.flatten())
print('Pearson correlation: ' + str(corr))
"""

# precon_all vs U-Net WM, GM, CSF
root_path='/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/site-mountsinai-P'
pa_path=root_path+'/site-mountsinai-P_seg/'
unet_path=root_path+'/site-mountsinai-P_unet/'
pa_path_list=os.listdir(pa_path)
pa_path_list.sort()
dice_coefficients = np.zeros((3, len(pa_path_list)))

for i,pa in enumerate(pa_path_list):
    sub=pa[0:10]
    unet=glob.glob(unet_path+sub+'*')[0]
    d1 = nb.load(unet).get_fdata()
    d2 = nb.load(pa_path+pa).get_fdata()
    
    for j in [1,2,3]:
        data1 = (d1==j)*1
        if j==1:
            data2 = (d2==3)*1
        elif j==2:
            data2 = (d2==2)*1
        elif j==3:
            data2 = (d2==1)*1
        dice = distance.dice(data1.flatten(), data2.flatten())
        dice_coefficients[j-1,i] = 1-dice
        print(sub, dice_coefficients[j-1,i])

sio.savemat(root_path+'/dice_seg_unet.mat', {'dice':dice_coefficients})