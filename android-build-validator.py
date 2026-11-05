import json
import subprocess
import sys
import argparse
import os
import re
from datetime import datetime

__version__ = "1.0.0"

DEFAULT_PROPERTIES = [
    "ro.build.date",
    "ro.build.fingerprint"
]

def get_system_property(prop_name):
    """Get system property value from ADB"""
    try:
        cmd = f"adb shell getprop {prop_name}"
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode('utf-8').strip()
        return output if output else "N/A"
    except Exception:
        return "N/A"

def get_actual_version(package_id):
    """Get actual version from ADB"""
    try:
        cmd = f"adb shell dumpsys package {package_id} | grep versionName"
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode('utf-8').strip()
        if output and "=" in output:
            return output.split('=')[1].split()[0]
    except Exception:
        return None
    return None

def is_expected_not_installed(version_val):
    """Check if the configured version indicates the app should not be installed"""
    if version_val is None:
        return True
    return str(version_val).strip().lower() in ("", "n/a", "not installed", "not_installed", "none")

def ensure_configs_dir(config_dir="configs"):
    """Ensure configs directory exists, generate example if empty"""
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print(f"📁 Directory created: {config_dir}")

    json_files = [f for f in os.listdir(config_dir) if f.endswith('.json')]
    if not json_files:
        example_path = os.path.join(config_dir, "example_config.json")
        example_data = {
            "project_name": "Example Project",
            "apps_to_check": [
                {
                    "name": "YouTube",
                    "package_name": "com.google.android.youtube",
                    "version": "19.01.33"
                },
                {
                    "name": "Line",
                    "package_name": "jp.naver.line.android",
                    "version": "14.1.1"
                }
            ]
        }
        with open(example_path, 'w', encoding='utf-8') as f:
            json.dump(example_data, f, indent=4)
        print(f"💡 Generated example config: {example_path}")

