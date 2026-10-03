"""
Bug Resolution Impact & Module Regression Scope Analyzer
Identifies modified modules, files, and recommends regression test cases based on resolved Bug fixes.
"""

import sys
import json
import re

# Architecture mapping: File path pattern -> Subsystem/Module & QA Test Scope
MODULE_MAPPING = {
    r".*(audio|sound|codec|dsp).*": {
        "module": "Audio & DSP HAL",
        "impact_level": "HIGH",
        "test_scope": [
            "Audio/Video Sync Verification",
            "Multi-channel Audio Output Test",
            "Headset/Bluetooth Audio Routing",
            "DSP Power Consumption Baseline"
        ]
    },
    r".*(camera|isp|sensor).*": {
        "module": "Camera & Imaging Subsystem",
        "impact_level": "HIGH",
        "test_scope": [
            "Low-light capture & HDR verification",
            "Camera launch & switch latency",
            "Video recording (4K 60fps) stability"
        ]
    },
    r".*(video|mediaservice|stagefright|codec).*": {
        "module": "Multimedia & Video Codecs",
        "impact_level": "CRITICAL",
        "test_scope": [
            "H.264/H.265/VP9 playback sanity",
            "Secure OTT playback (Widevine L1/Netflix)",
            "Hardware decoding under stress cycles"
        ]
    },
    r".*(thermal|power|battery|governor).*": {
        "module": "Thermal & Power Management",
        "impact_level": "MEDIUM",
        "test_scope": [
            "Thermal throttling under 3D gaming load",
            "Current drain profiling in screen-off state",
            "DVFS clock scaling validation"
        ]
    },
    r".*(display|drm|gpu|surfaceflinger).*": {
        "module": "Display & GPU Pipeline",
        "impact_level": "HIGH",
        "test_scope": [
            "Refresh rate switching (60Hz -> 120Hz)",
            "SurfaceFlinger frame drop / jank analysis",
            "Display flicker on low brightness"
        ]
    }
}

# Mock database representing resolved bugs and corresponding Git commit patches
RESOLVED_BUGS_DB = {
    "BUG-84920": {
        "title": "Netflix VP9 video decoding freeze under low memory",
        "developer": "Codec Team",
        "status": "RESOLVED / MERGED",
        "commit_hash": "a4f891b",
        "changed_files": [
            "frameworks/av/media/libstagefright/codecs/vp9/dec/vpx_decoder.cpp",
            "hardware/interfaces/media/omx/1.0/vpu_driver.c",
            "kernel/drivers/video/mediatek/vcodec/vcodec_drv.c"
        ]
    },
    "BUG-73104": {
        "title": "Camera HAL crash when switching from portrait to night mode",
        "developer": "Imaging Team",
        "status": "RESOLVED / MERGED",
        "commit_hash": "c7104ae",
        "changed_files": [
            "hardware/interfaces/camera/provider/2.4/default/CameraDevice.cpp",
            "vendor/mediatek/proprietary/custom/isp/isp_sensor_tune.h"
        ]
    },
    "BUG-91022": {
        "title": "Excessive battery drain during background audio streaming",
        "developer": "Audio Team",
        "status": "RESOLVED / MERGED",
        "commit_hash": "e129f9c",
        "changed_files": [
            "hardware/interfaces/audio/core/all-versions/default/StreamOut.cpp",
            "kernel/sound/soc/mediatek/common/mtk-dsp-audio.c"
        ]
    }
}

def analyze_bug_impact(bug_id):
    print("=" * 70)
    print(f"       BUG IMPACT & REGRESSION BLAST-RADIUS ANALYZER")
    print("=" * 70)
    
    bug_info = RESOLVED_BUGS_DB.get(bug_id.upper())
    
    if not bug_info:
        print(f"[!] Bug ID '{bug_id}' not found in resolved database.")
        print(f"    Available sample IDs: {', '.join(RESOLVED_BUGS_DB.keys())}")
        return

    print(f"Bug ID       : {bug_id.upper()}")
    print(f"Summary      : {bug_info['title']}")
    print(f"Resolution   : {bug_info['status']} (Commit: {bug_info['commit_hash']})")
    print(f"Resolved By  : {bug_info['developer']}")
    print("-" * 70)
    
    print("\n[+] Changed Files in Patch:")
    for f in bug_info["changed_files"]:
        print(f"  • {f}")

    # Map changed files to system modules & regression scope
    affected_modules = set()
    recommended_tests = set()
    max_impact = "LOW"

    for file_path in bug_info["changed_files"]:
        for pattern, config in MODULE_MAPPING.items():
            if re.match(pattern, file_path, re.IGNORECASE):
                affected_modules.add(config["module"])
                for test in config["test_scope"]:
                    recommended_tests.add(test)
                if config["impact_level"] in ["CRITICAL", "HIGH"]:
                    max_impact = config["impact_level"]

    print("\n" + "=" * 70)
    print(f"[!] IMPACT ASSESSMENT: {max_impact} BLAST RADIUS")
    print(f"[!] Affected Subsystems: {', '.join(affected_modules) if affected_modules else 'General Core'}")
    print("=" * 70)

    print("\n[*] Recommended QA Verification / Regression Test Scope:")
    for idx, test in enumerate(recommended_tests, 1):
        print(f"  {idx}. [MUST RUN] {test}")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    target_bug = sys.argv[1] if len(sys.argv) > 1 else "BUG-84920"
    analyze_bug_impact(target_bug)
