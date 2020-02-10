import nibabel as nb
from scipy.spatial import distance
from scipy.stats import pearsonr

file1 = '/Users/xinhui.li/Documents/research/data/out/csf/959574_3T_T1w_MPR1_pre_mask.nii.gz'
file2 = '/Users/xinhui.li/Documents/research/data/human/test/mask_csf/959574_final_contr.nii.gz'

img1 = nb.load(file1)
data1 = img1.get_fdata()

img2 = nb.load(file2)
data2 = img2.get_fdata()

dice = distance.dice(data1.flatten(), data2.flatten())
print('Dice coefficient: ' + str(1-dice))

corr, _ = pearsonr(data1.flatten(), data2.flatten())
print('Pearson correlation: ' + str(corr))