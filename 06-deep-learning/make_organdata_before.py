# Simulate "raw" (not yet preprocessed) data from OrganData:
# every case is resampled to a random voxel spacing, so cases no longer share a common grid.
#   in-plane (x = y) and slice (z) spacing drawn from [0.3, 2.1] mm, with z > x = y
# The physical extent, origin and direction are kept, so the anatomy is unchanged; only the grid differs.
# Images use linear interpolation, masks nearest neighbour (labels stay integers).
# Output types: images float32, masks int8.
# Comparison set (python make_organdata_before.py --large -> OrganDataBeforeLarge): same spacings and values,
# but stored in wasteful types: masks float32, and the first case (image + mask) float64.
import sys
from pathlib import Path
import numpy as np
import SimpleITK as sitk

SRC = Path(__file__).resolve().parent.parent / "OrganData"
SPACING_RANGE = (0.3, 2.1)
SEED = 0


def resample(image, spacing, interpolator):
    size = [max(1, int(round(n * s_old / s_new)))
            for n, s_old, s_new in zip(image.GetSize(), image.GetSpacing(), spacing)]
    return sitk.Resample(image, size, sitk.Transform(), interpolator,
                         image.GetOrigin(), spacing, image.GetDirection(),
                         0, image.GetPixelID())


def main(dst, img_type=sitk.sitkFloat32, mask_type=sitk.sitkInt8, first_type=None):
    # first_type: if given, the first case (image and mask) is stored with this type instead
    dst.mkdir(exist_ok=True)
    rng = np.random.default_rng(SEED)
    for n, img_path in enumerate(sorted(SRC.glob("*_img.nii*"))):
        mask_path = img_path.with_name(img_path.name.replace("_img", "_mask"))
        xy, z = sorted(rng.uniform(*SPACING_RANGE, size=2))   # smaller -> in-plane, larger -> slices
        spacing = (float(xy), float(xy), float(z))

        img = sitk.ReadImage(str(img_path), sitk.sitkFloat32)   # source images are mixed uint16/float32/float64
        mask = sitk.ReadImage(str(mask_path), sitk.sitkInt8)     # source masks are mixed uint16/float32; labels 0-8
        new_img = resample(img, spacing, sitk.sitkLinear)
        new_mask = resample(mask, spacing, sitk.sitkNearestNeighbor)
        out_img_type, out_mask_type = (first_type, first_type) if n == 0 and first_type else (img_type, mask_type)
        sitk.WriteImage(sitk.Cast(new_img, out_img_type), str(dst / img_path.name))
        sitk.WriteImage(sitk.Cast(new_mask, out_mask_type), str(dst / mask_path.name))
        print(f"{img_path.name:16s} {img.GetSize()} @ {tuple(round(s, 2) for s in img.GetSpacing())}"
              f"  ->  {new_img.GetSize()} @ {tuple(round(s, 2) for s in spacing)}"
              f"  [{sitk.GetPixelIDValueAsString(out_img_type)} / {sitk.GetPixelIDValueAsString(out_mask_type)}]")


if __name__ == "__main__":
    if "--large" in sys.argv:
        main(SRC.with_name("OrganDataBeforeLarge"), mask_type=sitk.sitkFloat32, first_type=sitk.sitkFloat64)
    else:
        main(SRC.with_name("OrganDataBefore"))
