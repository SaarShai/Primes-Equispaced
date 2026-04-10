"""Parse COLMAP binary format (cameras.bin, images.bin, points3D.bin).

Produces camera intrinsics, per-image extrinsics (as 4x4 world-to-camera matrices),
and the SfM point cloud with colors for Gaussian initialization.

References:
  - COLMAP binary format: https://colmap.github.io/format.html
  - Original 3DGS COLMAP reader: graphdeco-inria/gaussian-splatting
"""

import struct
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Tuple

import numpy as np
from PIL import Image


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

class CameraIntrinsics(NamedTuple):
    """Camera intrinsic parameters."""
    camera_id: int
    model: str          # SIMPLE_PINHOLE, PINHOLE, OPENCV, etc.
    width: int
    height: int
    fx: float
    fy: float
    cx: float
    cy: float


class ImageMeta(NamedTuple):
    """Per-image metadata from COLMAP."""
    image_id: int
    qw: float
    qx: float
    qy: float
    qz: float
    tx: float
    ty: float
    tz: float
    camera_id: int
    name: str


class SfMPoint(NamedTuple):
    """3D point from Structure-from-Motion."""
    xyz: np.ndarray         # (3,)
    rgb: np.ndarray         # (3,) uint8
    error: float


# ---------------------------------------------------------------------------
# COLMAP binary readers
# ---------------------------------------------------------------------------

def _read_next_bytes(fid, num_bytes, format_char_sequence, endian_character="<"):
    """Read and unpack bytes from a binary file."""
    data = fid.read(num_bytes)
    return struct.unpack(endian_character + format_char_sequence, data)


def read_cameras_binary(path: Path) -> Dict[int, CameraIntrinsics]:
    """Read cameras.bin -> dict of camera_id -> CameraIntrinsics."""
    cameras = {}
    with open(path, "rb") as f:
        num_cameras = _read_next_bytes(f, 8, "Q")[0]
        for _ in range(num_cameras):
            camera_id, model_id, width, height = _read_next_bytes(f, 24, "iiQQ")

            # Model IDs: 0=SIMPLE_PINHOLE, 1=PINHOLE, 2=SIMPLE_RADIAL, 4=OPENCV
            if model_id == 0:  # SIMPLE_PINHOLE: f, cx, cy
                params = _read_next_bytes(f, 24, "ddd")
                fx = fy = params[0]
                cx, cy = params[1], params[2]
                model = "SIMPLE_PINHOLE"
            elif model_id == 1:  # PINHOLE: fx, fy, cx, cy
                params = _read_next_bytes(f, 32, "dddd")
                fx, fy, cx, cy = params
                model = "PINHOLE"
            elif model_id == 2:  # SIMPLE_RADIAL: f, cx, cy, k
                params = _read_next_bytes(f, 32, "dddd")
                fx = fy = params[0]
                cx, cy = params[1], params[2]
                model = "SIMPLE_RADIAL"
            elif model_id == 4:  # OPENCV: fx, fy, cx, cy, k1, k2, p1, p2
                params = _read_next_bytes(f, 64, "dddddddd")
                fx, fy, cx, cy = params[0], params[1], params[2], params[3]
                model = "OPENCV"
            else:
                # Fallback: read num_params doubles based on model
                # Common models and their param counts
                num_params_map = {
                    0: 3, 1: 4, 2: 4, 3: 5, 4: 8, 5: 5, 6: 5, 7: 12, 8: 4, 9: 5, 10: 4
                }
                n_params = num_params_map.get(model_id, 4)
                params = _read_next_bytes(f, 8 * n_params, "d" * n_params)
                fx = fy = params[0]
                cx = params[1] if len(params) > 1 else width / 2
                cy = params[2] if len(params) > 2 else height / 2
                model = f"MODEL_{model_id}"

            cameras[camera_id] = CameraIntrinsics(
                camera_id=camera_id,
                model=model,
                width=int(width),
                height=int(height),
                fx=float(fx),
                fy=float(fy),
                cx=float(cx),
                cy=float(cy),
            )
    return cameras


