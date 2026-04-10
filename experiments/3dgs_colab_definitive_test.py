#!/usr/bin/env python3
"""
=============================================================================
DEFINITIVE TEST: Farey-Guided vs Standard ADC Densification on Real 3DGS
=============================================================================

Google Colab notebook (T4 GPU). Copy each cell block into a Colab cell.
Tests on bicycle scene from Mip-NeRF 360 dataset.
30K iterations, 3 random seeds, reports PSNR / SSIM / LPIPS / count / time.

Author: Saar Shai (Farey Sequence Research Project)
Date: 2026-03-29
"""

# ============================================================================
# CELL 1: Environment Setup (run once)
# ============================================================================

"""
# %%
# --- CELL 1: Install dependencies ---
# Colab already has PyTorch+CUDA. Only install gsplat and metric libraries.
# If gsplat 1.5.0 fails, try: pip install gsplat (latest)
!pip install gsplat==1.5.0
!pip install lpips scikit-image plyfile tqdm matplotlib pandas

import torch
print(f"PyTorch: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
assert torch.cuda.is_available(), "This notebook requires a GPU. Go to Runtime > Change runtime type > T4 GPU"

# Verify gsplat
import gsplat
print(f"gsplat: {gsplat.__version__}")
"""

# ============================================================================
# CELL 2: Download bicycle scene
# ============================================================================

"""
# %%
# --- CELL 2: Download Mip-NeRF 360 bicycle scene ---
import os

SCENE = "bicycle"
DATA_ROOT = "/content/nerf_data"
SCENE_DIR = f"{DATA_ROOT}/{SCENE}"

if not os.path.exists(SCENE_DIR):
    os.makedirs(DATA_ROOT, exist_ok=True)
    # Mip-NeRF 360 scenes hosted by the original authors
    !wget -q -O /content/bicycle.zip "http://storage.googleapis.com/gresearch/refraw360/bicycle.zip"
    !cd {DATA_ROOT} && unzip -q /content/bicycle.zip
    !rm /content/bicycle.zip
    print(f"Downloaded bicycle scene to {SCENE_DIR}")
else:
    print(f"Scene already exists at {SCENE_DIR}")

# Verify
import glob
n_images = len(glob.glob(f"{SCENE_DIR}/images/*.JPG")) + len(glob.glob(f"{SCENE_DIR}/images/*.jpg"))
print(f"Found {n_images} images")
assert os.path.exists(f"{SCENE_DIR}/sparse/0/cameras.bin"), "COLMAP data missing!"
print("COLMAP sparse reconstruction found.")
"""

# ============================================================================
# CELL 3: Core imports and COLMAP loader
# ============================================================================

"""
# %%
# --- CELL 3: Imports, COLMAP loader, dataset class ---

import os, sys, time, json, math, struct, collections
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from tqdm import tqdm
from dataclasses import dataclass
import matplotlib.pyplot as plt
import pandas as pd

DEVICE = torch.device("cuda")
SCENE_DIR = "/content/nerf_data/bicycle"


# ---------------------------------------------------------------------------
# COLMAP binary reader (cameras.bin, images.bin, points3D.bin)
# ---------------------------------------------------------------------------

CameraModel = collections.namedtuple("CameraModel", ["model_id", "model_name", "num_params"])
Camera = collections.namedtuple("Camera", ["id", "model", "width", "height", "params"])
BaseImage = collections.namedtuple("Image", ["id", "qvec", "tvec", "camera_id", "name", "xys", "point3D_ids"])
Point3D = collections.namedtuple("Point3D", ["id", "xyz", "rgb", "error", "image_ids", "point2D_idxs"])

CAMERA_MODELS = {
    0: CameraModel(0, "SIMPLE_PINHOLE", 3),
    1: CameraModel(1, "PINHOLE", 4),
    2: CameraModel(2, "SIMPLE_RADIAL", 4),
    3: CameraModel(3, "RADIAL", 5),
    4: CameraModel(4, "OPENCV", 8),
    5: CameraModel(5, "OPENCV_FISHEYE", 8),
}


def read_next_bytes(fid, num_bytes, format_char_sequence, endian="<"):
    data = fid.read(num_bytes)
    return struct.unpack(endian + format_char_sequence, data)


def read_cameras_binary(path):
    cameras = {}
    with open(path, "rb") as fid:
        num_cameras = read_next_bytes(fid, 8, "Q")[0]
        for _ in range(num_cameras):
            cam_props = read_next_bytes(fid, 24, "iiQQ")
            camera_id, model_id = cam_props[0], cam_props[1]
            width, height = cam_props[2], cam_props[3]
            num_params = CAMERA_MODELS[model_id].num_params
            params = np.array(read_next_bytes(fid, 8 * num_params, "d" * num_params))
            cameras[camera_id] = Camera(camera_id, CAMERA_MODELS[model_id].model_name, width, height, params)
    return cameras


def read_images_binary(path):
    images = {}
    with open(path, "rb") as fid:
        num_images = read_next_bytes(fid, 8, "Q")[0]
        for _ in range(num_images):
            props = read_next_bytes(fid, 64, "idddddddi")
            image_id = props[0]
            qvec = np.array(props[1:5])
            tvec = np.array(props[5:8])
            camera_id = props[8]
            name = b""
            ch = fid.read(1)
            while ch != b"\x00":
                name += ch
                ch = fid.read(1)
            name = name.decode("utf-8")
            num_points2D = read_next_bytes(fid, 8, "Q")[0]
            xys = np.zeros((num_points2D, 2))
            point3D_ids = np.zeros(num_points2D, dtype=np.int64)
            for j in range(num_points2D):
                xy_id = read_next_bytes(fid, 24, "ddq")
                xys[j] = np.array(xy_id[:2])
                point3D_ids[j] = xy_id[2]
            images[image_id] = BaseImage(image_id, qvec, tvec, camera_id, name, xys, point3D_ids)
    return images


def read_points3D_binary(path):
    points3D = {}
    with open(path, "rb") as fid:
        num_points = read_next_bytes(fid, 8, "Q")[0]
        for _ in range(num_points):
            props = read_next_bytes(fid, 43, "QdddBBBd")
            point_id = props[0]
            xyz = np.array(props[1:4])
            rgb = np.array(props[4:7])
            error = props[7]
            track_length = read_next_bytes(fid, 8, "Q")[0]
            track_data = read_next_bytes(fid, 8 * track_length, "ii" * track_length)
            image_ids = np.array(track_data[0::2])
            point2D_idxs = np.array(track_data[1::2])
            points3D[point_id] = Point3D(point_id, xyz, rgb, error, image_ids, point2D_idxs)
    return points3D


def qvec2rotmat(qvec):
    w, x, y, z = qvec
    return np.array([
        [1 - 2*y*y - 2*z*z, 2*x*y - 2*w*z,     2*x*z + 2*w*y],
        [2*x*y + 2*w*z,     1 - 2*x*x - 2*z*z, 2*y*z - 2*w*x],
        [2*x*z - 2*w*y,     2*y*z + 2*w*x,     1 - 2*x*x - 2*y*y],
    ])
"""

