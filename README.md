# Medical Imaging Teaching Portfolio

Selected Python and Jupyter teaching materials for programming, medical image analysis, deep learning, and research practice.

I developed these examples to support practical teaching in medical physics and biomedical engineering. The emphasis is on explaining technical concepts through short, reproducible examples and then connecting them to realistic medical-imaging workflows.

## Teaching areas represented

| Topic | Example material | Teaching focus |
|---|---|---|
| Python fundamentals | `01-python-basics/` | Functions, classes, file handling, and basic programming structure |
| NumPy | `02-numpy/` | Arrays, indexing, reshaping, views/copies, masking, statistics, and normalisation |
| Scientific visualisation | `03-visualisation/` | Matplotlib, distributions, paired measurements, and Bland–Altman agreement |
| Medical image I/O | `04-medical-image-io/` | SimpleITK, nibabel, NIfTI, metadata, voxel/physical coordinates, resampling, and saving |
| Classical image processing | `05-classical-image-processing/` | Intensity normalisation, filtering, thresholding, morphology, connected components, and evaluation |
| Deep learning for segmentation | `06-deep-learning/` | Preprocessing, patient-level splitting, U-Net training, multi-organ segmentation, augmentation, and evaluation |
| Evaluation & research practice | `07-evaluation-research-practice/` | Physical units, segmentation/classification metrics, data leakage, reproducibility, project structure, and large 3D data |
| Additional programming exercises | `supplementary-exercises/` | Small standalone examples used to practise programming and quantitative reasoning |

## Selected practical sequence

The `06-deep-learning` section shows a complete progression from raw medical images to a trained segmentation model:

**heterogeneous scans → geometry inspection → resampling → crop/pad → patient-level split → U-Net → multi-organ prediction → Dice/HD95/volume evaluation**

This sequence is designed to teach not only how to train a model, but also why medical-image geometry, interpolation, patient-level splitting, and appropriate evaluation matter.

## Teaching approach

The materials use worked examples followed by exercises. Wherever possible, examples connect a programming concept to a medical-imaging question—for example:

- why voxel spacing must be considered when calculating physical volume;
- why labels require nearest-neighbour interpolation during resampling;
- why train/test splitting should be performed by patient rather than image slice;
- how Dice, HD95, volume error, ROC/AUC, and agreement plots answer different evaluation questions;
- how reproducibility, environment information, and project structure support good research practice.

## Repository structure

```text
medical-imaging-teaching/
├── 01-python-basics/
├── 02-numpy/
├── 03-visualisation/
├── 04-medical-image-io/
├── 05-classical-image-processing/
├── 06-deep-learning/
├── 07-evaluation-research-practice/
├── supplementary-exercises/
├── DATA.md
├── requirements.txt
└── .gitignore
```

## Running the notebooks

Python 3.10–3.12 is recommended.

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

PyTorch installation can depend on the available CPU/GPU platform. For a CUDA system, install the appropriate PyTorch build before installing the remaining requirements.

## Data

Large medical-imaging datasets are deliberately not included in this repository. Some notebooks therefore require the corresponding teaching data to reproduce every cell. See [`DATA.md`](DATA.md).

Small non-clinical text examples used for the measurement-agreement exercises are included.

## Notes for reviewers

The repository is intended primarily as a **teaching portfolio** rather than a software package. The notebooks preserve a step-by-step classroom style so that individual concepts can be discussed, modified, and exercised interactively with students.
