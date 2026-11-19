# Deep learning practical: preprocessing to segmentation

This sequence demonstrates a complete medical-image segmentation practical used for teaching.

1. `01_preprocessing_common_grid.ipynb` — inspect heterogeneous image geometry, resample scans and labels, crop/pad to a common grid, and verify the result.
2. `02_unet_single_organ.ipynb` — introduce a compact binary U-Net and patient-level train/validation/test splitting.
3. `03_multiorgan_segmentation.ipynb` — extend to multi-organ segmentation with MONAI, augmentation, training, and quantitative evaluation.
4. `make_organdata_before.py` — create deliberately heterogeneous voxel grids from the teaching dataset so students can see why preprocessing is necessary.

The larger pelvic MRI dataset is not included in this public portfolio. See [`../DATA.md`](../DATA.md) for details.
