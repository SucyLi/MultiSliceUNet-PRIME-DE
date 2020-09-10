import glob
import numpy as np
import nibabel as nb
import scipy.io as sio
from scipy.spatial import distance
from scipy.stats import pearsonr

# filepath_pred = '/Users/xinhui.li/Documents/monkey-segmentation/data/out/colab/hbn_test_hnu_train_pT1/*'
# filepath_gt = '/Users/xinhui.li/Documents/monkey-segmentation/data/hbn/test/mask/*'

filepath_pred = '/Users/xinhui.li/Downloads/9sites_34monkeys/unet_test2/*'
filepath_gt = '/Users/xinhui.li/Downloads/9sites_34monkeys/test2/*'

filelist_pred = glob.glob(filepath_pred)
# filelist_pred = ["/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/stef/mountsinai-P/acpc_aligned_mask/sub-032153_mask_acpc.nii.gz"]
filelist_pred.sort()

filelist_gt = glob.glob(filepath_gt)
# filelist_gt = ["/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/stef/mountsinai-P/acpc_aligned_unet_output/sub-032153_sanlm_T1_mean_bc_n4_acpc_pre_mask.nii.gz"]
filelist_gt.sort()

tissue = ['background','wm','gm'] #['background','wm','gm','csf','skull','skin','eye']
dice_coefficients = np.zeros((len(tissue), len(filelist_pred)))

for j, pred in enumerate(filelist_pred):
    img1 = nb.load(pred)
    data1 = img1.get_fdata()

    img2 = nb.load(filelist_gt[j])
    data2 = img2.get_fdata()
    print(pred[pred.rindex('/')+1:pred.rindex('_T1_bc')])

    for i, t in enumerate(tissue):
        d1 = data1 == i
        d2 = data2 == i
        t1 = d1 * 1
        t2 = d2 * 1
        dice = distance.dice(t1.flatten(), t2.flatten())
        dice_coefficients[i,j] = 1-dice
        print(t, str(round(dice_coefficients[i,j],2)))

sio.savemat('/Users/xinhui.li/Downloads/monkey_wm_gm_unet_model2/dice.mat', {'dice':dice_coefficients})


# TODO fix NMT monkey mask intensity 
# d1 = data1 == 1
# d2 = data2 == 3
# t1 = d1 * 1
# t2 = d2 * 1
# dice = distance.dice(t1.flatten(), t2.flatten())
# print("CSF", str(1-dice))

# d1 = data1 == 3
# d2 = data2 == 1
# t1 = d1 * 1
# t2 = d2 * 1
# dice = distance.dice(t1.flatten(), t2.flatten())
# print("WM", str(1-dice))


# dice = distance.dice(data1.flatten(), data2.flatten())
# print('Dice coefficient: ' + str(1-dice))

# corr, _ = pearsonr(data1.flatten(), data2.flatten())
# print('Pearson correlation: ' + str(corr))