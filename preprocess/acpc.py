import os

t1_path = "/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/stef/mountsinai-P/t1w/nmt_t1w_bc_n4_cut.nii.gz"
t1_brain_path = "/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/stef/mountsinai-P/brain/nmt_brain.nii.gz"
mask_path = "/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/stef/mountsinai-P/mask/nmt_final_contr_cut.nii.gz"
output_path = "/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/stef/preprocessed"

os.chdir(output_path)

cmd = "robustfov -i %s -m roi2full.mat -r robustroi.nii.gz -b 70" % t1_brain_path
os.system(cmd)

cmd = "convert_xfm -omat full2roi.mat -inverse roi2full.mat"
os.system(cmd)

cmd = "flirt -interp spline -in robustroi.nii.gz -ref MacaqueYerkes19_T1w_0.5mm_brain.nii.gz -omat roi2std.mat -o roi2std.nii.gz -searchrx -30 30 -searchry -30 30 -searchrz -30 30"
os.system(cmd)

cmd = "convert_xfm -omat full2std.mat -concat roi2std.mat full2roi.mat"
os.system(cmd)

cmd = "aff2rigid full2std.mat acpc.mat"
os.system(cmd)

cmd = "applywarp --rel --interp=spline -i %s -r MacaqueYerkes19_T1w_0.5mm_brain.nii.gz --premat=acpc.mat -o nmt_acpc.nii.gz" % t1_path
os.system(cmd)

cmd = "applywarp --rel --interp=nn -i %s -r MacaqueYerkes19_T1w_0.5mm_brain.nii.gz --premat=acpc.mat -o nmt_mask_acpc.nii.gz" % mask_path
os.system(cmd)