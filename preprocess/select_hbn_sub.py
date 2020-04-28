import glob
import subprocess

# root_path='/data2/HBNcore/CMI_HBN_Data/MRI/'
root_path='/home/xli/hbn/'
site_list=['CUNY'] #'RU', 'CBIC', 'CUNY'

"""
# create softlink for HBN data 
for site in site_list:
    data_path_list=glob.glob(root_path+site+'/data/sub*')
    for data_path in data_path_list:
        file_list = glob.glob(data_path+'/anat/*')
        if any("T2w.nii.gz" in file for file in file_list):
            for file in file_list:
                if "T2w.nii.gz" in file:
                    cmd = ['ln', '-s', file, 'hbn/']
                    subprocess.check_output(cmd)

                    t1 = file[0:file.rindex('T2w.nii.gz')]+'T1w.nii.gz'
                    cmd1 = ['ln', '-s', t1, 'hbn/']
                    subprocess.check_output(cmd1)

                    print(cmd)
                    print(cmd1)
"""
# sub_list=['sub-5000820_acq-HCP_T1w', 'sub-5000820_acq-HCP_T2w',
# 	'sub-5016867_acq-HCP_T1w', 'sub-5016867_acq-HCP_T2w',
# 	'sub-5041326_acq-HCP_T1w', 'sub-5041326_acq-HCP_T2w',
# 	'sub-5053185_acq-HCP_T1w', 'sub-5053185_acq-HCP_T2w',
# 	'sub-5053933_acq-HCP_T1w', 'sub-5053933_acq-HCP_T2w',	
#     'sub-5054052_acq-HCP_T1w', 'sub-5054052_acq-HCP_T2w',
# 	'sub-5071634_acq-HCP_T1w', 'sub-5071634_acq-HCP_T2w',
# 	'sub-5078842_acq-HCP_T1w', 'sub-5078842_acq-HCP_T2w',
# 	'sub-5132170_acq-HCP_T1w', 'sub-5132170_acq-HCP_T2w',
# 	'sub-5133471_acq-HCP_T1w', 'sub-5133471_acq-HCP_T2w',
#     'sub-5181563_acq-HCP_T1w', 'sub-5181563_acq-HCP_T2w',
# 	'sub-5199450_acq-HCP_T1w', 'sub-5199450_acq-HCP_T2w',
# 	'sub-5205070_acq-HCP_T1w', 'sub-5205070_acq-HCP_T2w',
# 	'sub-5214644_acq-HCP_T1w', 'sub-5214644_acq-HCP_T2w',
# 	'sub-5256599_acq-HCP_T1w', 'sub-5256599_acq-HCP_T2w',
#     'sub-5282775_acq-HCP_T1w', 'sub-5282775_acq-HCP_T2w',
# 	'sub-5293590_acq-HCP_T1w', 'sub-5293590_acq-HCP_T2w',
# 	'sub-5306651_acq-HCP_T1w', 'sub-5306651_acq-HCP_T2w',
# 	'sub-5318253_acq-HCP_T1w', 'sub-5318253_acq-HCP_T2w',
# 	'sub-5371774_acq-HCP_T1w', 'sub-5371774_acq-HCP_T2w']

