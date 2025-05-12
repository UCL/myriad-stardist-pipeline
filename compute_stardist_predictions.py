"""Compute predicted pixelwise labels using StarDist models on one or more images."""

from __future__ import annotations

import argparse
import datetime
import warnings
from pathlib import Path
from typing import Callable, List, Tuple

import numpy as np
from csbdeep.utils import normalize
from stardist import gputools_available
from stardist.models import StarDist3D
from tifffile import imread


def get_model_paths(model_dir: Path) -> List[Path]:
    """Get paths to all model subdirectories in `model_dir`."""
    return [path for path in model_dir.iterdir() if path.is_dir()]


def get_image_paths(image_dir: Path, image_file_pattern: str) -> List[Path]:
    """Get paths to all image files matching `image_file_pattern` in `image_dir`."""
    return sorted(image_dir.glob(image_file_pattern))


def load_images(
    image_paths: List[Path],
    norm_min: float = 1.0,
    norm_max: float = 99.8,
    norm_axis: tuple[int, ...] = (0, 1, 2),
) -> list[np.ndarray]:
    """Load all images in `image_paths` and normalizing to `(norm_min, norm_max)`."""
    raw_images = [imread(path) for path in image_paths]
    return [
        normalize(raw_image, pmin=norm_min, pmax=norm_max, axis=norm_axis)
        for raw_image in raw_images
    ]


def print_with_timestamp(message: str) -> None:
    """Print a message `message` prepended with current timestamp in ISO format."""
    timestamp = datetime.datetime.now().isoformat()
    print(f"{timestamp}: {message}")


def compute_and_save_model_label_predictions(
    model_paths: List[Path],
    output_dir: Path,
    image_paths: List[Path],
    images: List[np.ndarray],
    n_tiles_zyx: Tuple[int, int, int],
    log_function: Callable = print_with_timestamp,
) -> None:
    for model_path in model_paths:
        log_function(f"Working on model {model_path.name}")
        model = StarDist3D(None, name=model_path.name, basedir=model_path.parent)
        model_output_dir = output_dir / model_path.name
        model_output_dir.mkdir(parents=True, exist_ok=True)
        for image, image_path in zip(images, image_paths):
            log_function(f"   Computing predictions for image {image_path.stem}...")
            labels, _ = model.predict_instances(image, n_tiles=n_tiles_zyx)
            log_function("    ...done")
            log_function(f"   There are {np.max(labels)} labels in {image_path.stem}")
            output_path = model_output_dir / (image_path.stem + "_labels.npy")
            log_function(f"   Saving predicted labels to {output_path}")
            np.save(output_path, labels)


def parse_arguments():
    """Parse command line arguments to script."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        help="Path to directory containing models to compute predictions with",
    )
    parser.add_argument(
        "--image-dir",
        type=Path,
        help="Path to directory containing images to compute predictions for",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Path to directory to output predictions for each model and image",
    )
    parser.add_argument(
        "--n-tiles-zyx",
        type=int,
        nargs=3,
        default=[8, 12, 12],
        help="Number of tiles to split each image into along Z, Y and X axes",
    )
    parser.add_argument(
        "--image-file-pattern",
        default="*.tif",
        help="Pattern to use to match image files in image directory",
    )
    parser.add_argument(
        "--image-norm-min",
        type=float,
        default=1.0,
        help="Minimum value to normalize image pixel values to",
    )
    parser.add_argument(
        "--image-norm-max",
        type=float,
        default=99.8,
        help="Maximum value to normalize image pixels to",
    )
    parser.add_argument(
        "--image-norm-axis",
        type=int,
        nargs="+",
        default=[0, 1, 2],
        help="Axis or axes to normalize images across",
    )
    return parser.parse_args()


def main() -> None:
    """Parse command line arguments, load models and images and compute predictions."""
    args = parse_arguments()
    if not gputools_available():
        warnings.warn(
            "gputools not available - computation will occur on CPU", stacklevel=2
        )
    model_paths = get_model_paths(args.model_dir)
    print_with_timestamp(f"Found {len(model_paths)} models")
    image_paths = get_image_paths(args.image_dir, args.image_file_pattern)
    print_with_timestamp(f"Found {len(image_paths)} images")
    print_with_timestamp("Starting loading images...")
    images = load_images(
        image_paths,
        args.image_norm_min,
        args.image_norm_max,
        tuple(args.image_norm_axis),
    )
    print_with_timestamp("...done")
    compute_and_save_model_label_predictions(
        model_paths, args.output_dir, image_paths, images, args.n_tiles_zyx
    )


if __name__ == "__main__":
    main()