def generate_html_report(project_name, prop_results, results, report_folder="reports"):
    """Generate a stylized HTML report"""
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)
        print(f"📁 Created report folder: {report_folder}")

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = now.strftime("%Y%m%d_%H%M%S")
    safe_project_name = re.sub(r'[\\/*?:"<>|\s]+', '_', project_name).strip('_') or "project"
    output_path = os.path.join(report_folder, f"report_{safe_project_name}_{file_timestamp}.html")
    
    prop_rows = ""
    for p in prop_results:
        prop_rows += f"""
        <tr>
            <td><code>{p['property']}</code></td>
            <td><code>{p['value']}</code></td>
        </tr>
        """

    rows = ""
    for r in results:
        status_color = "#28a745" if "✅" in r['status'] else "#dc3545" if "❌" in r['status'] else "#ffc107"
        rows += f"""
        <tr>
            <td>{r['name']}</td>
            <td><code>{r['pkg_id']}</code></td>
            <td>{r['expected']}</td>
            <td>{r['actual']}</td>
            <td style="color: {status_color}; font-weight: bold;">{r['status']}</td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Android Build Validation Report - {project_name}</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; margin: 40px; background: #f4f7f6; color: #333; }}
            .container {{ max-width: 1000px; margin: auto; }}
            table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 25px; }}
            th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #eee; }}
            th {{ background-color: #007bff; color: white; text-transform: uppercase; font-size: 14px; }}
            tr:hover {{ background-color: #f9f9f9; }}
            .header {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 5px solid #007bff; }}
            h1 {{ margin-top: 0; color: #007bff; }}
            h2 {{ color: #333; font-size: 18px; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📱 Android Build Validation Report</h1>
                <p><strong>Project:</strong> {project_name}</p>
                <p><strong>Generated At:</strong> {timestamp}</p>
            </div>
            <h2>🔧 System Properties</h2>
            <table>
                <thead>
                    <tr>
                        <th style="width: 35%;">Property</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    {prop_rows}
                </tbody>
            </table>
            <h2>📦 APK Versions</h2>
            <table>
                <thead>
                    <tr>
                        <th>App Name</th>
                        <th>Package Name</th>
                        <th>Expected</th>
                        <th>Actual</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            <div style="margin-top:20px; text-align:center; font-size:12px; color:#999;">
                Powered by Android Build Validator v{__version__}
            </div>
        </div>
    </body>
    </html>
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"\n📑 HTML report generated: {os.path.abspath(output_path)}")

def select_config_file(config_dir="configs"):
    """Interactive config selection"""
    ensure_configs_dir(config_dir)

    json_files = [f for f in os.listdir(config_dir) if f.endswith('.json')]
    if len(json_files) == 1:
        return os.path.join(config_dir, json_files[0])
    
    print(f"\n📂 Available configurations in '{config_dir}':")
    for idx, filename in enumerate(json_files, 1):
        print(f"  {idx}. {filename}")
    
    while True:
        try:
            choice = input(f"\nSelect a configuration file (1-{len(json_files)}): ")
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(json_files):
                return os.path.join(config_dir, json_files[choice_idx])
        except (ValueError, KeyboardInterrupt):
            sys.exit("\nExecution terminated by user.")
        print("❌ Invalid input. Please try again.")

def run_validator(config_path, output_html=False):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error: Failed to read config file ({e})")
        return

    project_name = data.get("project_name", os.path.basename(config_path))
    props = data.get("properties_to_check", DEFAULT_PROPERTIES)
    apps = data.get("apps_to_check", [])
    prop_results = []
    results = []
    
    print(f"\n🚀 Project: {project_name} (Script v{__version__})")

    print("\n🔧 System Properties")
    prop_header = f"{'Property':<30} | {'Value'}"
    print("-" * 115)
    print(prop_header)
    print("-" * 115)
    for prop in props:
        val = get_system_property(prop)
        print(f"{prop:<30} | {val}")
        prop_results.append({
            'property': prop,
            'value': val
        })

    print("\n📦 APK Versions")
    header = f"{'App Name':<20} | {'Package Name':<30} | {'Expected':<20} | {'Actual':<20} | {'Status':<12}"
    print("-" * 115)
    print(header)
    print("-" * 115)

    for app in apps:
        name = app.get("name", "Unknown")
        pkg_id = app.get("package_name")
        raw_expected = app.get("version")
        expect_not_installed = is_expected_not_installed(raw_expected)
        expected_v = "Not Installed" if expect_not_installed else str(raw_expected).strip()
        actual_v = get_actual_version(pkg_id)
        
        if expect_not_installed:
            if actual_v is None:
                status = "✅ Pass"
                actual_v = "Not Installed"
            else:
                status = "❌ Unexpected Installed"
        else:
            if actual_v is None:
                status = "❌ Not Installed"
                actual_v = "Not Installed"
            elif actual_v == expected_v:
                status = "✅ Pass"
            else:
                status = "⚠️ Mismatch"
            
        print(f"{name:<20} | {pkg_id:<30} | {expected_v:<20} | {actual_v:<20} | {status:<12}")
        results.append({
            'name': name, 'pkg_id': pkg_id, 'expected': expected_v, 
            'actual': actual_v, 'status': status
        })
    
    if output_html:
        generate_html_report(project_name, prop_results, results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="📱 Android Build Validator - Check device build & APK versions against config.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  python android-build-validator.py\n  python android-build-validator.py -c configs/prod.json --html"
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{__version__}")
    parser.add_argument("-c", "--config", help="Path to JSON config. Defaults to searching in configs/ folder.")
    parser.add_argument("--html", action="store_true", help="Generate an HTML report in reports/ folder.")
    
    args = parser.parse_args()

    # ADB Connection Check
    adb_check = subprocess.run("adb devices", shell=True, capture_output=True).stdout.decode()
    if adb_check.count('\t') < 1:
        print("❌ Error: No Android device detected via ADB. Please check connection and USB debugging.")
        sys.exit()

    final_config = args.config if args.config else select_config_file("configs")
    run_validator(final_config, args.html)
