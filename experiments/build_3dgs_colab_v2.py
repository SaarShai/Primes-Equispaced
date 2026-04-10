#!/usr/bin/env python3
"""Build 3dgs_colab_v2.ipynb as valid JSON with compile-checked cells."""
import json, sys, os

def make_md_cell(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(True)}

def make_code_cell(source):
    # Validate syntax
    try:
        compile(source, "<cell>", "exec")
    except SyntaxError as e:
        print(f"SYNTAX ERROR in cell:\n{source[:120]}...\n{e}", file=sys.stderr)
        sys.exit(1)
    lines = source.splitlines(True)
    # Ensure last line has no trailing newline for cleanliness
    if lines and lines[-1].endswith('\n'):
        lines[-1] = lines[-1].rstrip('\n')
    return {
        "cell_type": "code",
        "metadata": {},
        "source": lines,
        "execution_count": None,
        "outputs": []
    }

def make_raw_cell(source):
    """For cells with shell commands that can't be compile()-checked."""
    lines = source.splitlines(True)
    if lines and lines[-1].endswith('\n'):
        lines[-1] = lines[-1].rstrip('\n')
    return {
        "cell_type": "code",
        "metadata": {},
        "source": lines,
        "execution_count": None,
        "outputs": []
    }

cells = []

# ── Cell 1: Title ──
cells.append(make_md_cell("""\
# Farey-Guided 3D Gaussian Splatting — Colab Benchmark v2

**What this does:** Compares standard ADC densification (Kerbl et al. 2023) against
Farey-mediant-guided densification on the MipNeRF-360 Bicycle scene.

**Instructions:**
1. Use a **GPU runtime** (Runtime → Change runtime type → T4 GPU)
2. Run cells in order
3. Quick run (~20 min on T4): default settings
4. Full run (~2 hrs): set `TOTAL_ITERS=30000`, `SEEDS=[42,123,7]`

**Requirements:** gsplat, PyTorch with CUDA, ~8GB GPU RAM
"""))

# ── Cell 2: Install ──
cells.append(make_raw_cell("""\
!pip install -q gsplat torch torchvision lpips scikit-image

import torch
print(f"CUDA: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Device: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB")
else:
    print("WARNING: No GPU detected. This notebook requires CUDA.")
"""))

# ── Cell 3: Download bicycle scene ──
cells.append(make_raw_cell("""\
import os, subprocess

os.makedirs('/content/data', exist_ok=True)

if not os.path.exists('/content/data/bicycle'):
    print("Downloading bicycle scene (~1.4 GB)...")
    subprocess.run(['wget', '-q', '--show-progress',
                    'http://storage.googleapis.com/gresearch/refraw360/bicycle.zip',
                    '-O', '/content/data/bicycle.zip'], check=True)
    subprocess.run(['unzip', '-q', '/content/data/bicycle.zip',
                    '-d', '/content/data/'], check=True)
    os.remove('/content/data/bicycle.zip')
    print("Done.")
else:
    print("Bicycle scene already downloaded.")

img_dir = '/content/data/bicycle/images'
if os.path.isdir(img_dir):
    print(f"Images: {len(os.listdir(img_dir))}")
"""))

# ── Cell 4: Configuration ──
cells.append(make_code_cell("""\
# ── Experiment Configuration ──
TOTAL_ITERS = 7000       # Quick: 7000, Full: 30000
SEEDS = [42]             # Quick: [42], Full: [42, 123, 7]
DENSIFY_START = 500
DENSIFY_STOP = 15000
DENSIFY_INTERVAL = 100
GRAD_THRESHOLD = 0.0002
IMAGE_SCALE = 8          # Use images_8 (downscaled 8x)
LR_POSITION = 1.6e-4
LR_FEATURE = 2.5e-3
LR_OPACITY = 5e-2
LR_SCALE = 5e-3
LR_ROTATION = 1e-3
OPACITY_RESET_INTERVAL = 3000
OPACITY_PRUNE_THRESHOLD = 0.005
SCENE_DIR = '/content/data/bicycle'
"""))

