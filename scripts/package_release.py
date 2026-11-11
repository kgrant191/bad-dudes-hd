"""Package the approved runtime without a ROM or emulator dependency."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def package(output):
    manifest = json.loads((ROOT / 'validation/v1.0.0_release.json').read_text())
    expected = manifest['pack_sha256']
    pack = ROOT / 'pack'
    actual = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
              for p in pack.iterdir() if p.is_file()}
    if actual != expected or len(actual) != 13:
        raise ValueError('Runtime files differ from the approved release manifest')
    if any(Path(name).suffix not in {'.png', '.txt'} for name in expected):
        raise ValueError('Unexpected install-pack file type')
    output.mkdir(parents=True, exist_ok=True)
    target = output / 'Bad_Dudes_HD_v1.0.0.zip'
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for name in sorted(expected):
            info = zipfile.ZipInfo(name, (2026, 11, 10, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (pack / name).read_bytes(), compresslevel=9)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP integrity check failed')
        unpacked = {name: hashlib.sha256(archive.read(name)).hexdigest()
                    for name in archive.namelist()}
        if unpacked != expected:
            raise ValueError('ZIP contents differ from the approved runtime')
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(json.dumps({'file': str(target), 'files': len(expected), 'sha256': digest}))
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    package(parser.parse_args().output)
