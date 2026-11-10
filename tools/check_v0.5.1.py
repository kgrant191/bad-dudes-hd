"""Verify v0.5.1 mappings and matching MesenCE replay screenshots."""
import argparse
from collections import defaultdict
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--baseline', type=Path, required=True)
parser.add_argument('--before', type=Path, required=True)
parser.add_argument('--after', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
pack = root / 'pack'


def rules(text, atlas):
    result = defaultdict(list)
    for line in text.splitlines():
        if '<tile>' not in line:
            continue
        condition, value = line.split('<tile>')
        fields = value.split(',')
        x, y = map(int, fields[3:5])
        assert 0 <= x <= atlas.width - 32 and 0 <= y <= atlas.height - 32
        key = (condition, *fields[:3], *fields[5:])
        result[key].append(hashlib.sha256(atlas.crop((x, y, x+32, y+32)).tobytes()).hexdigest())
    return result


text = (pack / 'hires.txt').read_text()
current = rules(text, Image.open(pack / 'tiles.png'))
with zipfile.ZipFile(args.baseline) as baseline:
    previous = rules(baseline.read('hires.txt').decode(), Image.open(io.BytesIO(baseline.read('tiles.png'))))
    changed = [key for key, value in previous.items() if current.get(key) != value]
    assert all(key[0] == '[level2&hud&stage_area]' for key in changed), changed
    assert all(int(key[2], 16) < 0x800 for key in changed), changed
    added = set(current) - set(previous)
    assert all(key[0].startswith('[level2&hud&stage_area&') for key in added)
    scenes = [name for name in baseline.namelist() if name.endswith('.png') and name != 'tiles.png']
    for name in scenes:
        assert baseline.read(name) == (pack / name).read_bytes(), name

conditions = {line.split('>')[1].split(',')[0] for line in text.splitlines() if line.startswith('<condition>')}
for line in text.splitlines():
    if line.startswith('['):
        assert set(line[1:line.index(']')].split('&')) <= conditions, line

green_pairs = 0
for key, value in current.items():
    condition, image, tile, palette, *rest = key
    t = int(tile, 16)
    if condition == '[level2&hud&stage_area]' and palette == '0F091910' and 0x500 <= t < 0x580:
        pair = (condition, image, f'{t+0x280:X}', palette, *rest)
        if pair in current:
            assert value == current[pair], (key, pair)
            green_pairs += 1

frames = sorted(args.after.glob('*.png'))
assert len(frames) == 264, len(frames)
for path in frames:
    a = np.array(Image.open(path).convert('RGBA'))
    b = np.array(Image.open(args.before / path.name).convert('RGBA'))
    assert np.array_equal(a[800:], b[800:]), ('HUD changed', path.name)
    assert np.array_equal(a[:384], b[:384]), ('skyline/upper sprites changed', path.name)

# Identify each full wheel by its hub, then check its complete top row.
# This catches the intermittent blank $700 cell without relying on one phase.
template = np.array(Image.open(args.after / '00600.png').convert('RGBA'))[640:768,512:640]
hub_hash = hashlib.sha256(template[32:96].tobytes()).digest()
wheel_count = 0
for frame in range(590, 661):
    strip = np.array(Image.open(args.after / f'{frame:05d}.png').convert('RGBA'))[640:768]
    matches = [x for x in range(0,897,4)
               if hashlib.sha256(strip[32:96,x:x+128].tobytes()).digest() == hub_hash]
    assert len(matches) >= 4, (frame, matches)
    for x in matches:
        assert np.array_equal(strip[:32,x:x+128], template[:32]), ('tire gap', frame, x)
        wheel_count += 1

cab_hashes = {
    hashlib.sha256(Image.open(args.after / f'{frame:05d}.png')
                   .crop((0,388,384,768)).tobytes()).digest()
    for frame in range(7480,7561)
}
assert len(cab_hashes) == 1, 'Cab body or wheel flickers while stationary'

report = {
    'version': '0.5.1',
    'movie_inputs': 8850,
    'sampled_frames': len(frames),
    'dense_wheel_frames': 71,
    'complete_tread_checks': wheel_count,
    'stable_cab_frames': 81,
    'identical_green_bank_pairs': green_pairs,
    'changed_level2_scenery_rules': len(changed),
    'added_context_rules': len(added),
    'unchanged_other_rule_images': len(previous)-len(changed),
    'unchanged_scene_pngs': len(scenes),
    'hud_and_upper_scene_pixel_identical': True,
    'changed_rules': [{'tile': key[2], 'palette': key[3]} for key in changed],
}
args.output.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k != 'changed_rules'}, indent=2))