# ── Cell 5: COLMAP binary reader ──
cells.append(make_code_cell("""\
import struct
import numpy as np
from collections import namedtuple

CameraModel = namedtuple('CameraModel', ['model_id', 'model_name', 'num_params'])

CAMERA_MODELS = {
    0: CameraModel(0, 'SIMPLE_PINHOLE', 3),
    1: CameraModel(1, 'PINHOLE', 4),
    2: CameraModel(2, 'SIMPLE_RADIAL', 4),
    3: CameraModel(3, 'RADIAL', 5),
    4: CameraModel(4, 'OPENCV', 8),
    5: CameraModel(5, 'OPENCV_FISHEYE', 8),
    6: CameraModel(6, 'FULL_OPENCV', 12),
    7: CameraModel(7, 'FOV', 5),
    8: CameraModel(8, 'SIMPLE_RADIAL_FISHEYE', 4),
    9: CameraModel(9, 'RADIAL_FISHEYE', 5),
    10: CameraModel(10, 'THIN_PRISM_FISHEYE', 12),
}

Camera = namedtuple('Camera', ['id', 'model', 'width', 'height', 'params'])
Image = namedtuple('Image', ['id', 'qvec', 'tvec', 'camera_id', 'name', 'xys', 'point3D_ids'])
Point3D = namedtuple('Point3D', ['id', 'xyz', 'rgb', 'error', 'image_ids', 'point2D_idxs'])


def read_cameras_binary(path):
    cameras = {}
    with open(path, 'rb') as f:
        num_cameras = struct.unpack('<Q', f.read(8))[0]
        for _ in range(num_cameras):
            cam_id = struct.unpack('<I', f.read(4))[0]
            model_id = struct.unpack('<i', f.read(4))[0]
            width = struct.unpack('<Q', f.read(8))[0]
            height = struct.unpack('<Q', f.read(8))[0]
            num_params = CAMERA_MODELS[model_id].num_params
            params = np.array(struct.unpack(f'<{num_params}d', f.read(8 * num_params)))
            cameras[cam_id] = Camera(cam_id, model_id, width, height, params)
    return cameras


def read_images_binary(path):
    images = {}
    with open(path, 'rb') as f:
        num_images = struct.unpack('<Q', f.read(8))[0]
        for _ in range(num_images):
            img_id = struct.unpack('<I', f.read(4))[0]
            qvec = np.array(struct.unpack('<4d', f.read(32)))
            tvec = np.array(struct.unpack('<3d', f.read(24)))
            camera_id = struct.unpack('<I', f.read(4))[0]
            name = b''
            while True:
                ch = f.read(1)
                if ch == b'\\x00':
                    break
                name += ch
            name = name.decode('utf-8')
            num_points2D = struct.unpack('<Q', f.read(8))[0]
            xys = np.zeros((num_points2D, 2))
            point3D_ids = np.zeros(num_points2D, dtype=np.int64)
            for j in range(num_points2D):
                xys[j] = struct.unpack('<2d', f.read(16))
                point3D_ids[j] = struct.unpack('<q', f.read(8))[0]
            images[img_id] = Image(img_id, qvec, tvec, camera_id, name, xys, point3D_ids)
    return images


def read_points3D_binary(path):
    points = {}
    with open(path, 'rb') as f:
        num_points = struct.unpack('<Q', f.read(8))[0]
        for _ in range(num_points):
            pt_id = struct.unpack('<Q', f.read(8))[0]
            xyz = np.array(struct.unpack('<3d', f.read(24)))
            rgb = np.array(struct.unpack('<3B', f.read(3)))
            error = struct.unpack('<d', f.read(8))[0]
            track_len = struct.unpack('<Q', f.read(8))[0]
            image_ids = np.zeros(track_len, dtype=np.int32)
            point2D_idxs = np.zeros(track_len, dtype=np.int32)
            for j in range(track_len):
                image_ids[j] = struct.unpack('<I', f.read(4))[0]
                point2D_idxs[j] = struct.unpack('<I', f.read(4))[0]
            points[pt_id] = Point3D(pt_id, xyz, rgb, error, image_ids, point2D_idxs)
    return points


print("COLMAP binary reader defined.")
"""))

