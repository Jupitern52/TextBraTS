# Copyright 2020 - 2022 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from utils.data_utils import get_loader
from utils.textswin_unetr import TextSwinUNETR
import os
import time
import torch
import torch.nn.parallel
import torch.utils.data.distributed
from utils.utils import AverageMeter
from monai.utils.enums import MetricReduction
from monai.metrics import DiceMetric, HausdorffDistanceMetric


parser = argparse.ArgumentParser(description="TextBraTS segmentation pipeline")
parser.add_argument("--data_dir", default="./data/TextBraTSData", type=str, help="dataset directory")
parser.add_argument("--exp_name", default="TextBraTS", type=str, help="experiment name")
parser.add_argument("--json_list", default="Test.json", type=str, help="dataset json file")
parser.add_argument("--fold", default=0, type=int, help="data fold")
parser.add_argument("--pretrained_model_name", default="model.pt", type=str, help="pretrained model name")
parser.add_argument("--feature_size", default=48, type=int, help="feature size")
parser.add_argument("--infer_overlap", default=0.6, type=float, help="sliding window inference overlap")
parser.add_argument("--in_channels", default=4, type=int, help="number of input channels")
parser.add_argument("--out_channels", default=3, type=int, help="number of output channels")
parser.add_argument("--a_min", default=-175.0, type=float, help="a_min in ScaleIntensityRanged")
parser.add_argument("--a_max", default=250.0, type=float, help="a_max in ScaleIntensityRanged")
parser.add_argument("--b_min", default=0.0, type=float, help="b_min in ScaleIntensityRanged")
parser.add_argument("--b_max", default=1.0, type=float, help="b_max in ScaleIntensityRanged")
parser.add_argument("--space_x", default=1.5, type=float, help="spacing in x direction")
parser.add_argument("--space_y", default=1.5, type=float, help="spacing in y direction")
parser.add_argument("--space_z", default=2.0, type=float, help="spacing in z direction")
parser.add_argument("--roi_x", default=128, type=int, help="roi size in x direction")
parser.add_argument("--roi_y", default=128, type=int, help="roi size in y direction")
parser.add_argument("--roi_z", default=128, type=int, help="roi size in z direction")
parser.add_argument("--dropout_rate", default=0.0, type=float, help="dropout rate")
parser.add_argument("--distributed", action="store_true", help="start distributed training")
parser.add_argument("--workers", default=8, type=int, help="number of workers")
parser.add_argument("--RandScaleIntensityd_prob", default=0.1, type=float, help="RandScaleIntensityd aug probability")
parser.add_argument("--RandShiftIntensityd_prob", default=0.1, type=float, help="RandShiftIntensityd aug probability")
parser.add_argument("--spatial_dims", default=3, type=int, help="spatial dimension of input data")
parser.add_argument("--use_checkpoint", action="store_true", help="use gradient checkpointing to save memory")
parser.add_argument(
    "--pretrained_dir",
    default="./runs/TextBraTS/",
    type=str,
    help="pretrained checkpoint directory",
)


def main():
    args = parser.parse_args()
    args.test_mode = True
    output_directory = "./outputs/" + args.exp_name
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    test_loader = get_loader(args)
    pretrained_dir = args.pretrained_dir
    model_name = args.pretrained_model_name
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pretrained_pth = os.path.join(pretrained_dir, model_name)
    model = TextSwinUNETR(
        img_size=128,
        in_channels=args.in_channels,
        out_channels=args.out_channels,
        feature_size=args.feature_size,
        drop_rate=0.0,
        attn_drop_rate=0.0,
        dropout_path_rate=0.0,
        use_checkpoint=args.use_checkpoint,
        text_dim=768,
    )
    model_dict = torch.load(pretrained_pth)["state_dict"]
    model.load_state_dict(model_dict, strict=False)
    model.eval()
    model.to(device)

    def val_epoch(model, loader, acc_func,  hd95_func):
        model.eval()
        start_time = time.time()
        run_acc = AverageMeter()
        run_hd95 = AverageMeter()

        with torch.no_grad():
            for idx, batch_data in enumerate(loader):
                data, target, text = batch_data["image"], batch_data["label"], batch_data["text_feature"]
                data, target, text = data.cuda(), target.cuda(), text.cuda()
                logits = model(data,text)
                prob = torch.sigmoid(logits)
                prob = (prob > 0.5).int()

                acc_func(y_pred=prob, y=target)
                acc, not_nans = acc_func.aggregate()
                acc = acc.cuda()

                run_acc.update(acc.cpu().numpy(), n=not_nans.cpu().numpy())

                # HD95 Metric
                hd95_func(y_pred=prob, y=target)
                hd95 = hd95_func.aggregate()  # Assuming it returns a single value
                run_hd95.update(hd95.cpu().numpy())


                Dice_TC = run_acc.avg[0]
                Dice_WT = run_acc.avg[1]
                Dice_ET = run_acc.avg[2]
                HD95_TC = run_hd95.avg[0]
                HD95_WT = run_hd95.avg[1]
                HD95_ET = run_hd95.avg[2]
                print(
                    "Val  {}/{}".format(idx, len(loader)),
                    ", Dice_TC:", Dice_TC,
                    ", Dice_WT:", Dice_WT,
                    ", Dice_ET:", Dice_ET,
                    ", Avg Dice:", (Dice_ET + Dice_TC + Dice_WT) / 3,
                    ", HD95_TC:", HD95_TC,
                    ", HD95_WT:", HD95_WT,
                    ", HD95_ET:", HD95_ET,
                    ", Avg HD95:", (HD95_ET + HD95_TC + HD95_WT) / 3,
                    ", time {:.2f}s".format(time.time() - start_time),
                )
                start_time = time.time()
            with open(output_directory+'/log.txt', "a") as log_file:
                log_file.write(f"Experiment name:{args.pretrained_dir.split('/')[-2]}, "
            f"Final Validation Results - Dice_TC: {Dice_TC}, Dice_WT: {Dice_WT}, Dice_ET: {Dice_ET}, "
            f"Avg Dice: {(Dice_ET + Dice_TC + Dice_WT) / 3}, "
            f"HD95_TC: {HD95_TC}, HD95_WT: {HD95_WT}, HD95_ET: {HD95_ET}, "
            f"Avg HD95: {(HD95_ET + HD95_TC + HD95_WT) / 3}\n")
        return run_acc.avg

    dice_acc = DiceMetric(include_background=True, reduction=MetricReduction.MEAN_BATCH, get_not_nans=True)
    hd95_acc = HausdorffDistanceMetric(include_background=True, reduction=MetricReduction.MEAN_BATCH, percentile=95.0)
    val_epoch(model, test_loader, acc_func=dice_acc,hd95_func=hd95_acc)

if __name__ == "__main__":
    main()
