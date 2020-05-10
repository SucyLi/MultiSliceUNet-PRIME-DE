import os, subprocess

datapath='/Users/xinhui.li/Documents/monkey-segmentation/data/out/colab/FNFP_aligned/fnfp'
tissue=['wm','gm','csf','skull','skin','eye']
fnfp=['fn','fp']

for t in tissue:
    for f in fnfp:
        cwd=os.path.join(datapath,t,f)
        errormap=os.listdir(cwd)
        os.chdir(cwd)

        cmd=["fslmaths", errormap[0], "-div", "15", "merged_mean.nii.gz"]
        subprocess.check_output(cmd)
                
        for d in ["X","Y","Z"]:
            cmd=["fslmaths", "merged_mean.nii.gz", "-"+d+"mean", "merged_mean_"+d+".nii.gz"]
            subprocess.check_output(cmd)