# ── Cell 6: Load scene ──
cells.append(make_code_cell("""\
import os, glob
import numpy as np
from PIL import Image as PILImage
import torch

def qvec2rotmat(qvec):
    w, x, y, z = qvec
    return np.array([
        [1 - 2*y*y - 2*z*z, 2*x*y - 2*w*z, 2*x*z + 2*w*y],
        [2*x*y + 2*w*z, 1 - 2*x*x - 2*z*z, 2*y*z - 2*w*x],
        [2*x*z - 2*w*y, 2*y*z + 2*w*x, 1 - 2*x*x - 2*y*y]
    ])

def load_scene(scene_dir, image_scale=8):
    sparse_dir = os.path.join(scene_dir, 'sparse', '0')
    cameras = read_cameras_binary(os.path.join(sparse_dir, 'cameras.bin'))
    images = read_images_binary(os.path.join(sparse_dir, 'images.bin'))
    points3D = read_points3D_binary(os.path.join(sparse_dir, 'points3D.bin'))

    img_subdir = f'images_{image_scale}' if image_scale > 1 else 'images'
    img_dir = os.path.join(scene_dir, img_subdir)
    if not os.path.isdir(img_dir):
        img_dir = os.path.join(scene_dir, 'images')
        print(f"Warning: {img_subdir} not found, using full-res images")

    # Sort images by name for reproducible train/test split
    sorted_imgs = sorted(images.values(), key=lambda x: x.name)

    scene_data = []
    for idx, img in enumerate(sorted_imgs):
        cam = cameras[img.camera_id]
        img_path = os.path.join(img_dir, img.name)
        if not os.path.exists(img_path):
            continue

        pil_img = PILImage.open(img_path)
        gt = torch.from_numpy(np.array(pil_img)).float() / 255.0  # (H, W, 3)
        H, W = gt.shape[:2]

        R = qvec2rotmat(img.qvec)
        T = img.tvec

        # Build intrinsics from camera model
        if cam.model in (0,):  # SIMPLE_PINHOLE
            fx = fy = cam.params[0] * (W / cam.width)
            cx, cy = cam.params[1] * (W / cam.width), cam.params[2] * (H / cam.height)
        elif cam.model in (1,):  # PINHOLE
            fx = cam.params[0] * (W / cam.width)
            fy = cam.params[1] * (H / cam.height)
            cx = cam.params[2] * (W / cam.width)
            cy = cam.params[3] * (H / cam.height)
        else:  # OPENCV and others: first 4 params are fx, fy, cx, cy
            fx = cam.params[0] * (W / cam.width)
            fy = cam.params[1] * (H / cam.height)
            cx = cam.params[2] * (W / cam.width)
            cy = cam.params[3] * (H / cam.height)

        K = torch.tensor([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=torch.float32)

        # World-to-camera: [R | T]
        viewmat = torch.eye(4, dtype=torch.float32)
        viewmat[:3, :3] = torch.from_numpy(R).float()
        viewmat[:3, 3] = torch.from_numpy(T).float()

        scene_data.append({
            'name': img.name,
            'gt': gt,        # (H, W, 3)
            'K': K,           # (3, 3)
            'viewmat': viewmat,  # (4, 4)
            'H': H, 'W': W,
        })

    # Train/test split: every 8th image is test
    train = [d for i, d in enumerate(scene_data) if i % 8 != 0]
    test = [d for i, d in enumerate(scene_data) if i % 8 == 0]

    # Initial point cloud
    pts = np.array([p.xyz for p in points3D.values()])
    cols = np.array([p.rgb for p in points3D.values()]) / 255.0

    print(f"Scene loaded: {len(scene_data)} images ({len(train)} train, {len(test)} test)")
    print(f"Initial points: {len(pts)}, Image size: {scene_data[0]['H']}x{scene_data[0]['W']}")

    return train, test, pts, cols


train_data, test_data, init_pts, init_cols = load_scene(SCENE_DIR, IMAGE_SCALE)
"""))

# ── Cell 7: Gaussian model + renderer ──
cells.append(make_code_cell("""\
import torch
import torch.nn as nn
import math
from gsplat import rasterization

class GaussianModel(nn.Module):
    def __init__(self, points, colors, device='cuda'):
        super().__init__()
        N = len(points)
        self.device = device

        # Positions
        self.means = nn.Parameter(torch.from_numpy(points).float().to(device))

        # Log-scales (initialize to reasonable size based on point cloud)
        avg_dist = self._compute_avg_dist(points)
        init_scale = math.log(avg_dist * 0.5)
        self.log_scales = nn.Parameter(torch.full((N, 3), init_scale, device=device))

        # Rotations as quaternions (w, x, y, z), initialized to identity
        quats = torch.zeros(N, 4, device=device)
        quats[:, 0] = 1.0
        self.quats = nn.Parameter(quats)

        # Opacities (logit space)
        self.logit_opacities = nn.Parameter(torch.logit(torch.full((N,), 0.1, device=device)))

        # Spherical harmonics (degree 0 only for speed)
        # SH degree 0: single coefficient per channel, color = c0 * 0.28209
        sh0 = torch.from_numpy(colors).float().to(device)
        sh0 = (sh0 - 0.5) / 0.28209  # Inverse of SH basis
        self.sh_coeffs = nn.Parameter(sh0.unsqueeze(1))  # (N, 1, 3)

        # Accumulated gradients for densification
        self.grad_accum = torch.zeros(N, device=device)
        self.grad_count = torch.zeros(N, device=device)

    def _compute_avg_dist(self, points):
        from scipy.spatial import KDTree
        # Use subset for speed
        subset = points[::max(1, len(points) // 5000)]
        tree = KDTree(subset)
        dists, _ = tree.query(subset, k=4)
        return float(np.mean(dists[:, 1:]))

    @property
    def scales(self):
        return torch.exp(self.log_scales)

    @property
    def opacities(self):
        return torch.sigmoid(self.logit_opacities)

    @property
    def num_gaussians(self):
        return self.means.shape[0]

    def get_colors(self):
        return torch.clamp(self.sh_coeffs[:, 0, :] * 0.28209 + 0.5, 0.0, 1.0)

    def render(self, viewmat, K, H, W):
        viewmat_4x4 = viewmat.unsqueeze(0).to(self.device)  # (1, 4, 4)
        K_3x3 = K.unsqueeze(0).to(self.device)  # (1, 3, 3)

        renders, alphas, meta = rasterization(
            means=self.means,
            quats=self.quats / (self.quats.norm(dim=-1, keepdim=True) + 1e-8),
            scales=self.scales,
            opacities=self.opacities,
            colors=self.sh_coeffs,
            viewmats=viewmat_4x4,
            Ks=K_3x3,
            width=W,
            height=H,
            sh_degree=0,
            near_plane=0.01,
            far_plane=100.0,
        )
        # renders: (1, H, W, 3), alphas: (1, H, W, 1)
        image = renders.squeeze(0)  # (H, W, 3)
        return image, alphas.squeeze(0), meta

    def accumulate_gradients(self, meta):
        if self.means.grad is not None:
            visible = meta.get('gaussian_ids', None)
            if visible is not None:
                grad_norms = self.means.grad.norm(dim=-1)
                # Scatter-add for visible Gaussians
                self.grad_accum.scatter_add_(0, visible.long(),
                    grad_norms[visible.long()] if visible.max() < len(grad_norms) else
                    torch.zeros(visible.shape[0], device=self.device))
                self.grad_count.scatter_add_(0, visible.long(),
                    torch.ones(visible.shape[0], device=self.device))
            else:
                self.grad_accum += self.means.grad.norm(dim=-1)
                self.grad_count += 1

    def reset_grad_stats(self):
        self.grad_accum.zero_()
        self.grad_count.zero_()


print(f"GaussianModel defined. gsplat rasterization imported.")
"""))