def read_images_binary(path: Path) -> Dict[int, ImageMeta]:
    """Read images.bin -> dict of image_id -> ImageMeta."""
    images = {}
    with open(path, "rb") as f:
        num_images = _read_next_bytes(f, 8, "Q")[0]
        for _ in range(num_images):
            image_id = _read_next_bytes(f, 4, "i")[0]
            qw, qx, qy, qz = _read_next_bytes(f, 32, "dddd")
            tx, ty, tz = _read_next_bytes(f, 24, "ddd")
            camera_id = _read_next_bytes(f, 4, "i")[0]

            # Read image name (null-terminated string)
            name_chars = []
            while True:
                ch = f.read(1)
                if ch == b"\x00":
                    break
                name_chars.append(ch.decode("utf-8"))
            name = "".join(name_chars)

            # Read 2D points (we skip them but must consume the bytes)
            num_points2d = _read_next_bytes(f, 8, "Q")[0]
            # Each point2D: x(double), y(double), point3D_id(long long)
            f.read(num_points2d * 24)

            images[image_id] = ImageMeta(
                image_id=image_id,
                qw=qw, qx=qx, qy=qy, qz=qz,
                tx=tx, ty=ty, tz=tz,
                camera_id=camera_id,
                name=name,
            )
    return images


def read_points3d_binary(path: Path) -> List[SfMPoint]:
    """Read points3D.bin -> list of SfMPoint."""
    points = []
    with open(path, "rb") as f:
        num_points = _read_next_bytes(f, 8, "Q")[0]
        for _ in range(num_points):
            # point3D_id (long long), xyz (3 doubles), rgb (3 unsigned chars), error (double)
            point3d_id = _read_next_bytes(f, 8, "Q")[0]
            xyz = np.array(_read_next_bytes(f, 24, "ddd"))
            rgb = np.array(_read_next_bytes(f, 3, "BBB"))
            error = _read_next_bytes(f, 8, "d")[0]
            # Track length: num_elements, then pairs of (image_id, point2d_idx)
            track_length = _read_next_bytes(f, 8, "Q")[0]
            f.read(track_length * 8)  # Each element: image_id(int) + point2d_idx(int)

            points.append(SfMPoint(xyz=xyz, rgb=rgb, error=error))
    return points


# ---------------------------------------------------------------------------
# Quaternion -> rotation matrix
# ---------------------------------------------------------------------------

def quat_to_rotmat(qw: float, qx: float, qy: float, qz: float) -> np.ndarray:
    """Convert quaternion (w, x, y, z) to 3x3 rotation matrix."""
    # Normalize
    norm = np.sqrt(qw * qw + qx * qx + qy * qy + qz * qz)
    qw, qx, qy, qz = qw / norm, qx / norm, qy / norm, qz / norm

    R = np.array([
        [1 - 2*(qy*qy + qz*qz), 2*(qx*qy - qz*qw),     2*(qx*qz + qy*qw)],
        [2*(qx*qy + qz*qw),     1 - 2*(qx*qx + qz*qz), 2*(qy*qz - qx*qw)],
        [2*(qx*qz - qy*qw),     2*(qy*qz + qx*qw),     1 - 2*(qx*qx + qy*qy)],
    ])
    return R


def image_meta_to_world2cam(meta: ImageMeta) -> np.ndarray:
    """Convert COLMAP image metadata to 4x4 world-to-camera matrix.

    COLMAP stores the world-to-camera rotation and translation directly:
        R = rotation_matrix(q)
        t = [tx, ty, tz]
        world_point_in_cam = R @ world_point + t
    """
    R = quat_to_rotmat(meta.qw, meta.qx, meta.qy, meta.qz)
    t = np.array([meta.tx, meta.ty, meta.tz])

    w2c = np.eye(4)
    w2c[:3, :3] = R
    w2c[:3, 3] = t
    return w2c


def world2cam_to_cam_center(w2c: np.ndarray) -> np.ndarray:
    """Get camera center in world coordinates from world2cam matrix.

    camera_center = -R^T @ t
    """
    R = w2c[:3, :3]
    t = w2c[:3, 3]
    return -R.T @ t


# ---------------------------------------------------------------------------
# High-level scene loader
# ---------------------------------------------------------------------------