# ============================================================================
# CELL 4: Dataset class
# ============================================================================

"""
# %%
# --- CELL 4: Dataset loading and camera utilities ---

from PIL import Image as PILImage
from torchvision import transforms


@dataclass
class CameraInfo:
    uid: int
    R: np.ndarray        # 3x3 rotation (world-to-camera)
    T: np.ndarray        # 3x1 translation
    FoVx: float
    FoVy: float
    image: torch.Tensor  # [3, H, W]
    image_name: str
    width: int
    height: int


def focal2fov(focal, pixels):
    return 2.0 * math.atan(pixels / (2.0 * focal))


def load_colmap_dataset(scene_dir, downsample=4):
    \"\"\"Load a COLMAP dataset, returning train/test camera lists and initial points.\"\"\"
    sparse_dir = os.path.join(scene_dir, "sparse", "0")
    cameras = read_cameras_binary(os.path.join(sparse_dir, "cameras.bin"))
    images = read_images_binary(os.path.join(sparse_dir, "images.bin"))
    points3D = read_points3D_binary(os.path.join(sparse_dir, "points3D.bin"))

    # Determine image directory
    if downsample > 1:
        img_dir = os.path.join(scene_dir, f"images_{downsample}")
        if not os.path.exists(img_dir):
            img_dir = os.path.join(scene_dir, "images")
            print(f"Warning: images_{downsample}/ not found, using full-res images")
    else:
        img_dir = os.path.join(scene_dir, "images")

    cam_infos = []
    for img_id in sorted(images.keys()):
        img_data = images[img_id]
        cam = cameras[img_data.camera_id]

        # Rotation and translation
        R = qvec2rotmat(img_data.qvec)
        T = img_data.tvec

        # Intrinsics
        if cam.model == "SIMPLE_PINHOLE":
            fx = fy = cam.params[0]
        elif cam.model == "PINHOLE":
            fx, fy = cam.params[0], cam.params[1]
        elif cam.model in ("SIMPLE_RADIAL", "RADIAL"):
            fx = fy = cam.params[0]
        elif cam.model == "OPENCV":
            fx, fy = cam.params[0], cam.params[1]
        else:
            fx = fy = cam.params[0]

        # Load image
        img_path = os.path.join(img_dir, img_data.name)
        if not os.path.exists(img_path):
            # Try different extensions
            for ext in [".JPG", ".jpg", ".png", ".PNG"]:
                alt = os.path.join(img_dir, Path(img_data.name).stem + ext)
                if os.path.exists(alt):
                    img_path = alt
                    break

        pil_img = PILImage.open(img_path).convert("RGB")
        W_actual, H_actual = pil_img.size

        # Adjust focal length for actual resolution vs COLMAP resolution
        scale_x = W_actual / cam.width
        scale_y = H_actual / cam.height
        fx_scaled = fx * scale_x
        fy_scaled = fy * scale_y

        FoVx = focal2fov(fx_scaled, W_actual)
        FoVy = focal2fov(fy_scaled, H_actual)

        img_tensor = transforms.ToTensor()(pil_img)  # [3, H, W] in [0, 1]

        cam_infos.append(CameraInfo(
            uid=img_id, R=R, T=T, FoVx=FoVx, FoVy=FoVy,
            image=img_tensor, image_name=img_data.name,
            width=W_actual, height=H_actual
        ))

    # Every 8th image for test
    cam_infos_sorted = sorted(cam_infos, key=lambda c: c.image_name)
    train_cams = [c for i, c in enumerate(cam_infos_sorted) if i % 8 != 0]
    test_cams = [c for i, c in enumerate(cam_infos_sorted) if i % 8 == 0]

    # Initial 3D points
    pts_xyz = np.array([p.xyz for p in points3D.values()])
    pts_rgb = np.array([p.rgb for p in points3D.values()]) / 255.0

    print(f"Loaded {len(train_cams)} train / {len(test_cams)} test cameras")
    print(f"Initial SfM points: {len(pts_xyz)}")
    print(f"Image resolution: {cam_infos[0].width}x{cam_infos[0].height}")

    return train_cams, test_cams, pts_xyz, pts_rgb
"""

# ============================================================================
# CELL 5: Scene normalization (for 360 scenes)
# ============================================================================