# ── Cell 8: Standard ADC densification ──
cells.append(make_code_cell("""\
import torch
import torch.nn as nn
import numpy as np

def densify_adc(model, grad_threshold=GRAD_THRESHOLD, extent=None):
    \"\"\"Standard Adaptive Density Control (Kerbl et al. 2023).

    1. Compute average positional gradient per Gaussian
    2. Split Gaussians that are too large AND have high gradient
    3. Clone Gaussians that are small AND have high gradient
    4. Prune near-transparent Gaussians
    \"\"\"
    with torch.no_grad():
        avg_grad = model.grad_accum / (model.grad_count + 1e-8)
        high_grad = avg_grad > grad_threshold

        scales = model.scales
        max_scale = scales.max(dim=-1).values

        # Size threshold: Gaussians larger than this get split
        if extent is None:
            extent = (model.means.max(dim=0).values - model.means.min(dim=0).values).max().item()
        size_threshold = extent * 0.01

        # Split: large Gaussians with high gradient
        split_mask = high_grad & (max_scale > size_threshold)
        n_split = split_mask.sum().item()

        # Clone: small Gaussians with high gradient
        clone_mask = high_grad & (max_scale <= size_threshold)
        n_clone = clone_mask.sum().item()

        new_means = []
        new_log_scales = []
        new_quats = []
        new_logit_opacities = []
        new_sh = []

        if n_split > 0:
            # Split each into 2 offset copies with reduced scale
            split_means = model.means[split_mask]
            split_scales = scales[split_mask]
            stds = split_scales
            offsets = torch.randn_like(split_means) * stds
            new_means.append(split_means + offsets)
            new_means.append(split_means - offsets)
            reduced_log_scale = model.log_scales[split_mask] - math.log(1.6)
            new_log_scales.extend([reduced_log_scale, reduced_log_scale])
            new_quats.extend([model.quats[split_mask], model.quats[split_mask]])
            new_logit_opacities.extend([model.logit_opacities[split_mask],
                                         model.logit_opacities[split_mask]])
            new_sh.extend([model.sh_coeffs[split_mask], model.sh_coeffs[split_mask]])

        if n_clone > 0:
            new_means.append(model.means[clone_mask])
            new_log_scales.append(model.log_scales[clone_mask])
            new_quats.append(model.quats[clone_mask])
            new_logit_opacities.append(model.logit_opacities[clone_mask])
            new_sh.append(model.sh_coeffs[clone_mask])

        # Remove split originals
        keep_mask = ~split_mask

        # Prune low-opacity
        prune_mask = model.opacities < OPACITY_PRUNE_THRESHOLD
        keep_mask = keep_mask & ~prune_mask
        n_pruned = (~keep_mask & ~split_mask).sum().item()

        # Gather kept Gaussians
        kept_means = model.means[keep_mask]
        kept_log_scales = model.log_scales[keep_mask]
        kept_quats = model.quats[keep_mask]
        kept_logit_opacities = model.logit_opacities[keep_mask]
        kept_sh = model.sh_coeffs[keep_mask]

        if new_means:
            all_means = torch.cat([kept_means] + new_means)
            all_log_scales = torch.cat([kept_log_scales] + new_log_scales)
            all_quats = torch.cat([kept_quats] + new_quats)
            all_logit_opacities = torch.cat([kept_logit_opacities] + new_logit_opacities)
            all_sh = torch.cat([kept_sh] + new_sh)
        else:
            all_means = kept_means
            all_log_scales = kept_log_scales
            all_quats = kept_quats
            all_logit_opacities = kept_logit_opacities
            all_sh = kept_sh

        N_new = all_means.shape[0]
        model.means = nn.Parameter(all_means)
        model.log_scales = nn.Parameter(all_log_scales)
        model.quats = nn.Parameter(all_quats)
        model.logit_opacities = nn.Parameter(all_logit_opacities)
        model.sh_coeffs = nn.Parameter(all_sh)
        model.grad_accum = torch.zeros(N_new, device=model.device)
        model.grad_count = torch.zeros(N_new, device=model.device)

    return {'split': n_split, 'clone': n_clone, 'pruned': n_pruned, 'total': N_new}


print("ADC densification defined.")
"""))

