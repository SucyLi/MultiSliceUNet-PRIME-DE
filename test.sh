# local
# python muSkullStrip.py -in /Users/xinhui.li/Documents/monkey-segmentation/data/human_init_test/test/t1w/959574_3T_T1w_MPR1.nii.gz -out /Users/xinhui.li/Documents/monkey-segmentation/data/out/test -model /Users/xinhui.li/Documents/monkey-segmentation/data/out/test/model-00-epoch
# python muSkullStrip.py -in /Users/xinhui.li/Documents/research/data/monkey/test/head_in_brain.nii.gz -out /Users/xinhui.li/Documents/research/data/out/aws/monkey-with-human-model/wm -model /Users/xinhui.li/Documents/research/data/out/aws/hcp/wm/model-09-epoch
# python muSkullStrip.py -in /Users/xinhui.li/Documents/research/data/monkey/test/head_in_brain.nii.gz -out /Users/xinhui.li/Documents/research/data/out/aws/monkey-with-human-model/gm -model /Users/xinhui.li/Documents/research/data/out/aws/hcp/gm/model-09-epoch
# python muSkullStrip.py -in /Users/xinhui.li/Documents/research/data/monkey/test/head_in_brain.nii.gz -out /Users/xinhui.li/Documents/research/data/out/aws/monkey-with-human-model/csf -model /Users/xinhui.li/Documents/research/data/out/aws/hcp/csf/model-09-epoch
# python muSkullStrip.py -in /Users/xinhui.li/Documents/monkey-segmentation/data/hcp/test/t1w -out /Users/xinhui.li/Documents/monkey-segmentation/data/out/aws/hcp/tissue -model /Users/xinhui.li/Documents/monkey-segmentation/data/out/aws/hcp/tissue/model-09-epoch -class 7
# human
# python muSkullStrip.py -in /Users/xinhui.li/Documents/monkey-segmentation/data/human_init_test/test/t1w/959574_3T_T1w_MPR1.nii.gz -out /Users/xinhui.li/Documents/monkey-segmentation/data/out/test/all_channel_01 -model /Users/xinhui.li/Documents/monkey-segmentation/data/out/test/all_channel_01/model-02-epoch
# python testSs_UNet.py -tet1w /Users/xinhui.li/Documents/monkey-segmentation/data/hcp_test/t1w_raw/927359_3T_T1w_MPR1.nii.gz -temsk /Users/xinhui.li/Documents/monkey-segmentation/data/hcp_test/mask/927359_final_contr.nii.gz -out /Users/xinhui.li/Documents/monkey-segmentation/data/out/test/prior -model /Users/xinhui.li/Documents/monkey-segmentation/data/out/colab/model-09-epoch_hcp

# monkey
# python muSkullStrip.py -in /Users/xinhui.li/Documents/monkey-segmentation/data/monkey/site-mountsinai-P/site-mountsinai-P_preprocessed_T1 -out /Users/xinhui.li/Documents/monkey-segmentation/data/monkey/site-mountsinai-P_unet -model /Users/xinhui.li/Documents/monkey-segmentation/data/out/aws/hcp/fix_bg/monkey/model-09-epoch
python muSkullStrip.py -in /Users/xinhui.li/Documents/monkey-segmentation/data/monkey/site-mountsinai-P/site-mountsinai-P_preprocessed_T1 -out /Users/xinhui.li/Documents/monkey-segmentation/data/monkey/site-mountsinai-P_unet2 -model /Users/xinhui.li/Documents/monkey-segmentation/data/monkey/stef/mountsinai-P/model-09-epoch



# aws 
# python muSkullStrip.py -in /media/ebs/data/hcp/test/t1w -out /media/ebs/out/hcp/wm -model /media/ebs/out/hcp/wm/model-09-epoch # function to save dice fails 
# python muSkullStrip.py -in /media/ebs/data/hcp/test/t1w -out /media/ebs/out/hcp/gm -model /media/ebs/out/hcp/gm/model-09-epoch
# python muSkullStrip.py -in /media/ebs/data/hcp/test/t1w -out /media/ebs/out/hcp/csf -model /media/ebs/out/hcp/csf/model-09-epoch

# python testSs_UNet.py -tet1w /media/ebs/data/hcp/test/t1w -temsk /media/ebs/data/hcp/test/mask_wm -out /media/ebs/out/hcp/wm -model /media/ebs/out/hcp/wm/model-09-epoch
# python testSs_UNet.py -tet1w /media/ebs/data/hcp/test/t1w -temsk /media/ebs/data/hcp/test/mask_gm -out /media/ebs/out/hcp/gm -model /media/ebs/out/hcp/gm/model-09-epoch
# python testSs_UNet.py -tet1w /media/ebs/data/hcp/test/t1w -temsk /media/ebs/data/hcp/test/mask_csf -out /media/ebs/out/hcp/csf -model /media/ebs/out/hcp/csf/model-09-epoch