"""
# %%
# --- CELL 5: Scene normalization ---

def normalize_scene(train_cams, test_cams, pts_xyz):
    \"\"\"Center and scale scene so cameras are in a unit sphere. Standard for 360 scenes.\"\"\"
    # Camera centers
    cam_centers = []
    for cam in train_cams + test_cams:
        R = cam.R
        T = cam.T
        center = -R.T @ T
        cam_centers.append(center)
    cam_centers = np.array(cam_centers)

    # Scene center = centroid of camera centers
    scene_center = cam_centers.mean(axis=0)

    # Scale = max distance from center * 1.1
    dists = np.linalg.norm(cam_centers - scene_center, axis=1)
    scene_scale = dists.max() * 1.1

    # Normalize points
    pts_xyz_norm = (pts_xyz - scene_center) / scene_scale

    # Normalize camera translations
    def normalize_cam(cam):
        T_new = cam.T.copy()
        R = cam.R
        # T_colmap = -R @ center => center = -R^T @ T
        center = -R.T @ T_new
        center_norm = (center - scene_center) / scene_scale
        T_new = -R @ center_norm
        return CameraInfo(
            uid=cam.uid, R=cam.R, T=T_new,
            FoVx=cam.FoVx, FoVy=cam.FoVy,
            image=cam.image, image_name=cam.image_name,
            width=cam.width, height=cam.height
        )

    train_cams_n = [normalize_cam(c) for c in train_cams]
    test_cams_n = [normalize_cam(c) for c in test_cams]

    print(f"Scene center: {scene_center}")
    print(f"Scene scale: {scene_scale:.2f}")
    print(f"Normalized points range: [{pts_xyz_norm.min():.2f}, {pts_xyz_norm.max():.2f}]")

    return train_cams_n, test_cams_n, pts_xyz_norm, scene_center, scene_scale
"""

# ============================================================================
# CELL 6: Gaussian Model (gsplat-based)
# ============================================================================

"""
# %%
# --- CELL 6: 3D Gaussian model using gsplat rasterization ---

import gsplat
from gsplat import rasterization

print(f"gsplat version: {gsplat.__version__}")


class GaussianModel3D:
    \"\"\"3D Gaussian Splatting model using gsplat rasterization.\"\"\"

    def __init__(self, pts_xyz, pts_rgb, device="cuda"):
        self.device = device
        N = len(pts_xyz)
        print(f"Initializing {N} Gaussians from SfM points")

        # Positions [N, 3]
        self.means = nn.Parameter(torch.tensor(pts_xyz, dtype=torch.float32, device=device))

        # Scales [N, 3] -- log scale, init from nearest-neighbor distance
        pts_t = torch.tensor(pts_xyz, dtype=torch.float32, device=device)
        # Sample distances for init (use subset for speed)
        if N > 10000:
            idx = torch.randperm(N, device=device)[:10000]
            dists = torch.cdist(pts_t[idx], pts_t[idx])
            dists[dists == 0] = 1e10
            nn_dist = dists.min(dim=1).values.median().item()
        else:
            dists = torch.cdist(pts_t, pts_t)
            dists[dists == 0] = 1e10
            nn_dist = dists.min(dim=1).values.median().item()

        init_scale = np.log(max(nn_dist * 0.5, 1e-6))
        self.log_scales = nn.Parameter(torch.full((N, 3), init_scale, device=device))

        # Rotations [N, 4] -- quaternion (w, x, y, z), init to identity
        self.quats = nn.Parameter(torch.zeros(N, 4, device=device))
        self.quats.data[:, 0] = 1.0

        # Colors [N, 3] -- sigmoid space
        rgb_t = torch.tensor(pts_rgb, dtype=torch.float32, device=device).clamp(0.01, 0.99)
        self.sh_coeffs = nn.Parameter(torch.logit(rgb_t))  # inverse sigmoid

        # Opacities [N, 1] -- sigmoid space, init to ~0.5
        self.raw_opacities = nn.Parameter(torch.zeros(N, 1, device=device))

        # Densification bookkeeping
        self.grad_accum = torch.zeros(N, device=device)
        self.grad_count = torch.zeros(N, device=device, dtype=torch.int32)
        self.max_radii2D = torch.zeros(N, device=device)

    @property
    def num_gaussians(self):
        return self.means.shape[0]

    def get_params(self):
        return [self.means, self.log_scales, self.quats, self.sh_coeffs, self.raw_opacities]

    @property
    def scales(self):
        return torch.exp(self.log_scales)

    @property
    def opacities(self):
        return torch.sigmoid(self.raw_opacities.squeeze(-1))

    @property
    def colors(self):
        return torch.sigmoid(self.sh_coeffs)

    def render(self, cam, bg_color=None):
        \"\"\"Render from a CameraInfo using gsplat rasterization.\"\"\"
        if bg_color is None:
            bg_color = torch.zeros(3, device=self.device)
        elif not isinstance(bg_color, torch.Tensor):
            bg_color = torch.tensor(bg_color, dtype=torch.float32, device=self.device)

        W, H = cam.width, cam.height
        R = torch.tensor(cam.R, dtype=torch.float32, device=self.device)
        T = torch.tensor(cam.T, dtype=torch.float32, device=self.device)

        # Build view matrix [4, 4] (world-to-camera)
        viewmat = torch.eye(4, device=self.device)
        viewmat[:3, :3] = R
        viewmat[:3, 3] = T

        # Intrinsics from FoV
        fx = W / (2.0 * math.tan(cam.FoVx / 2.0))
        fy = H / (2.0 * math.tan(cam.FoVy / 2.0))
        cx = W / 2.0
        cy = H / 2.0
        K = torch.tensor([[fx, 0, cx], [0, fy, cy], [0, 0, 1]],
                         dtype=torch.float32, device=self.device)

        # Prepare covariance parameters
        quats_n = F.normalize(self.quats, dim=-1)
        scales = self.scales
        opacities = self.opacities

        # gsplat rasterization
        # renders: [C, H, W, 3], alphas: [C, H, W, 1], meta dict
        renders, alphas, meta = rasterization(
            means=self.means,                  # [N, 3]
            quats=quats_n,                     # [N, 4]
            scales=scales,                     # [N, 3]
            opacities=opacities,               # [N]
            colors=self.colors,                # [N, 3]
            viewmats=viewmat.unsqueeze(0),     # [1, 4, 4]
            Ks=K.unsqueeze(0),                 # [1, 3, 3]
            width=W,
            height=H,
            backgrounds=bg_color.unsqueeze(0), # [1, 3]
            packed=False,
            render_mode="RGB",
        )

        # renders shape: [1, H, W, 3] -> [3, H, W]
        image = renders[0].permute(2, 0, 1).clamp(0.0, 1.0)
        return image, alphas, meta

    def accumulate_gradients(self, meta):
        \"\"\"Accumulate position gradients for densification decisions.\"\"\"
        if self.means.grad is not None:
            grad_norms = self.means.grad.detach().norm(dim=-1)
            # Only accumulate for visible Gaussians
            visible = grad_norms > 0
            self.grad_accum[visible] += grad_norms[visible]
            self.grad_count[visible] += 1

    def _concat_new_gaussians(self, new_means, new_scales, new_quats, new_sh, new_opac):
        \"\"\"Helper to append new Gaussians to the model.\"\"\"
        N_new = new_means.shape[0]
        if N_new == 0:
            return

        self.means = nn.Parameter(torch.cat([self.means.data, new_means], dim=0))
        self.log_scales = nn.Parameter(torch.cat([self.log_scales.data, new_scales], dim=0))
        self.quats = nn.Parameter(torch.cat([self.quats.data, new_quats], dim=0))
        self.sh_coeffs = nn.Parameter(torch.cat([self.sh_coeffs.data, new_sh], dim=0))
        self.raw_opacities = nn.Parameter(torch.cat([self.raw_opacities.data, new_opac], dim=0))

        # Extend bookkeeping
        self.grad_accum = torch.cat([self.grad_accum, torch.zeros(N_new, device=self.device)])
        self.grad_count = torch.cat([self.grad_count, torch.zeros(N_new, device=self.device, dtype=torch.int32)])
        self.max_radii2D = torch.cat([self.max_radii2D, torch.zeros(N_new, device=self.device)])

    def prune(self, mask_keep):
        \"\"\"Keep only Gaussians where mask_keep is True.\"\"\"
        self.means = nn.Parameter(self.means.data[mask_keep])
        self.log_scales = nn.Parameter(self.log_scales.data[mask_keep])
        self.quats = nn.Parameter(self.quats.data[mask_keep])
        self.sh_coeffs = nn.Parameter(self.sh_coeffs.data[mask_keep])
        self.raw_opacities = nn.Parameter(self.raw_opacities.data[mask_keep])
        self.grad_accum = self.grad_accum[mask_keep]
        self.grad_count = self.grad_count[mask_keep]
        self.max_radii2D = self.max_radii2D[mask_keep]

    def reset_grad_stats(self):
        N = self.num_gaussians
        self.grad_accum = torch.zeros(N, device=self.device)
        self.grad_count = torch.zeros(N, device=self.device, dtype=torch.int32)
"""

