# 📱 Android APK Version Validator

[English] | [繁體中文](README.zh-TW.md)

A Python-based utility to verify installed APK versions on Android devices against expected versions using ADB.

---

## 🌟 Key Features

- **Automated Version Check**: Retrieves `versionName` directly from the device via ADB.
- **Project Management**: Supports multiple JSON configurations within the `configs/` directory.
- **Interactive CLI**: Automatically detects config files and provides a selection menu.
- **Visual HTML Reports**: Generate stylized reports saved automatically in the `reports/` folder.
- **Auto-Initialization**: Automatically creates directories and example configs on the first run.

---

## 🛠️ Prerequisites

1. **Python 3.6+**
2. **Android SDK Platform-Tools**: Ensure `adb` is in your system's PATH.
3. **USB Debugging**: The Android device must have USB Debugging enabled and authorized.

---

## 📂 Project Structure

```text
.
├── apk_version_validator.py   # Main Script
├── README.md                 # Documentation
├── configs/                  # Directory for JSON configurations
│   └── example_config.json   # Generated on first run
└── reports/                  # Directory for generated HTML reports

```

---

## ⚙️ Configuration Format (JSON)

Ensure your `.json` files follow this structure:

```json
{
  "project_name": "My QA Project",
  "apps_to_check": [
    {
      "name": "YouTube",
      "package_name": "com.google.android.youtube",
      "version": "19.01.33"
    }
  ]
}

```

---

## 💻 Usage

### 1. View Help and Version

```bash
python apk_version_validator.py --help
python apk_version_validator.py --version

```

### 2. Standard Interactive Mode

Searches for files in `configs/` and lets you choose:

```bash
python apk_version_validator.py

```

### 3. Generate HTML Report

```bash
python apk_version_validator.py --html

```

### 4. Specify Custom Config Path

```bash
python apk_version_validator.py -c ./my_custom_setup.json --html

```

---

## 📊 Status Reference

| Status | Meaning |
| --- | --- |
| **✅ Pass** | Installed version matches the config exactly. |
| **⚠️ Mismatch** | App is installed but version differs from config. |
| **❌ Not Installed** | Package name could not be found on the device. |

---

## ⚠️ Notes

* **Device Connection**: Run `adb devices` to ensure your device is recognized before starting.
* **Multi-Device**: If multiple devices are connected, the script targets the default ADB device.
* **Permissions**: Ensure you have write permissions for the script directory to allow folder creation.