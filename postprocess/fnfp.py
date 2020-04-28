import glob
import numpy as np
import nibabel as nb

def write_nifti(data, aff, shape, out_path):
    data=data[0:shape[0],0:shape[1],0:shape[2]]
    img=nb.Nifti1Image(data, aff)
    img.to_filename(out_path)

tissue = ['wm','gm','csf','skull','skin','eye']

for t in tissue:
    mask_path='/Users/xinhui.li/Documents/monkey-segmentation/data/out/aws/hcp/fix_bg/FNFP_aligned/'+t+'/*'
    mask_list=glob.glob(mask_path)
    num_test=15
    x=182
    y=218
    z=182
    # x=256
    # y=320
    # z=320

    fn = np.zeros((num_test, x, y, z))
    fp = np.zeros((num_test, x, y, z))

    for i, m in enumerate(mask_list):
        mask = nb.load(m)
        mask_data = mask.get_data()
        
        mask_data_fn = mask_data < 0
        mask_data_fp = mask_data > 0
        
        mask_data_fn = mask_data_fn * 1
        mask_data_fp = mask_data_fp * 1

        fn[i,:,:,:] = mask_data_fn
        fp[i,:,:,:] = mask_data_fp

        if i==0:
            fnfp_aff=mask.affine
            fnfp_shape=mask.shape

    fn = np.sum(fn, axis=0)
    fp = np.sum(fp, axis=0)

    out_path='/Users/xinhui.li/Documents/monkey-segmentation/data/out/aws/hcp/fix_bg/FNFP_aligned/'+t+'/'+t+'_fn.nii.gz'
    write_nifti(np.array(fn, dtype=np.float32), fnfp_aff, fnfp_shape, out_path)

    out_path='/Users/xinhui.li/Documents/monkey-segmentation/data/out/aws/hcp/fix_bg/FNFP_aligned/'+t+'/'+t+'_fp.nii.gz'
    write_nifti(np.array(fp, dtype=np.float32), fnfp_aff, fnfp_shape, out_path)


# for i, b in enumerate(bmsk_list):
#     pr_bmsk = nb.load('/Users/xinhui.li/Documents/monkey-segmentation/data/out/colab/test/'+pr_bmsk_final_list[i])
#     pr_bmsk_data = pr_bmsk.get_data()

#     bmsk = nb.load('/Users/xinhui.li/Documents/monkey-segmentation/data/hcp_test/mask/'+b)
#     bmsk_data = bmsk.get_data()

#     t1w_aff=bmsk.affine
#     t1w_shape=bmsk.shape

#     fn_fp=estimate_fn_fp(bmsk_data, pr_bmsk_data, num_class)

#     for i_class in range(0,num_class-1):
#         out_path=os.path.join(nii_outdir, b[0:b.rindex('.nii.gz')] +"_fnfp_"+str(i_class)+".nii.gz")
#         write_nifti(np.array(fn_fp[i_class,:,:,:], dtype=np.float32), t1w_aff, t1w_shape, out_path)
#         print(out_path)