# ============================================================================
# CELL 7: Standard ADC Densification
# ============================================================================

"""
# %%
# --- CELL 7: Standard ADC densification (baseline) ---

def densify_adc(model, grad_threshold=0.0002, scale_threshold=0.01,
                opacity_prune_threshold=0.005, max_screen_size=20.0):
    \"\"\"
    Standard Adaptive Density Control from Kerbl et al. (SIGGRAPH 2023).

    1. Compute average positional gradient per Gaussian
    2. Split Gaussians with large gradients AND large scale
    3. Clone Gaussians with large gradients AND small scale
    4. Prune low-opacity and oversized Gaussians
    \"\"\"
    with torch.no_grad():
        N = model.num_gaussians
        avg_grad = model.grad_accum / (model.grad_count.float() + 1e-7)

        # Identify candidates: gradient above threshold
        grad_mask = avg_grad >= grad_threshold

        # Scale criterion
        scales = model.scales.max(dim=-1).values  # max scale per Gaussian
        big_scale = scales > scale_threshold

        # --- SPLIT: large gradient + large scale ---
        split_mask = grad_mask & big_scale
        n_split = split_mask.sum().item()

        if n_split > 0:
            # For each Gaussian to split, create 2 new ones offset along principal axis
            means = model.means.data[split_mask]
            log_scales = model.log_scales.data[split_mask]
            quats = model.quats.data[split_mask]
            sh = model.sh_coeffs.data[split_mask]
            opac = model.raw_opacities.data[split_mask]

            # Sample offsets along the Gaussian's extent
            stds = model.scales[split_mask]
            offsets = torch.randn(n_split, 3, device=model.device) * stds

            new_means = torch.cat([means + offsets, means - offsets], dim=0)
            # Reduce scale by factor of 1.6 after splitting
            new_scales = torch.cat([log_scales - math.log(1.6)] * 2, dim=0)
            new_quats = torch.cat([quats, quats], dim=0)
            new_sh = torch.cat([sh, sh], dim=0)
            new_opac = torch.cat([opac, opac], dim=0)

            model._concat_new_gaussians(new_means, new_scales, new_quats, new_sh, new_opac)

        # --- CLONE: large gradient + small scale ---
        clone_mask = grad_mask & ~big_scale
        n_clone = clone_mask.sum().item()

        if n_clone > 0:
            new_means = model.means.data[clone_mask].clone()
            new_scales = model.log_scales.data[clone_mask].clone()
            new_quats = model.quats.data[clone_mask].clone()
            new_sh = model.sh_coeffs.data[clone_mask].clone()
            new_opac = model.raw_opacities.data[clone_mask].clone()
            model._concat_new_gaussians(new_means, new_scales, new_quats, new_sh, new_opac)

        # --- PRUNE: low opacity or too big ---
        opacities = model.opacities
        keep = opacities > opacity_prune_threshold
        # Also prune enormous Gaussians
        if max_screen_size > 0:
            keep = keep & (model.max_radii2D <= max_screen_size)
        # Remove the original split Gaussians (they were replaced by 2 new ones)
        if n_split > 0:
            # The first N entries are the originals; split_mask marks which to remove
            orig_keep = ~split_mask
            # Expand keep to cover new Gaussians too
            full_keep = torch.cat([
                keep[:N] & orig_keep,
                torch.ones(model.num_gaussians - N, device=model.device, dtype=torch.bool)
            ])
            # But also apply opacity pruning to new ones
            full_keep[N:] = keep[N:]
            keep = full_keep

        if not keep.all():
            model.prune(keep)

        model.reset_grad_stats()
        return {"split": n_split, "clone": n_clone, "pruned": int((~keep).sum().item()),
                "total": model.num_gaussians}
"""

