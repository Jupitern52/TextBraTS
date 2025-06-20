# TextBraTS

A text-image public dataset with novel text-guided 3D brain tumor segmentation.

---

## Introduction

**TextBraTS** is an open-access dataset designed to advance research in text-guided 3D brain tumor segmentation. It includes paired multi-modal brain MRI scans and expertly annotated radiology reports, enabling the development and evaluation of multi-modal deep learning models that bridge vision and language in neuro-oncology.

![TextBraTS Overview](assets/datasample.PNG)

## Features

- Multi-modal 3D brain MRI scans with expert-annotated segmentation (T1, T1ce, T2, FLAIR) from BraTS20 challenge training set
- Structured radiology reports for each case
- Text-image alignment method for research on multi-modal fusion

![TextBraTS Overview](assets/overview.PNG)

## Usage

You can use this dataset for:
- Developing and benchmarking text-guided segmentation models
- Evaluating multi-modal fusion algorithms in medical imaging
- Research in language-driven medical AI

## Installing Dependencies
Run the following commands to set up the environment:
<pre>conda env create -f environment.yml 
pip install git+https://github.com/Project-MONAI/MONAI.git@07de215c </pre>
If you need to activate the environment, use:
<pre>conda activate TextBraTS </pre>

## Dataset

Due to BraTS official guidelines, MRI images must be downloaded directly from the [BraTS 2020 challenge website](https://www.med.upenn.edu/cbica/brats2020/data.html) (training set).

Our provided text reports, feature files, and prompt files are named to match the original BraTS folder IDs exactly. You can simply merge them with the downloaded MRI data.

**Download our text, feature, and prompt files:**  
[https://drive.google.com/file/d/1i1R6_bVY4VbNtxEIQVsiXUSWuVAtgJhg/view?usp=sharing](https://drive.google.com/file/d/1i1R6_bVY4VbNtxEIQVsiXUSWuVAtgJhg/view?usp=sharing)

## Inference

We provide our pre-trained weights for direct inference and evaluation.  
Download the weights from the following link:

[https://drive.google.com/file/d/147283LL2fRDcTYR_vQA-95vbZysjjD1v/view?usp=sharing](https://drive.google.com/file/d/147283LL2fRDcTYR_vQA-95vbZysjjD1v/view?usp=sharing)

After downloading, place the weights in your desired directory, then run the following command for inference:

```bash
python test.py --pretrained_dir=/path/to/your/weights/ --exp_name=TextBraTS```

## Training

If you would like to train the model from scratch, please use the following command:

```bash
python main.py --distributed --use_ssl_pretrained --save_checkpoint --logdir=TextBraTS

- The `--use_ssl_pretrained` option utilizes the pre-trained weights from NVIDIA's Swin UNETR model.
- Download the Swin UNETR pre-trained weights from:  
  [https://drive.google.com/file/d/1FJ0N_Xo3olzAV-oojEkAsbsUgiFsoPdl/view?usp=sharing](https://drive.google.com/file/d/1FJ0N_Xo3olzAV-oojEkAsbsUgiFsoPdl/view?usp=sharing)
- Please place the downloaded weights in the appropriate directory as specified in your configuration or script.


## Citation

If you use TextBraTS in your research, please cite:

```bibtex
@inproceedings{shi2025textbrats,
  title = {TextBraTS: Text-Guided Volumetric Brain Tumor Segmentation with Innovative Dataset Development and Fusion Module Exploration},
  author = {Shi, Xiaoyu and Jain, Rahul Kumar and Li, Yinhao and Hou, Ruibo and Cheng, Jingliang and Bai, Jie and Zhao, Guohua and Lin, Lanfen and Xu, Rui and Chen, Yen-wei},
  booktitle = {Proceedings of the International Conference on Medical Image Computing and Computer Assisted Intervention (MICCAI)},
  year = {2025},
  note = {to appear}
}