# ── Cell 9: Farey-guided densification ──
cells.append(make_code_cell("""\
import torch
import torch.nn as nn
import numpy as np

def densify_farey(model, grad_threshold=GRAD_THRESHOLD, max_growth=0.05, extent=None):
    \"\"\"Farey-mediant-guided densification.

    Instead of splitting/cloning based purely on gradient magnitude,
    we find spatial gaps between adjacent Gaussians (sorted per axis)
    and insert mediants weighted by scale and reconstruction error.

    Steps:
    1. Sort Gaussians by position along each axis
    2. Find largest gaps between consecutive Gaussians
    3. Insert new Gaussians at mediant positions (weighted average)
    4. Gate insertions by reconstruction gradient
    5. Limit growth to max_growth fraction per step
    Also: prune low-opacity Gaussians (same as ADC)
    \"\"\"
    with torch.no_grad():
        N = model.num_gaussians
        max_new = max(int(N * max_growth), 1)

        avg_grad = model.grad_accum / (model.grad_count + 1e-8)
        positions = model.means.detach()

        # Collect gap candidates across all 3 axes
        candidates = []  # (score, pos, scale, quat, opacity, sh)

        for axis in range(3):
            sorted_idx = torch.argsort(positions[:, axis])
            sorted_pos = positions[sorted_idx]

            # Gaps between consecutive Gaussians along this axis
            gaps = sorted_pos[1:, axis] - sorted_pos[:-1, axis]

            # Score = gap size * average gradient of neighbors
            neighbor_grad = (avg_grad[sorted_idx[:-1]] + avg_grad[sorted_idx[1:]]) / 2
            scores = gaps * neighbor_grad

            # Only consider gaps where at least one neighbor has high gradient
            grad_ok = (avg_grad[sorted_idx[:-1]] > grad_threshold * 0.5) | \\
                      (avg_grad[sorted_idx[1:]] > grad_threshold * 0.5)

            for j in range(len(gaps)):
                if not grad_ok[j]:
                    continue
                idx_a = sorted_idx[j].item()
                idx_b = sorted_idx[j + 1].item()

                # Mediant position: weighted by inverse scale (smaller Gaussians get more weight)
                sa = model.scales[idx_a].mean().item()
                sb = model.scales[idx_b].mean().item()
                wa = 1.0 / (sa + 1e-8)
                wb = 1.0 / (sb + 1e-8)
                w_total = wa + wb
                mediant_pos = (positions[idx_a] * wa + positions[idx_b] * wb) / w_total

                # New Gaussian properties: interpolate
                mediant_scale = (model.log_scales[idx_a] + model.log_scales[idx_b]) / 2
                mediant_quat = (model.quats[idx_a] + model.quats[idx_b]) / 2
                mediant_opacity = (model.logit_opacities[idx_a] + model.logit_opacities[idx_b]) / 2
                mediant_sh = (model.sh_coeffs[idx_a] + model.sh_coeffs[idx_b]) / 2

                candidates.append((
                    scores[j].item(),
                    mediant_pos, mediant_scale, mediant_quat,
                    mediant_opacity, mediant_sh
                ))

        # Sort by score descending, take top max_new
        candidates.sort(key=lambda x: -x[0])
        candidates = candidates[:max_new]

        # Prune low-opacity first
        prune_mask = model.opacities < OPACITY_PRUNE_THRESHOLD
        keep_mask = ~prune_mask
        n_pruned = prune_mask.sum().item()

        kept_means = model.means[keep_mask]
        kept_log_scales = model.log_scales[keep_mask]
        kept_quats = model.quats[keep_mask]
        kept_logit_opacities = model.logit_opacities[keep_mask]
        kept_sh = model.sh_coeffs[keep_mask]

        n_inserted = len(candidates)
        if n_inserted > 0:
            new_means = torch.stack([c[1] for c in candidates])
            new_log_scales = torch.stack([c[2] for c in candidates])
            new_quats = torch.stack([c[3] for c in candidates])
            new_logit_opacities = torch.stack([c[4] for c in candidates])
            new_sh = torch.stack([c[5] for c in candidates])

            all_means = torch.cat([kept_means, new_means])
            all_log_scales = torch.cat([kept_log_scales, new_log_scales])
            all_quats = torch.cat([kept_quats, new_quats])
            all_logit_opacities = torch.cat([kept_logit_opacities, new_logit_opacities])
            all_sh = torch.cat([kept_sh, new_sh])
        else:
            all_means = kept_means
            all_log_scales = kept_log_scales
            all_quats = kept_quats
            all_logit_opacities = kept_logit_opacities
            all_sh = kept_sh

        N_new = all_means.shape[0]
        model.means = nn.Parameter(all_means)
        model.log_scales = nn.Parameter(all_log_scales)
        model.quats = nn.Parameter(all_quats)
        model.logit_opacities = nn.Parameter(all_logit_opacities)
        model.sh_coeffs = nn.Parameter(all_sh)
        model.grad_accum = torch.zeros(N_new, device=model.device)
        model.grad_count = torch.zeros(N_new, device=model.device)

    return {'inserted': n_inserted, 'pruned': n_pruned, 'total': N_new}


print("Farey-guided densification defined.")
"""))