# ============================================================================
# CELL 8: Farey-Guided Densification
# ============================================================================

"""
# %%
# --- CELL 8: Farey-guided densification ---

def densify_farey(model, grad_threshold=0.0002, scale_threshold=0.01,
                  opacity_prune_threshold=0.005, max_screen_size=20.0,
                  max_insert_ratio=0.05):
    \"\"\"
    Farey-guided densification: mediant insertion based on spatial gaps.

    Instead of the ADC split/clone heuristic, we:
    1. Project Gaussians onto each axis (x, y, z)
    2. Find the largest spatial gaps between consecutive Gaussians
    3. Insert new Gaussians at the mediant (weighted midpoint) of gap endpoints
    4. Gate insertions by reconstruction error (gradient magnitude)
    5. Limit to max_insert_ratio * current_count new Gaussians per step

    Key Farey properties exploited:
    - Mediant insertion: new point = weighted average of neighbors (like Farey mediant)
    - One-per-gap: at most one insertion per spatial gap (bounded refinement)
    - Nested: existing Gaussians are never displaced
    - Error-gated: only insert where reconstruction error is high
    \"\"\"
    with torch.no_grad():
        N = model.num_gaussians
        avg_grad = model.grad_accum / (model.grad_count.float() + 1e-7)
        max_new = max(int(N * max_insert_ratio), 1)

        means = model.means.data  # [N, 3]

        # Collect candidate insertions from all 3 axes
        all_candidates = []  # (gap_score, midpoint, idx_left, idx_right)

        for axis in range(3):
            # Sort by position along this axis
            coords = means[:, axis]
            sorted_idx = torch.argsort(coords)
            sorted_coords = coords[sorted_idx]

            # Compute gaps between consecutive Gaussians
            gaps = sorted_coords[1:] - sorted_coords[:-1]  # [N-1]

            # For each gap, compute the error signal (max gradient of the two endpoints)
            left_idx = sorted_idx[:-1]
            right_idx = sorted_idx[1:]
            gap_grad = torch.max(avg_grad[left_idx], avg_grad[right_idx])

            # Gate: only consider gaps where at least one endpoint has high gradient
            grad_gate = gap_grad >= grad_threshold

            # Score = gap_size * gradient (spatial need * reconstruction need)
            scores = gaps * gap_grad

            # Apply gate
            scores[~grad_gate] = 0.0

            for j in range(len(gaps)):
                if scores[j] > 0:
                    li = left_idx[j].item()
                    ri = right_idx[j].item()
                    all_candidates.append((scores[j].item(), li, ri, axis))

        if not all_candidates:
            # No candidates -- just prune
            opacities = model.opacities
            keep = opacities > opacity_prune_threshold
            if max_screen_size > 0:
                keep = keep & (model.max_radii2D <= max_screen_size)
            if not keep.all():
                model.prune(keep)
            model.reset_grad_stats()
            return {"inserted": 0, "pruned": int((~keep).sum().item()), "total": model.num_gaussians}

        # Sort candidates by score (descending) and take top max_new
        all_candidates.sort(key=lambda x: -x[0])
        selected = all_candidates[:max_new]

        # Deduplicate: don't insert between the same pair twice
        seen_pairs = set()
        unique_selected = []
        for score, li, ri, axis in selected:
            pair = (min(li, ri), max(li, ri))
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                unique_selected.append((score, li, ri, axis))
        selected = unique_selected[:max_new]

        n_insert = len(selected)
        if n_insert > 0:
            new_means_list = []
            new_scales_list = []
            new_quats_list = []
            new_sh_list = []
            new_opac_list = []

            for score, li, ri, axis in selected:
                pos_l = model.means.data[li]
                pos_r = model.means.data[ri]
                scale_l = model.log_scales.data[li]
                scale_r = model.log_scales.data[ri]

                # Mediant position: weighted by inverse scale (smaller Gaussians
                # pull the midpoint toward them, like Farey mediants weight by denominator)
                s_l = model.scales[li].mean()
                s_r = model.scales[ri].mean()
                # Weight: smaller scale = higher weight (finer detail needed there)
                w_l = 1.0 / (s_l + 1e-8)
                w_r = 1.0 / (s_r + 1e-8)
                w_total = w_l + w_r
                alpha = (w_l / w_total).item()

                new_pos = alpha * pos_l + (1 - alpha) * pos_r
                new_scale = 0.5 * (scale_l + scale_r)  # average log-scale
                # Slightly reduce scale for the new insertion (tighter fit)
                new_scale = new_scale - 0.3

                new_means_list.append(new_pos.unsqueeze(0))
                new_scales_list.append(new_scale.unsqueeze(0))
                new_quats_list.append(model.quats.data[li].unsqueeze(0))  # inherit rotation
                new_sh_list.append(0.5 * (model.sh_coeffs.data[li] + model.sh_coeffs.data[ri]).unsqueeze(0))
                new_opac_list.append(model.raw_opacities.data[li].unsqueeze(0))

            new_means = torch.cat(new_means_list, dim=0)
            new_scales = torch.cat(new_scales_list, dim=0)
            new_quats = torch.cat(new_quats_list, dim=0)
            new_sh = torch.cat(new_sh_list, dim=0)
            new_opac = torch.cat(new_opac_list, dim=0)

            model._concat_new_gaussians(new_means, new_scales, new_quats, new_sh, new_opac)

        # --- PRUNE: same as ADC ---
        opacities = model.opacities
        keep = opacities > opacity_prune_threshold
        if max_screen_size > 0:
            keep = keep & (model.max_radii2D <= max_screen_size)
        if not keep.all():
            model.prune(keep)

        model.reset_grad_stats()
        return {"inserted": n_insert, "pruned": int((~keep).sum().item()),
                "total": model.num_gaussians}
"""