# sub_list=['sub-1091111_acq-VNavNorm_T1w', 'sub-1091111_acq-VNavNorm_T2w',
#     'sub-5000946_acq-VNavNorm_T1w', 'sub-5000946_acq-VNavNorm_T2w',
#     'sub-5007372_acq-VNavNorm_T1w', 'sub-5007372_acq-VNavNorm_T2w',
#     'sub-5016646_acq-VNavNorm_T1w', 'sub-5016646_acq-VNavNorm_T2w',
#     'sub-5016818_acq-VNavNorm_T1w', 'sub-5016818_acq-VNavNorm_T2w',
#     'sub-5026599_acq-VNavNorm_T1w', 'sub-5026599_acq-VNavNorm_T2w',
#     'sub-5028016_acq-VNavNorm_T1w', 'sub-5028016_acq-VNavNorm_T2w',
#     'sub-5029413_acq-VNavNorm_T1w', 'sub-5029413_acq-VNavNorm_T2w',
#     'sub-5036903_acq-VNav_T1w', 'sub-5036903_acq-VNav_T2w',
#     'sub-5039851_acq-VNavNorm_T1w', 'sub-5039851_acq-VNavNorm_T2w',
#     'sub-5048730_acq-VNavNorm_T1w', 'sub-5048730_acq-VNavNorm_T2w',
#     'sub-5056773_acq-VNavNorm_T1w', 'sub-5056773_acq-VNavNorm_T2w',
#     'sub-5062847_acq-VNavNorm_T1w', 'sub-5062847_acq-VNavNorm_T2w',
#     'sub-5073368_acq-VNavNorm_T1w', 'sub-5073368_acq-VNavNorm_T2w',
#     'sub-5080946_acq-VNavNorm_T1w', 'sub-5080946_acq-VNavNorm_T2w',
#     'sub-5081660_acq-VNavNorm_T1w', 'sub-5081660_acq-VNavNorm_T2w',
#     'sub-5085290_acq-VNavNorm_T1w', 'sub-5085290_acq-VNavNorm_T2w',
#     'sub-5094407_acq-VNavNorm_T1w', 'sub-5094407_acq-VNavNorm_T2w',
#     'sub-5097051_acq-VNavNorm_T1w', 'sub-5097051_acq-VNavNorm_T2w',
#     'sub-5105026_acq-VNavNorm_T1w', 'sub-5105026_acq-VNavNorm_T2w']

sub_list=['sub-5038475_acq-VNavNorm_T1w', 'sub-5038475_acq-VNavNorm_T2w',
    'sub-5088259_acq-VNavNorm_T1w', 'sub-5088259_acq-VNavNorm_T2w',
    'sub-5339884_acq-VNavNorm_T1w', 'sub-5339884_acq-VNavNorm_T2w',
    'sub-5357964_acq-VNavNorm_T1w', 'sub-5357964_acq-VNavNorm_T2w',
    'sub-5544605_acq-VNavNorm_T1w', 'sub-5544605_acq-VNavNorm_T2w',
    'sub-5677163_acq-VNavNorm_T1w', 'sub-5677163_acq-VNavNorm_T2w',
    'sub-5116406_acq-VNavNorm_T1w', 'sub-5116406_acq-VNavNorm_T2w',
    'sub-5721150_acq-VNavNorm_T1w', 'sub-5721150_acq-VNavNorm_T2w',
    'sub-5944927_acq-VNavNorm_T1w', 'sub-5944927_acq-VNavNorm_T2w',
    'sub-5963771_acq-VNavNorm_T1w', 'sub-5963771_acq-VNavNorm_T2w',
    'sub-5984828_acq-VNavNorm_T1w', 'sub-5984828_acq-VNavNorm_T2w',
    'sub-5946903_acq-VNavNorm_T1w', 'sub-5946903_acq-VNavNorm_T2w',
    'sub-5809159_acq-VNavNorm_T1w', 'sub-5809159_acq-VNavNorm_T2w',
    'sub-5761142_acq-VNavNorm_T1w', 'sub-5761142_acq-VNavNorm_T2w',
    'sub-5713008_acq-VNavNorm_T1w', 'sub-5713008_acq-VNavNorm_T2w',
    'sub-5703128_acq-VNavNorm_T1w', 'sub-5703128_acq-VNavNorm_T2w',
    'sub-5599101_acq-VNavNorm_T1w', 'sub-5599101_acq-VNavNorm_T2w',
    'sub-5423714_acq-VNavNorm_T1w', 'sub-5423714_acq-VNavNorm_T2w',
    'sub-5368608_acq-VNavNorm_T1w', 'sub-5368608_acq-VNavNorm_T2w',
    'sub-5224715_acq-VNavNorm_T1w', 'sub-5224715_acq-VNavNorm_T2w']

for sub in sub_list:
    cmd=['mv', root_path+'CUNY/'+sub+'.nii.gz', root_path+'cuny/']
    subprocess.check_output(cmd)