# ── Cell 10: Training loop ──
cells.append(make_code_cell("""\
import torch
import torch.nn.functional as F
import time
import math
import copy

def compute_psnr(img1, img2):
    mse = F.mse_loss(img1, img2).item()
    if mse < 1e-10:
        return 50.0
    return -10.0 * math.log10(mse)

def compute_ssim_simple(img1, img2, window_size=11):
    \"\"\"Simplified SSIM on (H,W,3) tensors.\"\"\"
    # Move to (1, 3, H, W) for F.avg_pool2d
    a = img1.permute(2, 0, 1).unsqueeze(0)
    b = img2.permute(2, 0, 1).unsqueeze(0)
    C1, C2 = 0.01**2, 0.03**2
    pad = window_size // 2
    mu_a = F.avg_pool2d(a, window_size, 1, pad)
    mu_b = F.avg_pool2d(b, window_size, 1, pad)
    mu_a2 = mu_a * mu_a
    mu_b2 = mu_b * mu_b
    mu_ab = mu_a * mu_b
    sig_a2 = F.avg_pool2d(a * a, window_size, 1, pad) - mu_a2
    sig_b2 = F.avg_pool2d(b * b, window_size, 1, pad) - mu_b2
    sig_ab = F.avg_pool2d(a * b, window_size, 1, pad) - mu_ab
    num = (2 * mu_ab + C1) * (2 * sig_ab + C2)
    den = (mu_a2 + mu_b2 + C1) * (sig_a2 + sig_b2 + C2)
    ssim_map = num / den
    return ssim_map.mean().item()

def evaluate_test(model, test_data):
    model.eval()
    psnrs, ssims = [], []
    with torch.no_grad():
        for td in test_data:
            pred, _, _ = model.render(td['viewmat'], td['K'], td['H'], td['W'])
            gt = td['gt'].to(model.device)
            pred = torch.clamp(pred, 0, 1)
            psnrs.append(compute_psnr(pred, gt))
            ssims.append(compute_ssim_simple(pred, gt))
    model.train()
    return np.mean(psnrs), np.mean(ssims)


def train_loop(method_name, densify_fn, train_data, test_data, init_pts, init_cols,
               n_iters=TOTAL_ITERS, seed=42):
    \"\"\"Full training loop. Returns metrics dict.\"\"\"
    torch.manual_seed(seed)
    np.random.seed(seed)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    model = GaussianModel(init_pts, init_cols, device=device)
    model.train()

    # Separate learning rates per parameter
    optimizer = torch.optim.Adam([
        {'params': [model.means], 'lr': LR_POSITION, 'name': 'means'},
        {'params': [model.sh_coeffs], 'lr': LR_FEATURE, 'name': 'sh'},
        {'params': [model.logit_opacities], 'lr': LR_OPACITY, 'name': 'opacity'},
        {'params': [model.log_scales], 'lr': LR_SCALE, 'name': 'scale'},
        {'params': [model.quats], 'lr': LR_ROTATION, 'name': 'rotation'},
    ])

    metrics = {'train_loss': [], 'test_psnr': [], 'test_ssim': [],
               'n_gaussians': [], 'timestamps': []}
    t0 = time.time()

    for step in range(1, n_iters + 1):
        # Random training image
        td = train_data[np.random.randint(len(train_data))]
        gt = td['gt'].to(device)

        pred, alpha, meta = model.render(td['viewmat'], td['K'], td['H'], td['W'])
        pred = torch.clamp(pred, 0, 1)

        # L1 + D-SSIM loss
        l1_loss = F.l1_loss(pred, gt)
        loss = 0.8 * l1_loss + 0.2 * (1 - compute_ssim_simple(pred.detach(), gt.detach()))

        optimizer.zero_grad()
        l1_loss.backward()  # Use l1 for gradient computation (simpler, standard)

        # Accumulate positional gradients for densification
        model.accumulate_gradients(meta)

        optimizer.step()

        # Densification
        if DENSIFY_START <= step <= min(DENSIFY_STOP, n_iters):
            if step % DENSIFY_INTERVAL == 0:
                info = densify_fn(model)

                # Rebuild optimizer for new parameters
                optimizer = torch.optim.Adam([
                    {'params': [model.means], 'lr': LR_POSITION, 'name': 'means'},
                    {'params': [model.sh_coeffs], 'lr': LR_FEATURE, 'name': 'sh'},
                    {'params': [model.logit_opacities], 'lr': LR_OPACITY, 'name': 'opacity'},
                    {'params': [model.log_scales], 'lr': LR_SCALE, 'name': 'scale'},
                    {'params': [model.quats], 'lr': LR_ROTATION, 'name': 'rotation'},
                ])
                model.reset_grad_stats()

                if step % (DENSIFY_INTERVAL * 5) == 0:
                    print(f"  [{method_name}] Step {step}: densify {info}, "
                          f"loss={l1_loss.item():.4f}")

        # Opacity reset
        if step % OPACITY_RESET_INTERVAL == 0 and step < n_iters - 500:
            with torch.no_grad():
                model.logit_opacities.fill_(torch.logit(torch.tensor(0.01)).item())

        # Log metrics periodically
        if step % 500 == 0 or step == n_iters:
            test_psnr, test_ssim = evaluate_test(model, test_data)
            elapsed = time.time() - t0
            metrics['train_loss'].append(l1_loss.item())
            metrics['test_psnr'].append(test_psnr)
            metrics['test_ssim'].append(test_ssim)
            metrics['n_gaussians'].append(model.num_gaussians)
            metrics['timestamps'].append(elapsed)
            print(f"[{method_name}] Step {step}/{n_iters} | "
                  f"Loss: {l1_loss.item():.4f} | PSNR: {test_psnr:.2f} | "
                  f"SSIM: {test_ssim:.4f} | #G: {model.num_gaussians} | "
                  f"Time: {elapsed:.0f}s")

    # Final evaluation
    final_psnr, final_ssim = evaluate_test(model, test_data)
    metrics['final_psnr'] = final_psnr
    metrics['final_ssim'] = final_ssim
    metrics['final_n_gaussians'] = model.num_gaussians
    metrics['total_time'] = time.time() - t0
    metrics['method'] = method_name
    metrics['seed'] = seed

    print(f"\\n[{method_name}] FINAL: PSNR={final_psnr:.2f}, SSIM={final_ssim:.4f}, "
          f"#G={model.num_gaussians}, Time={metrics['total_time']:.0f}s\\n")

    return metrics


print("Training loop defined.")
"""))