# ============================================================================
# CELL 9: Training loop
# ============================================================================

"""
# %%
# --- CELL 9: Training loop ---

import lpips as lpips_module
from skimage.metrics import structural_similarity as ssim_fn


def compute_metrics(rendered, gt, lpips_net=None):
    \"\"\"Compute PSNR, SSIM, LPIPS between rendered and ground truth [3, H, W] tensors.\"\"\"
    mse = ((rendered - gt) ** 2).mean().item()
    psnr = -10.0 * math.log10(max(mse, 1e-10))

    # SSIM
    r_np = rendered.detach().cpu().permute(1, 2, 0).numpy()
    g_np = gt.detach().cpu().permute(1, 2, 0).numpy()
    ssim_val = ssim_fn(r_np, g_np, channel_axis=2, data_range=1.0)

    # LPIPS
    lpips_val = 0.0
    if lpips_net is not None:
        with torch.no_grad():
            # LPIPS expects [-1, 1] range, [B, 3, H, W]
            r_lpips = (rendered.unsqueeze(0) * 2 - 1).cuda()
            g_lpips = (gt.unsqueeze(0) * 2 - 1).cuda()
            lpips_val = lpips_net(r_lpips, g_lpips).item()

    return {"psnr": psnr, "ssim": ssim_val, "lpips": lpips_val}


def evaluate_test(model, test_cams, lpips_net):
    \"\"\"Evaluate on all test cameras, return average metrics.\"\"\"
    psnrs, ssims, lpipss = [], [], []
    for cam in test_cams:
        gt = cam.image.to(model.device)
        rendered, _, _ = model.render(cam)
        m = compute_metrics(rendered, gt, lpips_net)
        psnrs.append(m["psnr"])
        ssims.append(m["ssim"])
        lpipss.append(m["lpips"])
    return {
        "psnr": np.mean(psnrs),
        "ssim": np.mean(ssims),
        "lpips": np.mean(lpipss),
    }


def train_one_run(train_cams, test_cams, pts_xyz, pts_rgb,
                  densify_fn, method_name, seed,
                  total_iters=30000,
                  densify_start=500,
                  densify_stop=15000,
                  densify_interval=100,
                  eval_interval=1000,
                  lr_means=0.00016,
                  lr_scales=0.005,
                  lr_quats=0.001,
                  lr_sh=0.0025,
                  lr_opac=0.05):
    \"\"\"
    Train a 3DGS model with a given densification function.
    Returns: final metrics dict + training log.
    \"\"\"
    torch.manual_seed(seed)
    np.random.seed(seed)

    print(f"\\n{'='*70}")
    print(f"Training: {method_name} | Seed: {seed} | Iters: {total_iters}")
    print(f"{'='*70}")

    # Initialize model
    model = GaussianModel3D(pts_xyz, pts_rgb, device="cuda")
    n_init = model.num_gaussians

    # LPIPS network (shared across evals)
    lpips_net = lpips_module.LPIPS(net="vgg").cuda()

    # Optimizer
    def make_optimizer():
        return torch.optim.Adam([
            {"params": [model.means], "lr": lr_means, "name": "means"},
            {"params": [model.log_scales], "lr": lr_scales, "name": "scales"},
            {"params": [model.quats], "lr": lr_quats, "name": "quats"},
            {"params": [model.sh_coeffs], "lr": lr_sh, "name": "sh"},
            {"params": [model.raw_opacities], "lr": lr_opac, "name": "opac"},
        ])

    optimizer = make_optimizer()

    # Learning rate schedule: exponential decay for means
    lr_means_final = lr_means * 0.01
    lr_lambda = lambda step: max(0.01, math.exp(
        step / total_iters * math.log(lr_means_final / lr_means)
    )) if step > 0 else 1.0

    # Training log
    log = {"step": [], "train_psnr": [], "test_psnr": [], "test_ssim": [],
           "test_lpips": [], "n_gaussians": [], "time": []}

    # White background for 360 scenes
    bg_color = torch.ones(3, device="cuda")

    t_start = time.time()
    n_train = len(train_cams)

    for step in range(1, total_iters + 1):
        # Random training view
        cam = train_cams[step % n_train]
        gt = cam.image.to("cuda")

        # Render
        rendered, alphas, meta = model.render(cam, bg_color=bg_color)

        # Loss: L1 + 0.2 * SSIM
        l1_loss = F.l1_loss(rendered, gt)
        # Simple differentiable SSIM approximation via windowed means
        ssim_loss = 1.0 - _differentiable_ssim(rendered, gt)
        loss = 0.8 * l1_loss + 0.2 * ssim_loss

        # Backward
        optimizer.zero_grad()
        loss.backward()

        # Accumulate gradients for densification
        model.accumulate_gradients(meta)

        # Step optimizer
        optimizer.step()

        # Update learning rate
        for pg in optimizer.param_groups:
            if pg["name"] == "means":
                pg["lr"] = lr_means * lr_lambda(step)

        # Densification
        if densify_start <= step <= densify_stop and step % densify_interval == 0:
            result = densify_fn(model)
            # Rebuild optimizer with new parameters
            optimizer = make_optimizer()
            if step % 1000 == 0:
                print(f"  Step {step}: densify -> {result}")

        # Opacity reset (every 3000 steps during densification)
        if step % 3000 == 0 and step <= densify_stop:
            with torch.no_grad():
                model.raw_opacities.data.fill_(-2.0)  # reset to ~sigmoid(-2)=0.12
            optimizer = make_optimizer()

        # Logging
        if step % eval_interval == 0 or step == 1:
            elapsed = time.time() - t_start
            train_psnr = -10 * math.log10(max(F.mse_loss(rendered, gt).item(), 1e-10))
            test_metrics = evaluate_test(model, test_cams, lpips_net)

            log["step"].append(step)
            log["train_psnr"].append(train_psnr)
            log["test_psnr"].append(test_metrics["psnr"])
            log["test_ssim"].append(test_metrics["ssim"])
            log["test_lpips"].append(test_metrics["lpips"])
            log["n_gaussians"].append(model.num_gaussians)
            log["time"].append(elapsed)

            print(f"  [{method_name}] Step {step:>6d} | "
                  f"Train PSNR: {train_psnr:.2f} | "
                  f"Test PSNR: {test_metrics['psnr']:.2f} | "
                  f"SSIM: {test_metrics['ssim']:.4f} | "
                  f"LPIPS: {test_metrics['lpips']:.4f} | "
                  f"#G: {model.num_gaussians:,} | "
                  f"Time: {elapsed:.0f}s")

    # Final evaluation
    elapsed = time.time() - t_start
    final_metrics = evaluate_test(model, test_cams, lpips_net)
    final_metrics["n_gaussians"] = model.num_gaussians
    final_metrics["training_time_s"] = elapsed
    final_metrics["method"] = method_name
    final_metrics["seed"] = seed
    final_metrics["n_init"] = n_init

    print(f"\\n  FINAL [{method_name}, seed={seed}]: "
          f"PSNR={final_metrics['psnr']:.2f} | "
          f"SSIM={final_metrics['ssim']:.4f} | "
          f"LPIPS={final_metrics['lpips']:.4f} | "
          f"#G={model.num_gaussians:,} | "
          f"Time={elapsed:.0f}s")

    del lpips_net
    torch.cuda.empty_cache()

    return final_metrics, log


def _differentiable_ssim(img1, img2, window_size=11):
    \"\"\"Simple differentiable SSIM for training loss (not used for eval).\"\"\"
    C1 = 0.01 ** 2
    C2 = 0.03 ** 2
    # img1, img2: [3, H, W]
    pad = window_size // 2
    mu1 = F.avg_pool2d(img1.unsqueeze(0), window_size, stride=1, padding=pad)
    mu2 = F.avg_pool2d(img2.unsqueeze(0), window_size, stride=1, padding=pad)
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu12 = mu1 * mu2
    sigma1_sq = F.avg_pool2d((img1 ** 2).unsqueeze(0), window_size, stride=1, padding=pad) - mu1_sq
    sigma2_sq = F.avg_pool2d((img2 ** 2).unsqueeze(0), window_size, stride=1, padding=pad) - mu2_sq
    sigma12 = F.avg_pool2d((img1 * img2).unsqueeze(0), window_size, stride=1, padding=pad) - mu12
    ssim_map = ((2 * mu12 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()
"""

