"""Build "DCF Valuation.app" (a self-contained macOS app) and zip it.

Usage: python3 tools/build_mac_app.py
Output: dist/DCF-Valuation-mac.zip

The app bundles the calculator in dcf-calculator/ and opens it in the
default browser. It runs fully offline. Nothing needs compiling, so the
zip can be built on any OS.
"""
import shutil, subprocess, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "dcf-calculator"
DIST = ROOT / "dist"
APP_NAME = "DCF Valuation"
VERSION = "2.0"

LAUNCHER = """#!/bin/bash
# Copy the calculator to a fixed folder, then open it. A fixed path keeps the
# browser's saved valuations even if macOS runs the app from a temporary place.
SRC="$(cd "$(dirname "$0")/../Resources/app" && pwd)"
DEST="$HOME/Library/Application Support/DCF Valuation"
mkdir -p "$DEST"
/usr/bin/ditto "$SRC" "$DEST/app"
/usr/bin/open "$DEST/app/index.html"
"""

PLIST = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>{APP_NAME}</string>
  <key>CFBundleDisplayName</key><string>{APP_NAME}</string>
  <key>CFBundleIdentifier</key><string>com.jcannam.dcfvaluation</string>
  <key>CFBundleVersion</key><string>{VERSION}</string>
  <key>CFBundleShortVersionString</key><string>{VERSION}</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleExecutable</key><string>launch</string>
  <key>CFBundleIconFile</key><string>AppIcon</string>
  <key>LSMinimumSystemVersion</key><string>10.13</string>
  <key>LSApplicationCategoryType</key><string>public.app-category.finance</string>
  <key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
"""

def main():
    sys.path.insert(0, str(ROOT / "tools"))
    from make_icons import icns
    build = DIST / "build"
    shutil.rmtree(build, ignore_errors=True)
    app = build / f"{APP_NAME}.app" / "Contents"
    (app / "MacOS").mkdir(parents=True)
    (app / "Resources").mkdir()
    (app / "Info.plist").write_text(PLIST)
    (app / "MacOS" / "launch").write_text(LAUNCHER)
    icns(app / "Resources" / "AppIcon.icns")
    shutil.copytree(SRC, app / "Resources" / "app")

    DIST.mkdir(exist_ok=True)
    out = DIST / "DCF-Valuation-mac.zip"
    out.unlink(missing_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(build.rglob("*")):
            rel = p.relative_to(build).as_posix()
            if p.is_dir():
                zi = zipfile.ZipInfo(rel + "/"); zi.external_attr = (0o40755 << 16) | 0x10
                z.writestr(zi, b"")
            else:
                zi = zipfile.ZipInfo(rel)
                mode = 0o100755 if p.name == "launch" else 0o100644
                zi.external_attr = mode << 16
                zi.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(zi, p.read_bytes())
    shutil.rmtree(build)
    print(f"Built {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    main()
