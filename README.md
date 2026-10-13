TextBraTS

Bridging 3D MRI, text, and genotype for data-efficient glioma segmentation and radiogenomic analysis.

News

JBHI acceptance: Our extended work, “TextBraTS: Bridging 3D MRI, Text, and Genotype for Data-Efficient Glioma Segmentation and Analysis,” has been accepted by the IEEE Journal of Biomedical and Health Informatics (JBHI) and is available in Early Access: 10.1109/JBHI.2026.3725368.

Upcoming release: The code and updated dataset accompanying the JBHI extension are currently being prepared and will be released soon. This README will be updated with the new resources and usage instructions.

Our initial TextBraTS work appeared at MICCAI 2025. The preprint is available on [arxiv:2506.16784](https://arxiv.org/abs/2506.16784).

Introduction

TextBraTS is a multimodal dataset and research framework for text-guided 3D glioma segmentation and radiogenomic analysis. Building on BraTS 2020 and TCGA cohorts, the JBHI extension brings together volumetric MRI, expert-verified textual descriptions, and available IDH mutation labels to study the contribution of structured textual information to segmentation and molecular characterization.

Our data construction pipeline combines LLM-assisted report generation, radiologist verification, and clinical narrative standardization. MRI-derived descriptions are refined into structured attributes covering lesion location, edema, necrosis, and ventricular compression. A Multi-level Gated Fusion (MGF) network integrates these textual features with 3D visual representations at multiple stages.

The JBHI study extends our preliminary work with:

An LLM-driven Clinical Narrative Standardization protocol that converts narrative descriptions into structured semantic attributes.

Statistical analyses of text and feature distributions.

The MGF architecture for incorporating distilled textual features into 3D segmentation.

Expanded evaluation, including ablation studies, shuffled-text robustness experiments, external-cohort testing, and exploratory IDH mutation prediction.

The textual descriptions are semi-synthetic: generated from MRI and refined by experts. TextBraTS therefore provides a controlled benchmark for studying structured text guidance; its results should be interpreted in this setting, rather than as performance with independently acquired clinical reports.



<img width="1009" height="639" alt="TextBraTS illustration" src="https://github.com/user-attachments/assets/9184f02b-de69-441d-99de-1030caa3d179" />

Features

Volumetric MRI: Multi-sequence brain MRI, including T1, T1ce, T2, and FLAIR, with tumor segmentation annotations from BraTS.

Expert-verified text: MRI-derived descriptions reviewed and refined by radiologists.

Structured semantic attributes: Standardized descriptions of lesion location, edema, necrosis, and ventricular compression.

Text-guided segmentation: Multimodal fusion for studying the contribution of textual information to 3D glioma segmentation.

Radiogenomic analysis: Integration of imaging, text, and available IDH mutation information in the JBHI extension.



Release Status

The download links and commands below describe the existing TextBraTS release.

The JBHI extension code and updated dataset are being prepared for release. Updated documentation, download links, and instructions for reproducing the extended experiments will be added when they become available.

Usage

TextBraTS supports research on:

Text-guided volumetric glioma segmentation.

Multimodal fusion of 3D MRI and textual descriptions.

Clinical narrative standardization and structured semantic guidance.

Data-efficient medical image segmentation.

Multimodal IDH mutation prediction and radiogenomic analysis.

Installing Dependencies

Set up the environment:

conda env create -f environment.yml
conda activate TextBraTS
pip install git+https://github.com/Project-MONAI/MONAI.git@07de215c

Dataset

MRI Data

MRI scans must be obtained from the original data providers in accordance with their access requirements. For the existing BraTS 2020-based release, download the training images from the BraTS 2020 challenge website.

Existing TextBraTS Release

Download the text, feature, and prompt files from:

Google Drive

Hugging Face

The provided files preserve the original BraTS subject identifiers to support alignment with the MRI data. Configure the paths in merge.py, then run:

python merge.py

To change the dataset split, modify Train.json and Test.json accordingly.

JBHI Extension

The updated dataset accompanying the JBHI article is being prepared. Release details and documentation for the expert-refined narratives, distilled attributes, and available genotype information will be added here.

Inference

For the existing release, download the pre-trained checkpoint.

Place the weights in your desired directory and run:

python test.py --pretrained_dir=/path/to/your/weights/ --exp_name=TextBraTS

Instructions for the JBHI extension will be provided with its code release.

Training

For the existing release, configure main.py and run:

python main.py --distributed --use_ssl_pretrained --save_checkpoint --logdir=TextBraTS

The --use_ssl_pretrained option uses pre-trained weights from NVIDIA's Swin UNETR model.

Download the Swin UNETR pre-trained weights.

Configure the corresponding weights path before training.

Citation

Please cite the publication relevant to the dataset, methods, or experiments used in your work.

JBHI Extension

X. Shi et al., “TextBraTS: Bridging 3D MRI, Text, and Genotype for Data-Efficient Glioma Segmentation and Analysis,” IEEE Journal of Biomedical and Health Informatics, early access, doi: 10.1109/JBHI.2026.3725368.

MICCAI 2025

@inproceedings{shi2025textbrats,
  title = {TextBraTS: Text-Guided Volumetric Brain Tumor Segmentation with Innovative Dataset Development and Fusion Module Exploration},
  author = {Shi, Xiaoyu and Jain, Rahul Kumar and Li, Yinhao and Hou, Ruibo and Cheng, Jingliang and Bai, Jie and Zhao, Guohua and Lin, Lanfen and Xu, Rui and Chen, Yen-wei},
  booktitle = {Medical Image Computing and Computer Assisted Intervention -- MICCAI 2025},
  pages = {638--648},
  year = {2025},
  publisher = {Springer}
}