# ============================================================================
# CELL 10: Main experiment runner
# ============================================================================

"""
# %%
# --- CELL 10: Run the full experiment ---

SEEDS = [42, 123, 7]
TOTAL_ITERS = 30000

# Load dataset
train_cams, test_cams, pts_xyz, pts_rgb = load_colmap_dataset(SCENE_DIR, downsample=4)
train_cams, test_cams, pts_xyz, _, _ = normalize_scene(train_cams, test_cams, pts_xyz)

all_results = []
all_logs = {}

for seed in SEEDS:
    # --- Standard ADC ---
    metrics_adc, log_adc = train_one_run(
        train_cams, test_cams, pts_xyz, pts_rgb,
        densify_fn=densify_adc,
        method_name="ADC",
        seed=seed,
        total_iters=TOTAL_ITERS,
    )
    all_results.append(metrics_adc)
    all_logs[f"ADC_seed{seed}"] = log_adc

    # --- Farey-guided ---
    metrics_farey, log_farey = train_one_run(
        train_cams, test_cams, pts_xyz, pts_rgb,
        densify_fn=densify_farey,
        method_name="Farey",
        seed=seed,
        total_iters=TOTAL_ITERS,
    )
    all_results.append(metrics_farey)
    all_logs[f"Farey_seed{seed}"] = log_farey

    # Clear GPU memory between runs
    torch.cuda.empty_cache()

print("\\n\\nAll runs complete!")
"""

# ============================================================================
# CELL 11: Results table and analysis
# ============================================================================

"""
# %%
# --- CELL 11: Results summary ---

import pandas as pd

df = pd.DataFrame(all_results)
print("\\n" + "="*80)
print("INDIVIDUAL RUN RESULTS")
print("="*80)
print(df.to_string(index=False))

# Aggregate by method
print("\\n" + "="*80)
print("AGGREGATE RESULTS (mean +/- std across seeds)")
print("="*80)

for method in ["ADC", "Farey"]:
    sub = df[df["method"] == method]
    print(f"\\n--- {method} ---")
    for col in ["psnr", "ssim", "lpips", "n_gaussians", "training_time_s"]:
        mean = sub[col].mean()
        std = sub[col].std()
        print(f"  {col:>18s}: {mean:.4f} +/- {std:.4f}")

# Statistical comparison
print("\\n" + "="*80)
print("COMPARISON: Farey vs ADC")
print("="*80)

adc_psnr = df[df["method"] == "ADC"]["psnr"].values
farey_psnr = df[df["method"] == "Farey"]["psnr"].values
delta_psnr = farey_psnr - adc_psnr

adc_ssim = df[df["method"] == "ADC"]["ssim"].values
farey_ssim = df[df["method"] == "Farey"]["ssim"].values
delta_ssim = farey_ssim - adc_ssim

adc_lpips = df[df["method"] == "ADC"]["lpips"].values
farey_lpips = df[df["method"] == "Farey"]["lpips"].values
delta_lpips = farey_lpips - adc_lpips

adc_count = df[df["method"] == "ADC"]["n_gaussians"].values
farey_count = df[df["method"] == "Farey"]["n_gaussians"].values

print(f"  Delta PSNR  (Farey - ADC): {delta_psnr.mean():+.3f} dB  (per-seed: {delta_psnr})")
print(f"  Delta SSIM  (Farey - ADC): {delta_ssim.mean():+.5f}   (per-seed: {delta_ssim})")
print(f"  Delta LPIPS (Farey - ADC): {delta_lpips.mean():+.5f}   (per-seed: {delta_lpips})")
print(f"  ADC   Gaussian count: {adc_count.mean():.0f} +/- {adc_count.std():.0f}")
print(f"  Farey Gaussian count: {farey_count.mean():.0f} +/- {farey_count.std():.0f}")
print(f"  Count ratio (Farey/ADC): {farey_count.mean()/adc_count.mean():.3f}")

# Verdict
winner_psnr = "Farey" if delta_psnr.mean() > 0 else "ADC"
winner_ssim = "Farey" if delta_ssim.mean() > 0 else "ADC"
winner_lpips = "Farey" if delta_lpips.mean() < 0 else "ADC"  # lower is better
more_compact = "Farey" if farey_count.mean() < adc_count.mean() else "ADC"

print(f"\\n  PSNR winner:  {winner_psnr}")
print(f"  SSIM winner:  {winner_ssim}")
print(f"  LPIPS winner: {winner_lpips}")
print(f"  More compact: {more_compact}")

# Save results
results_path = "/content/3dgs_farey_vs_adc_results.json"
with open(results_path, "w") as f:
    json.dump({
        "individual": all_results,
        "config": {
            "scene": "bicycle",
            "dataset": "Mip-NeRF 360",
            "downsample": 4,
            "total_iters": TOTAL_ITERS,
            "seeds": SEEDS,
            "densify_start": 500,
            "densify_stop": 15000,
            "densify_interval": 100,
        }
    }, f, indent=2, default=str)
print(f"\\nResults saved to {results_path}")
"""