# ── Cell 11: Run experiments ──
cells.append(make_code_cell("""\
import json as _json

all_results = []

for seed in SEEDS:
    for method_name, densify_fn in [('ADC', densify_adc), ('Farey', densify_farey)]:
        print(f"{'='*60}")
        print(f"Running: {method_name}, seed={seed}")
        print(f"{'='*60}")
        result = train_loop(
            method_name=method_name,
            densify_fn=densify_fn,
            train_data=train_data,
            test_data=test_data,
            init_pts=init_pts.copy(),
            init_cols=init_cols.copy(),
            n_iters=TOTAL_ITERS,
            seed=seed,
        )
        all_results.append(result)

# Save results to JSON
with open('/content/3dgs_results.json', 'w') as f:
    # Convert non-serializable types
    serializable = []
    for r in all_results:
        sr = {}
        for k, v in r.items():
            if isinstance(v, (list, int, float, str)):
                sr[k] = v
            else:
                sr[k] = str(v)
        serializable.append(sr)
    _json.dump(serializable, f, indent=2)
    print("Results saved to /content/3dgs_results.json")
"""))

# ── Cell 12: Display results ──
cells.append(make_code_cell("""\
import numpy as np

# ── Summary Table ──
print("=" * 70)
print(f"{'Method':<10} {'Seed':<6} {'PSNR':>8} {'SSIM':>8} {'#Gauss':>10} {'Time(s)':>8}")
print("-" * 70)

adc_results = [r for r in all_results if r['method'] == 'ADC']
farey_results = [r for r in all_results if r['method'] == 'Farey']

for r in all_results:
    print(f"{r['method']:<10} {r['seed']:<6} {r['final_psnr']:>8.2f} "
          f"{r['final_ssim']:>8.4f} {r['final_n_gaussians']:>10} "
          f"{r['total_time']:>8.0f}")

print("-" * 70)

if len(adc_results) > 0 and len(farey_results) > 0:
    adc_psnr = np.mean([r['final_psnr'] for r in adc_results])
    farey_psnr = np.mean([r['final_psnr'] for r in farey_results])
    adc_ssim = np.mean([r['final_ssim'] for r in adc_results])
    farey_ssim = np.mean([r['final_ssim'] for r in farey_results])
    adc_ng = np.mean([r['final_n_gaussians'] for r in adc_results])
    farey_ng = np.mean([r['final_n_gaussians'] for r in farey_results])

    print(f"{'ADC avg':<10} {'':6} {adc_psnr:>8.2f} {adc_ssim:>8.4f} {adc_ng:>10.0f}")
    print(f"{'Farey avg':<10} {'':6} {farey_psnr:>8.2f} {farey_ssim:>8.4f} {farey_ng:>10.0f}")
    print(f"\\nDelta PSNR: {farey_psnr - adc_psnr:+.2f} dB")
    print(f"Delta SSIM: {farey_ssim - adc_ssim:+.4f}")
    print(f"Gaussian ratio: {farey_ng / adc_ng:.2f}x")

# ── Training Curves ──
try:
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    for r in all_results:
        steps = list(range(500, TOTAL_ITERS + 1, 500))
        label = f"{r['method']} (s={r['seed']})"
        axes[0].plot(steps[:len(r['test_psnr'])], r['test_psnr'], label=label)
        axes[1].plot(steps[:len(r['test_ssim'])], r['test_ssim'], label=label)
        axes[2].plot(steps[:len(r['n_gaussians'])], r['n_gaussians'], label=label)

    axes[0].set_title('Test PSNR')
    axes[0].set_xlabel('Iteration')
    axes[0].set_ylabel('PSNR (dB)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].set_title('Test SSIM')
    axes[1].set_xlabel('Iteration')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    axes[2].set_title('Gaussian Count')
    axes[2].set_xlabel('Iteration')
    axes[2].set_ylabel('# Gaussians')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/content/3dgs_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Plot saved to /content/3dgs_comparison.png")
except ImportError:
    print("matplotlib not available, skipping plots")

print("\\nDone! Download 3dgs_results.json for full metrics.")
"""))

