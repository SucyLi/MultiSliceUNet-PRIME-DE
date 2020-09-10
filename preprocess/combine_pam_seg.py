import os, glob

root_path = "/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/data/segmentation24"
out_path = "/Users/xinhui.li/Documents/monkey-segmentation/data/monkey/data/segmentation"

site_list = os.listdir(root_path)

for site in site_list:

    if site == ".DS_Store":
        continue

    site_path = os.path.join(root_path, site)
    sub_list = os.listdir(site_path)

    for sub in sub_list:

        if sub == ".DS_Store":
            continue

        sub_path = os.path.join(root_path, site, sub)
        ses_list = os.listdir(sub_path)
        for s in ses_list:
            if 'ses' in s:
                ses = s

        print(site, sub, ses)
        wm = os.path.join(root_path, site, sub, ses, "wm.nii.gz") # 1
        gm = os.path.join(root_path, site, sub, ses, "gm.nii.gz") # 2
        csf = os.path.join(root_path, site, sub, ses, "csf.nii.gz") # 3

        out_gm = os.path.join(out_path, site, sub+"_"+ses+"_gm.nii.gz")
        out_csf = os.path.join(out_path, site, sub+"_"+ses+"_csf.nii.gz")
        out_wm_gm = os.path.join(out_path, site, sub+"_"+ses+"_wm_gm.nii.gz")
        out_seg = os.path.join(out_path, site, sub+"_"+ses+"_brain_tissue.nii.gz")

        cmd = "fslmaths %s -mul 2 %s" % (gm, out_gm)
        os.system(cmd)

        cmd = "fslmaths %s -mul 3 %s" % (csf, out_csf)
        os.system(cmd)

        cmd = "fslmaths %s -add %s %s" % (wm, out_gm, out_wm_gm)
        os.system(cmd)

        cmd = "fslmaths %s -add %s %s" % (out_wm_gm, out_csf, out_seg)
        os.system(cmd)

        cmd = "rm %s" % (out_gm)
        os.system(cmd)

        cmd = "rm %s" % (out_csf)
        os.system(cmd)

        cmd = "rm %s" % (out_wm_gm)
        os.system(cmd)