class SceneData:
    """Container for a loaded COLMAP scene."""

    def __init__(
        self,
        cameras: Dict[int, CameraIntrinsics],
        train_metas: List[ImageMeta],
        test_metas: List[ImageMeta],
        points_xyz: np.ndarray,         # (N, 3) float64
        points_rgb: np.ndarray,         # (N, 3) float64 in [0, 1]
        image_dir: Path,
    ):
        self.cameras = cameras
        self.train_metas = train_metas
        self.test_metas = test_metas
        self.points_xyz = points_xyz
        self.points_rgb = points_rgb
        self.image_dir = image_dir

    @property
    def num_train(self) -> int:
        return len(self.train_metas)

    @property
    def num_test(self) -> int:
        return len(self.test_metas)

    @property
    def num_points(self) -> int:
        return self.points_xyz.shape[0]

    def get_intrinsics(self, meta: ImageMeta) -> CameraIntrinsics:
        return self.cameras[meta.camera_id]

    def get_world2cam(self, meta: ImageMeta) -> np.ndarray:
        return image_meta_to_world2cam(meta)

    def load_image(self, meta: ImageMeta, downscale: int = 1) -> np.ndarray:
        """Load image as float32 array (H, W, 3) in [0, 1]."""
        img_path = self.image_dir / meta.name
        img = Image.open(img_path)
        if downscale > 1:
            w, h = img.size
            img = img.resize((w // downscale, h // downscale), Image.LANCZOS)
        return np.array(img, dtype=np.float32) / 255.0


def load_scene(
    data_dir: str,
    images_subdir: str = "images_4",
    test_every: int = 8,
) -> SceneData:
    """Load a COLMAP scene from disk.

    Args:
        data_dir: Path to scene root (e.g., data/mipnerf360/garden)
        images_subdir: Subdirectory containing images (images, images_2, images_4, images_8)
        test_every: Every Nth image (sorted by name) is held out for testing

    Returns:
        SceneData with parsed cameras, train/test splits, and SfM points.
    """
    data_path = Path(data_dir)

    # Find COLMAP sparse reconstruction
    sparse_dir = data_path / "sparse" / "0"
    if not sparse_dir.exists():
        # Try without the /0 subdirectory
        sparse_dir = data_path / "sparse"
    assert sparse_dir.exists(), f"COLMAP sparse dir not found at {sparse_dir}"

    cameras_path = sparse_dir / "cameras.bin"
    images_path = sparse_dir / "images.bin"
    points_path = sparse_dir / "points3D.bin"

    assert cameras_path.exists(), f"cameras.bin not found at {cameras_path}"
    assert images_path.exists(), f"images.bin not found at {images_path}"
    assert points_path.exists(), f"points3D.bin not found at {points_path}"

    # Parse COLMAP binaries
    cameras = read_cameras_binary(cameras_path)
    images_dict = read_images_binary(images_path)
    sfm_points = read_points3d_binary(points_path)

    # Determine image directory
    image_dir = data_path / images_subdir
    if not image_dir.exists():
        # Fall back to full-res images
        image_dir = data_path / "images"
    assert image_dir.exists(), f"Image directory not found at {image_dir}"

    # If using downscaled images, adjust intrinsics
    # Check actual image size vs COLMAP camera size to compute scale factor
    sample_meta = list(images_dict.values())[0]
    sample_cam = cameras[sample_meta.camera_id]
    sample_img_path = image_dir / sample_meta.name
    if sample_img_path.exists():
        with Image.open(sample_img_path) as img:
            actual_w, actual_h = img.size
        scale_x = actual_w / sample_cam.width
        scale_y = actual_h / sample_cam.height

        if abs(scale_x - 1.0) > 0.01 or abs(scale_y - 1.0) > 0.01:
            # Adjust all camera intrinsics for the downscaled images
            adjusted_cameras = {}
            for cid, cam in cameras.items():
                adjusted_cameras[cid] = CameraIntrinsics(
                    camera_id=cam.camera_id,
                    model=cam.model,
                    width=int(cam.width * scale_x),
                    height=int(cam.height * scale_y),
                    fx=cam.fx * scale_x,
                    fy=cam.fy * scale_y,
                    cx=cam.cx * scale_x,
                    cy=cam.cy * scale_y,
                )
            cameras = adjusted_cameras

    # Sort images by filename for deterministic train/test split
    sorted_metas = sorted(images_dict.values(), key=lambda m: m.name)

    train_metas = []
    test_metas = []
    for i, meta in enumerate(sorted_metas):
        if i % test_every == 0:
            test_metas.append(meta)
        else:
            train_metas.append(meta)

    # Extract point cloud
    points_xyz = np.stack([p.xyz for p in sfm_points], axis=0)          # (N, 3)
    points_rgb = np.stack([p.rgb for p in sfm_points], axis=0) / 255.0  # (N, 3) [0, 1]

    print(f"[COLMAP] Loaded scene: {data_path.name}")
    print(f"  Cameras: {len(cameras)}")
    print(f"  Images: {len(sorted_metas)} (train={len(train_metas)}, test={len(test_metas)})")
    print(f"  SfM points: {points_xyz.shape[0]}")
    print(f"  Image dir: {image_dir}")

    return SceneData(
        cameras=cameras,
        train_metas=train_metas,
        test_metas=test_metas,
        points_xyz=points_xyz,
        points_rgb=points_rgb,
        image_dir=image_dir,
    )
