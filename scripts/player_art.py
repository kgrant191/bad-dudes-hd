"""Slice painted pose sheets into the game's original 8x8 sprite cells."""
from common import *
from collections import defaultdict
import json


def player_art(player=1):
    poses = json.loads((ROOT / 'metadata/player_poses.json').read_text())
    prefix = 'player_sheet' if player == 1 else 'player2'
    sheets = [Image.open(ROOT / f'art/{prefix}_{name}.png').convert('RGBA')
              for name in ['main', 'extra']]
    variants = defaultdict(list)
    previews = []
    stats = []
    for i, pose in enumerate(poses):
        rows = pose['tiles']
        width = max(r[0] for r in rows) + 8
        height = max(r[1] for r in rows) + 8
        original = Image.new('RGBA', (width * 4, height * 4))
        coverage = Image.new('L', original.size)
        for x, y, t, h, v in rows:
            im = scale(tile(t, 0xff0f2620))
            if h: im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if v: im = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            original.alpha_composite(im, (x * 4, y * 4))
            coverage.paste(255, (x * 4, y * 4, (x + 8) * 4, (y + 8) * 4))
        sheet, j, columns = (sheets[0], i, 4) if i < 16 else (sheets[1], i - 16, 2)
        cell = sheet.width // columns
        crop = sheet.crop((j % columns * cell, j // columns * cell,
                           (j % columns + 1) * cell, (j // columns + 1) * cell))
        # Anchor art to the original sprite's bounding box, preserving its
        # location and full pose dimensions. No changes to animation or ROM.
        bbox = original.getchannel('A').getbbox()
        painted_bbox = crop.getchannel('A').point(lambda a: 255 if a > 24 else 0).getbbox()
        if not painted_bbox: raise ValueError(f'Empty player art cell {i}')
        painted = crop.crop(painted_bbox).resize((bbox[2] - bbox[0], bbox[3] - bbox[1]), Image.Resampling.LANCZOS)
        canvas = Image.new('RGBA', original.size)
        canvas.alpha_composite(painted, bbox[:2])
        a = np.array(canvas)
        loss = ((a[:, :, 3] > 32) & (np.array(coverage) == 0)).sum()
        stats.append({'pose': i, 'frame': pose['frame'], 'tiles': len(rows),
                      'clipped_pixels': int(loss), 'opaque_pixels': int((a[:, :, 3] > 32).sum())})
        for x, y, t, h, v in rows:
            im = canvas.crop((x * 4, y * 4, (x + 8) * 4, (y + 8) * 4))
            if h: im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if v: im = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            variants[t].append({'pose': i, 'x': x, 'y': y, 'h': h, 'v': v, 'image': im})
        previews.append((original, canvas, coverage))
    return variants, poses, previews, stats


def flash(im):
    """Keep the game's warm power/damage flash on the detailed artwork."""
    a = np.array(im).astype(float)
    rgb = a[:, :, :3]
    rgb[:] = np.minimum(255, rgb * .55 + np.array([255, 126, 57]) * .45)
    return Image.fromarray(a.astype('uint8'))


if __name__ == '__main__':
    from PIL import ImageDraw
    variants, poses, previews, stats = player_art()
    out = Image.new('RGB', (1280, 1200), '#333e4a')
    d = ImageDraw.Draw(out)
    for i, (original, painted, coverage) in enumerate(previews):
        x, y = (i % 5) * 256, (i // 5) * 300
        d.text((x + 6, y + 4), f'Pose {i}, frame {poses[i]["frame"]}', fill='white')
        # Preview the exact cell coverage that the engine will render.
        a = np.array(painted);a[np.array(coverage) == 0, 3] = 0
        painted = Image.fromarray(a)
        out.paste(painted, (x + 16, y + 32), painted)
    out.save(ROOT / 'validation/player_pose_review.png')
    (ROOT / 'validation/player_slicing.json').write_text(json.dumps(stats, indent=2))
    print(json.dumps({'unique_tiles': len(variants), 'poses': len(poses), 'clipping': stats}, indent=2))