# ============================================================================
# CELL 12: Visualization
# ============================================================================

"""
# %%
# --- CELL 12: Training curves plot ---

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# PSNR over training
ax = axes[0, 0]
for key, log in all_logs.items():
    style = "-" if "ADC" in key else "--"
    color = "blue" if "ADC" in key else "red"
    ax.plot(log["step"], log["test_psnr"], style, color=color, alpha=0.5, label=key)
ax.set_xlabel("Iteration")
ax.set_ylabel("Test PSNR (dB)")
ax.set_title("Test PSNR over Training")
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# SSIM over training
ax = axes[0, 1]
for key, log in all_logs.items():
    style = "-" if "ADC" in key else "--"
    color = "blue" if "ADC" in key else "red"
    ax.plot(log["step"], log["test_ssim"], style, color=color, alpha=0.5, label=key)
ax.set_xlabel("Iteration")
ax.set_ylabel("Test SSIM")
ax.set_title("Test SSIM over Training")
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Gaussian count over training
ax = axes[1, 0]
for key, log in all_logs.items():
    style = "-" if "ADC" in key else "--"
    color = "blue" if "ADC" in key else "red"
    ax.plot(log["step"], log["n_gaussians"], style, color=color, alpha=0.5, label=key)
ax.set_xlabel("Iteration")
ax.set_ylabel("Number of Gaussians")
ax.set_title("Gaussian Count over Training")
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Final bar chart
ax = axes[1, 1]
methods = ["ADC", "Farey"]
psnr_means = [df[df["method"] == m]["psnr"].mean() for m in methods]
psnr_stds = [df[df["method"] == m]["psnr"].std() for m in methods]
bars = ax.bar(methods, psnr_means, yerr=psnr_stds, capsize=8,
              color=["steelblue", "indianred"], alpha=0.8)
ax.set_ylabel("Test PSNR (dB)")
ax.set_title("Final PSNR Comparison (mean +/- std)")
ax.grid(True, alpha=0.3, axis="y")
# Add value labels
for bar, mean, std in zip(bars, psnr_means, psnr_stds):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std + 0.1,
            f"{mean:.2f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

plt.suptitle("Farey vs ADC Densification on Bicycle (Mip-NeRF 360)\\n"
             f"30K iters, 3 seeds, images_4 resolution", fontsize=13)
plt.tight_layout()
plt.savefig("/content/farey_vs_adc_curves.png", dpi=150, bbox_inches="tight")
plt.show()
print("Plot saved to /content/farey_vs_adc_curves.png")
"""

# ============================================================================
# CELL 13: Render sample test views
# ============================================================================

"""
# %%
# --- CELL 13: Visual comparison of rendered test views ---

# Retrain the best seed for visual comparison
best_seed = SEEDS[0]

# Quick retrain ADC
model_adc = GaussianModel3D(pts_xyz, pts_rgb, device="cuda")
# (In practice, we'd save/load checkpoints. For the notebook, just use the
# last-trained models. If you want visuals, re-run cell 10 with just 1 seed.)

# For now, render from the last trained models by re-running a short version
# This cell is optional -- the metrics in Cell 11 are the primary output.

print("To see visual comparisons, reduce to 1 seed in Cell 10 and keep model references.")
print("The quantitative results in Cell 11 are the primary output of this experiment.")
"""

# ============================================================================
# CELL 14: Download results
# ============================================================================

"""
# %%
# --- CELL 14: Download results ---
from google.colab import files

# Download the JSON results
files.download("/content/3dgs_farey_vs_adc_results.json")

# Download the plot
files.download("/content/farey_vs_adc_curves.png")

print("Downloads initiated. Check your browser downloads folder.")
"""


# ============================================================================
# If running as a standalone script (not in Colab), execute everything
# ============================================================================

if __name__ == "__main__":
    print("This script is designed for Google Colab (T4 GPU).")
    print("Copy each CELL block into a separate Colab cell and run sequentially.")
    print("")
    print("Estimated runtime on T4 GPU:")
    print("  - Dataset download: ~2 min")
    print("  - Per training run (30K iters): ~30-45 min")
    print("  - Total (2 methods x 3 seeds = 6 runs): ~3-5 hours")
    print("")
    print("To reduce runtime for a quick test:")
    print("  - Set TOTAL_ITERS = 7000 in Cell 10")
    print("  - Set SEEDS = [42] in Cell 10")
    print("  - This gives ~15-20 min total")