# ── Build notebook ──
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.12"
        },
        "accelerator": "GPU",
        "colab": {
            "provenance": [],
            "gpuType": "T4"
        }
    },
    "cells": cells
}

out_path = os.path.expanduser("~/Desktop/Farey-Local/experiments/3dgs_colab_v2.ipynb")
with open(out_path, 'w') as f:
    json.dump(notebook, f, indent=1)

print(f"Wrote {out_path}")
print(f"Total cells: {len(cells)} ({sum(1 for c in cells if c['cell_type']=='code')} code, "
      f"{sum(1 for c in cells if c['cell_type']=='markdown')} markdown)")

# Count lines
total_lines = 0
for c in cells:
    total_lines += len(c['source'])
print(f"Total source lines: {total_lines}")

# Validate
import json as json2
with open(out_path, 'r') as f:
    nb = json2.load(f)
print(f"JSON load: OK ({len(nb['cells'])} cells)")

# Validate code cells compile (skip cells with ! commands)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    source = ''.join(cell['source'])
    # Skip cells with shell commands
    if source.strip().startswith('!') or '\n!' in source:
        # Check only the Python parts
        py_lines = [l for l in source.split('\n') if not l.strip().startswith('!')]
        py_source = '\n'.join(py_lines)
        if py_source.strip():
            try:
                compile(py_source, f"<cell_{i}>", "exec")
            except SyntaxError as e:
                print(f"WARNING: Cell {i} Python parts have syntax issue: {e}")
        continue
    try:
        compile(source, f"<cell_{i}>", "exec")
        print(f"Cell {i}: compile OK")
    except SyntaxError as e:
        print(f"FAIL Cell {i}: {e}")
        sys.exit(1)

print("\nAll validations passed!")
