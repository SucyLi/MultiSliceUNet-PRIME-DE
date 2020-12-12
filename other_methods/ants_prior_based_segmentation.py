import os, subprocess

anatomical_brain_path = "/data3/cnl/xli/unet_seg/data/monkey/9sites_34monkeys/unet_brain"
anatomical_brain_mask_path = "/data3/cnl/xli/unet_seg/data/monkey/9sites_34monkeys/unet_brain_mask"
out_path = "/data3/cnl/xli/unet_seg/data/monkey/9sites_34monkeys/ants_seg"

anatomical_brain_list = os.listdir(anatomical_brain_path)
anatomical_brain_mask_list = os.listdir(anatomical_brain_mask_path)

anatomical_brain_list.sort()
anatomical_brain_mask_list.sort()

template_brain_list = ["/data3/cnl/monkey_seg/templates/JointLabelCouncil/MacaqueYerkes19_T1w_0.5mm/T1w_brain.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_36mo_atlas_nACQ_194x252x160space_0.5mm/T1w_brain.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_36mo_atlas_oACQ_194x252x160space_0.5mm/T1w_brain.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_21mo_atlas_nACQ_194x252x160space_0.5mm/T1w_brain.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_21mo_atlas_oACQ_194x252x160space_0.5mm/T1w_brain.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_11mo_atlas_nACQ_194x252x160space_0.5mm/T1w_brain.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_11mo_atlas_oACQ_194x252x160space_0.5mm/T1w_brain.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_6mo_atlas_nACQ_194x252x160space_0.5mm/T1w_brain.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_6mo_atlas_oACQ_194x252x160space_0.5mm/T1w_brain.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_4mo_atlas_nACQ_194x252x160space_0.5mm/T1w_brain.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_4mo_atlas_oACQ_194x252x160space_0.5mm/T1w_brain.nii.gz"]

template_segmentation_list = ["/data3/cnl/monkey_seg/templates/JointLabelCouncil/MacaqueYerkes19_T1w_0.5mm/Segmentation.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_36mo_atlas_nACQ_194x252x160space_0.5mm/Segmentation.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_36mo_atlas_oACQ_194x252x160space_0.5mm/Segmentation.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_21mo_atlas_nACQ_194x252x160space_0.5mm/Segmentation.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_21mo_atlas_oACQ_194x252x160space_0.5mm/Segmentation.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_11mo_atlas_nACQ_194x252x160space_0.5mm/Segmentation.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_11mo_atlas_oACQ_194x252x160space_0.5mm/Segmentation.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_6mo_atlas_nACQ_194x252x160space_0.5mm/Segmentation.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_6mo_atlas_oACQ_194x252x160space_0.5mm/Segmentation.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_4mo_atlas_nACQ_194x252x160space_0.5mm/Segmentation.nii.gz",
"/data3/cnl/monkey_seg/templates/JointLabelCouncil/J_Macaque_4mo_atlas_oACQ_194x252x160space_0.5mm/Segmentation.nii.gz"]

for i, anatomical_brain in enumerate(anatomical_brain_list):
    
    basename = anatomical_brain[0:anatomical_brain.rindex('_T1')]

    os.chdir(out_path)
    os.mkdir(basename)
    os.chdir(basename)

    anatomical_brain_mask = anatomical_brain_mask_list[i]

    cmd = ["antsJointLabelFusion.sh"] 
    cmd.append(" -d 3 -o ants_multiatlas_ -t {0} -x {1} -y b -c 0".format(os.path.join(anatomical_brain_path,anatomical_brain), os.path.join(anatomical_brain_mask_path,anatomical_brain_mask)))

    for index in range(len(template_brain_list)):
        cmd.append(" -g {0} -l {1}".format(template_brain_list[index], template_segmentation_list[index]))
    
    str = ""
    bash_cmd = str.join(cmd)

    retcode = subprocess.check_output(bash_cmd, shell=True)