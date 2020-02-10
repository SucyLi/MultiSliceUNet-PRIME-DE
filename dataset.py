import torch
import torch.utils.data as data
import torch.nn as nn
import scipy.io as io
import numpy as np
import nibabel as nib
import os, sys

class VolumeDataset(data.Dataset):
    def __init__(self,
        rimg_in=None,
        cimg_in=None,
        bmsk_in=None,
        transform=None,
        debug=True
                ):
        super(VolumeDataset, self).__init__()

        # Raw Images
        self.rimg_in=rimg_in
        if isinstance(rimg_in, type(None)):
            self.rimg_dir=None
            self.rimg_files=None
        else:
            if isinstance(rimg_in, str) and os.path.isdir(rimg_in):
                self.rimg_dir=rimg_in
                self.rimg_files=os.listdir(rimg_in)
                self.rimg_files.sort()
            elif isinstance(rimg_in, str) and os.path.isfile(rimg_in):
                rimg_dir, rimg_file=os.path.split(rimg_in)
                self.rimg_dir=rimg_dir
                self.rimg_files=[rimg_file]
            else:
                print("Invalid rimg_in")
                sys.exit(1)

        # Corrected Images
        self.cimg_in=cimg_in
        if isinstance(cimg_in, type(None)):
            self.cimg_dir=None
            self.cimg_files=None
        else:
            if isinstance(cimg_in, str) and os.path.isdir(cimg_in):
                self.cimg_dir=cimg_in
                self.cimg_files=os.listdir(cimg_in)
                self.cimg_files.sort()
            elif isinstance(cimg_in, str) and os.path.isfile(cimg_in):
                cimg_dir, cimg_file=os.path.split(cimg_in)
                self.cimg_dir=cimg_dir
                self.cimg_files=[cimg_file]
            else:
                print("Invalid cimg_in")
                sys.exit(1)

        # Brain Masks
        self.bmsk_in=bmsk_in
        if isinstance(bmsk_in, type(None)):
            self.bmsk_dir=None
            self.bmsk_files=None
        else:
            if isinstance(bmsk_in, str) and os.path.isdir(bmsk_in):
                self.bmsk_dir=bmsk_in
                self.bmsk_files=os.listdir(bmsk_in)
                self.bmsk_files.sort()
            elif isinstance(bmsk_in, str) and os.path.isfile(bmsk_in):
                bmsk_dir, bmsk_file=os.path.split(bmsk_in)
                self.bmsk_dir=bmsk_dir
                self.bmsk_files=[bmsk_file]
            else:
                print("Invalid bmsk_in")
                sys.exit(1)

        self.cur_rimg_nii=None
        self.cur_cimg_nii=None
        self.cur_bmsk_nii=None

        self.debug=debug

    def getCurRimgNii(self):
        return self.cur_rimg_nii

    def getCurCimgNii(self):
        return self.cur_cimg_nii

    def getCurBmskNii(self):
        return self.cur_bmsk_nii

    def __len__(self):
        return len(self.cimg_files)

    def __getitem__(self, index):
        if self.debug:
            if isinstance(self.rimg_files, list):
                print(self.rimg_files[index])
            if isinstance(self.cimg_files, list):
                print(self.cimg_files[index])
            if isinstance(self.bmsk_files, list):
                print(self.bmsk_files[index])

        Out=list()
        if isinstance(self.rimg_files, list):
            rimg_nii=nib.load(os.path.join(self.rimg_dir, self.rimg_files[index]))
            rimg=np.array(rimg_nii.get_data(), dtype=np.float32)
            # 0-1 Normalization
            rimg=(rimg-rimg.min())/(rimg.max()-rimg.min())
            rimg=torch.from_numpy(rimg)
            Out.append(rimg)

            self.cur_rimg_nii=rimg_nii

        if isinstance(self.cimg_files, list):
            cimg_nii=nib.load(os.path.join(self.cimg_dir, self.cimg_files[index]))
            cimg=np.array(cimg_nii.get_data(), dtype=np.float32)
            # 0-1 Normalization
            cimg=(cimg-cimg.min())/(cimg.max()-cimg.min())
            cimg=torch.from_numpy(cimg)
            Out.append(cimg)

            self.cur_cimg_nii=cimg_nii

        if "rimg" in locals() and "cimg" in locals():
            bfld=cimg/rimg
            bfld[np.isnan(bfld)]=1
            bfld[np.isinf(bfld)]=1
            bfld=torch.from_numpy(bfld)
            Out.append(blfd)

        if isinstance(self.bmsk_files, list):
            bmsk_nii=nib.load(os.path.join(self.bmsk_dir, self.bmsk_files[index]))

            # temp = bmsk_nii.get_data()>0 # will only output 0/1
            temp = bmsk_nii.get_data()
            # print(type(temp))
            # print("brain mask > 0 " + str(temp.shape))

            bmsk=np.array(temp, dtype=np.int64)

            # print("brain mask shape " + str(bmsk.shape))
            
            bmsk=torch.from_numpy(bmsk)
            # print("brain mask out shape " + str(bmsk.shape))

            Out.append(bmsk)

            self.cur_bmsk_nii=bmsk_nii

        if len(Out)==1:
            Out=Out[0]
        else:
            Out=tuple(Out)
        return Out

