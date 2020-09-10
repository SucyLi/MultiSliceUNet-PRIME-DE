import os
import numpy as np
import nibabel as nb

def write_nifti(data, affine, out_path):
    img = nb.Nifti1Image(data, affine)
    img.to_filename(out_path)

unet_path = "/data3/cnl/xli/unet_seg/data/monkey/9sites_34monkeys/unet"
manual_path = "/data3/cnl/xli/unet_seg/data/monkey/9sites_34monkeys/seg_raw"
out_path = "/data3/cnl/xli/unet_seg/data/monkey/9sites_34monkeys/seg_wm_gm"

manual_list = os.listdir(manual_path)
manual_list.sort()

for i, file in enumerate(manual_list):
    manual = nb.load(os.path.join(manual_path, file))
    affine = manual.affine
    data = manual.get_fdata()
    out_data = np.zeros(data.shape)
    out_file = os.path.join(out_path, file)

    for x in range(0,data.shape[0]):
        for y in range(0,data.shape[1]):
            for z in range(0,data.shape[2]):
                # gm
                if data[x,y,z] == 42 or data[x,y,z] == 3:
                    out_data[x,y,z] = 2
                # wm
                if data[x,y,z] == 41 or data[x,y,z] == 2:
                    out_data[x,y,z] = 1

    write_nifti(out_data, affine, out_file)


'''
unet_list = os.listdir(unet_path)
unet_list.sort()
manual_list = os.listdir(manual_path)
manual_list.sort()

for i, unet_file in enumerate(unet_list):
    
    unet = nb.load(os.path.join(unet_path, unet_file))
    unet_affine = unet.affine
    unet_data = unet.get_fdata()
    manual_file = manual_list[i]
    manual_data = nb.load(os.path.join(manual_path, manual_file)).get_fdata()
    print(unet_file, manual_file)

    out_data = np.zeros(unet_data.shape)
    out_file = os.path.join(out_path, unet_file[0:unet_file.rindex('_T1')]+'.nii.gz')

    for x in range(0,unet_data.shape[0]):
        for y in range(0,unet_data.shape[1]):
            for z in range(0,unet_data.shape[2]):
                if unet_data[x,y,z] == 1:
                    out_data[x,y,z] = 1
                elif unet_data[x,y,z] == 4:
                    out_data[x,y,z] = 4
                elif unet_data[x,y,z] == 5:
                    out_data[x,y,z] = 5
                elif unet_data[x,y,z] == 6:
                    out_data[x,y,z] = 6
                # gm
                if manual_data[x,y,z] == 42 or manual_data[x,y,z] == 3:
                    out_data[x,y,z] = 2
                # wm
                if manual_data[x,y,z] == 41 or manual_data[x,y,z] == 2:
                    out_data[x,y,z] = 3

    write_nifti(out_data, unet_affine, out_file)
'''