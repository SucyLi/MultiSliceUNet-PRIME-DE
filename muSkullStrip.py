#!/usr/bin/env python
import torch
import torch.nn as nn
from function import predict_volumes
from model import UNet2d
import os, sys
import argparse
from quicknat import QuickNat
from solver import Solver

if __name__=='__main__':
    NoneType=type(None)
    # Argument
    parser=argparse.ArgumentParser(description='Skull Stripping', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    optional=parser._action_groups.pop()
    required=parser.add_argument_group('required arguments')
    # Required Options
    required.add_argument('-in', '--input_t1w', type=str, required=True, help='Input T1w Image for Skull Stripping')
    required.add_argument('-model', '--predict_model', required=True, type=str, help='Predict Model')
    # Optional Options
    optional.add_argument('-out', '--out_dir', type=str, help='Output Dir')
    optional.add_argument('-suffix', '--mask_suffix', type=str, default="pre_mask", help='Suffix of Mask')
    optional.add_argument('-class', '--num_class', type=int, default=7, help='Number of Class for Model Input')
    optional.add_argument('-slice', '--input_slice', type=int, default=3, help='Number of Slice for Model Input')
    optional.add_argument('-conv', '--conv_block', type=int, default=5, help='Number of UNet Block')
    optional.add_argument('-kernel', '--kernel_root', type=int, default=16, help='Number of the Root of Kernel')
    optional.add_argument('-rescale', '--rescale_dim', type=int, default=256, help='Number of the Root of Kernel')
    parser._action_groups.append(optional)
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    # Define whether show slice results
    
    quicknat_model = QuickNat(net_params)
    solver = Solver(quicknat_model,
                device=common_params['device'],
                num_class=args.num_class,
                optim_args={"lr": train_params['learning_rate'],
                            "betas": train_params['optim_betas'],
                            "eps": train_params['optim_eps'],
                            "weight_decay": train_params['optim_weight_decay']},
                model_name=common_params['model_name'],
                exp_name=train_params['exp_name'],
                labels=data_params['labels'],
                log_nth=train_params['log_nth'],
                num_epochs=train_params['num_epochs'],
                lr_scheduler_step_size=train_params['lr_scheduler_step_size'],
                lr_scheduler_gamma=train_params['lr_scheduler_gamma'],
                use_last_checkpoint=train_params['use_last_checkpoint'],
                log_dir=common_params['log_dir'],
                exp_dir=common_params['exp_dir'])

    solver.train(train_loader, val_loader)
    final_model_path = os.path.join(common_params['save_model_dir'], train_params['final_model_file'])
    quicknat_model.save(final_model_path)
    print("final model saved @ " + str(final_model_path))

    # train_model=UNet2d(dim_in=args.input_slice, num_class=args.num_class, num_conv_block=args.conv_block, kernel_root=args.kernel_root)
    # checkpoint=torch.load(args.predict_model, map_location={'cuda:0':'cpu'})
    # train_model.load_state_dict(checkpoint['state_dict'])
    # model=nn.Sequential(train_model, nn.Softmax2d())

    # predict_volumes(model, cimg_in=args.input_t1w, bmsk_in=None, rescale_dim=args.rescale_dim, num_class=args.num_class, save_dice=False,
    #         save_nii=True, nii_outdir=args.out_dir, suffix=args.mask_suffix)