class BlockDataset(data.Dataset):
    def __init__(self,
        rimg=None,
        bfld=None,
        bmsk=None,
        num_class=7,
        num_slice=3,
        rescale_dim=256):
        super(BlockDataset, self).__init__()
        
        if isinstance(bmsk, torch.Tensor) and rimg.shape!=bmsk.shape:
            print("Invalid shape of image")
            return
        raw_shape=rimg.data[0].shape
        max_dim=torch.tensor(raw_shape).max()
        rescale_factor=float(rescale_dim)/float(max_dim)

        uns_rimg=torch.unsqueeze(rimg, 0)
        uns_rimg=nn.functional.interpolate(uns_rimg, scale_factor=rescale_factor, mode="trilinear", align_corners=False)
        rimg=torch.squeeze(uns_rimg, 0)

        if isinstance(bfld, torch.Tensor):
            uns_bfld=torch.unsqueeze(bfld, 0)
            uns_bfld=nn.functional.interpolate(uns_bfld, scale_factor=rescale_factor, mode="trilinear", align_corners=False)
            bfld=torch.squeeze(uns_bfld, 0)

        if isinstance(bmsk, torch.Tensor):
            uns_bmsk=torch.unsqueeze(bmsk.float(), 0)
            uns_bmsk=nn.functional.interpolate(uns_bmsk, scale_factor=rescale_factor, mode="nearest")
            bmsk=torch.squeeze(uns_bmsk.long(), 0)
        
        # print("brain mask "+str(bmsk.shape))
        
        rescale_shape=rimg.data[0].shape

        # print("rescale shape "+str(rescale_shape))

        slist0=list()
        for i in range(rescale_shape[0]-num_slice+1):
            slist0.append(range(i, i+num_slice))
        self.slist0=slist0
        
        slist1=list()
        for i in range(rescale_shape[1]-num_slice+1):
            slist1.append(range(i, i+num_slice))
        self.slist1=slist1
        
        slist2=list()
        for i in range(rescale_shape[2]-num_slice+1):
            slist2.append(range(i, i+num_slice))
        self.slist2=slist2

        # print("slist0 length "+str(len(self.slist0)))
        # print("slist1 length "+str(len(self.slist1)))
        
        self.rimg=rimg
        self.bfld=bfld
        self.bmsk=bmsk
        
        self.batch_size=rimg.shape[0]
        self.batch_len=len(self.slist0)+len(self.slist1)+len(self.slist2)
        self.num_slice=num_slice
        self.num_class=num_class
        self.rescale_dim=rescale_dim
        self.rescale_factor=rescale_factor
        self.rescale_shape=rescale_shape
        self.raw_shape=raw_shape
    
    def get_rescale_factor(self):
        return self.rescale_factor

    def get_rescale_shape(self):
        return self.rescale_shape

    def get_raw_shape(self):
        return self.raw_shape

    def get_rescale_dim(self):
        return self.rescale_dim

    def get_one_directory(self, axis=0):
        if axis==0:
            ind=range(0, len(self.slist0))
            slist=self.slist0
        elif axis==1:
            ind=range(len(self.slist0), len(self.slist0)+len(self.slist1))
            slist=self.slist1
        elif axis==2:
            ind=range(len(self.slist0)+len(self.slist1), 
                len(self.slist0)+len(self.slist1)+len(self.slist2))
            slist=self.slist2
        
        slice_weight=np.zeros(slist[-1][-1]+1)
        for l in slist:
            slice_weight[l]+=1
        
        slice_data=list()
        for i in ind:
            slice_data.append(self.__getitem__(i))
        
        return slice_data, slist, slice_weight

    def __len__(self):
        list_len=self.batch_size*self.batch_len
        return list_len
    
    def __getitem__(self, index):
        bind=int(index/self.batch_len)
        index=index%self.batch_len
        # print("batch ind "+str(bind))
        

        if index<len(self.slist0):
            # print("***")

            sind=self.slist0[index]
            # print("index "+str(index))
            # print("sind "+str(sind))

            rimg_tmp=self.rimg.data[bind][sind, :, :]

            if isinstance(self.bfld, torch.Tensor):
                bfld_tmp=self.bfld.data[bind][sind, :, :]

            if isinstance(self.bmsk, torch.Tensor):
                bmsk_tmp=self.bmsk.data[bind][sind, :, :]
            # print("bmsk_tmp "+str(bmsk_tmp.shape))
        elif index<len(self.slist1)+len(self.slist0):
            # print("*********")
            
            sind=self.slist1[index-len(self.slist0)]
            # print("index "+str(index))
            # print("sind "+str(sind))

            rimg_tmp=self.rimg.data[bind][:, sind, :]
            rimg_tmp=rimg_tmp.permute([1, 0, 2])

            if isinstance(self.bfld, torch.Tensor):
                bfld_tmp=self.bfld.data[bind][:, sind, :]
                bfld_tmp=bfld_tmp.permute([1, 0, 2])

            if isinstance(self.bmsk, torch.Tensor):
                bmsk_tmp=self.bmsk.data[bind][:, sind, :]
                bmsk_tmp=bmsk_tmp.permute([1, 0, 2])
            # print("bmsk_tmp "+str(bmsk_tmp.shape))
        else:
            # print("***************************")

            sind=self.slist2[index-len(self.slist0)-len(self.slist1)]
            # print("index "+str(index))
            # print("sind "+str(sind))

            rimg_tmp=self.rimg.data[bind][:, :, sind]
            rimg_tmp=rimg_tmp.permute([2, 0, 1])
            
            if isinstance(self.bfld, torch.Tensor):
                bfld_tmp=self.bfld.data[bind][:, :, sind]
                bfld_tmp=bfld_tmp.permute([2, 0, 1])
        
            if isinstance(self.bmsk, torch.Tensor):
                bmsk_tmp=self.bmsk.data[bind][:, :, sind]
                bmsk_tmp=bmsk_tmp.permute([2, 0, 1])
            # print("bmsk_tmp "+str(bmsk_tmp.shape))

        extend_dim=self.rescale_dim
        slice_shape=rimg_tmp.data[0].shape

        rimg_blk=torch.zeros([self.num_slice, extend_dim, extend_dim], dtype=torch.float32)
        rimg_blk[:, :slice_shape[0], :slice_shape[1]]=rimg_tmp
        
        if isinstance(self.bfld, torch.Tensor):
            bfld_blk=torch.ones([self.num_slice, extend_dim, extend_dim], dtype=torch.float32)
            bfld_blk[:, :slice_shape[0], :slice_shape[1]]=bfld_tmp
        
            return rimg_blk, bfld_blk, bmsk_blk

        if isinstance(self.bmsk, torch.Tensor):
            # print("slice shape " + str(slice_shape))

            # expand mask/t1w dimension here?!!!
            bmsk_blk=torch.zeros([self.num_class, self.num_slice, extend_dim, extend_dim], dtype=torch.float)
            bmsk_blk_np = bmsk_blk.numpy()
            bmsk_tmp_np = bmsk_tmp.numpy()

            for i in range(0, self.num_class):
                a = bmsk_tmp_np==i
                if i == 0:
                    tmsk_tmp = (1 + bmsk_tmp_np) * (a * 1) 
                else:
                    tmsk_tmp = bmsk_tmp_np * (a * 1)
                # print("tissue mask shape "+str(tmsk_tmp.shape))
                bmsk_blk_np[i, :, :slice_shape[0], :slice_shape[1]] = tmsk_tmp # How to do with torch tensor?
            
            bmsk_blk=torch.from_numpy(bmsk_blk_np)
            
            # bmsk_blk=torch.zeros([self.num_slice, extend_dim, extend_dim], dtype=torch.long) 
            # bmsk_blk[:, :slice_shape[0], :slice_shape[1]]=bmsk_tmp
            # print("bmsk_blk " + str(bmsk_blk.shape))
            return rimg_blk, bmsk_blk

        return rimg_blk


if __name__ == '__main__':
    volume_dataset=VolumeDataset(rimg_in=None, cimg_in='../data/human_init_test/train/t1w', bmsk_in='../data/human_init_test/train/mask')
    volume_loader=data.DataLoader(dataset=volume_dataset, batch_size=1, shuffle=True)
    for i, (cimg, bmsk) in enumerate(volume_loader):
        block_dataset=BlockDataset(rimg=cimg, bfld=None, bmsk=bmsk, num_slice=3, num_class=7, rescale_dim=256)
        block_loader=data.DataLoader(dataset=block_dataset, batch_size=1, shuffle=True)
        for j, (cimg_blk, bmsk_blk) in enumerate(block_loader):
            # if j==0:
            #     bmsk_blk.__getitem__
            print(bmsk_blk.shape) #(1, 3, 256, 256)
            print(np.unique(bmsk_blk.numpy()))
