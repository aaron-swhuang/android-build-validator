# 📱 Android Build Validator

[繁體中文] | [English](README.md)

這是一個基於 Python 與 ADB (Android Debug Bridge) 的自動化工具，旨在幫助開發者與測試人員快速核對 Android 設備上的系統建置與已安裝應用版本是否符合預期。

---

## 🌟 主要功能

- **自動化版本抓取**：透過 ADB 指令精準獲取應用程式的 `versionName`。
- **多專案管理**：支援從 `configs/` 資料夾自動讀取多組 JSON 設定檔。
- **智慧選單**：若存在多個設定檔，提供互動式選單方便切換。
- **HTML 視覺化報告**：一鍵生成美觀的報表，並自動歸類至 `reports/` 資料夾。
- **靈活參數支援**：支援 `-c` 參數指定路徑，以及 `-h` 查看完整說明。

---

## 🛠️ 環境需求

1. **Python 3.6+**
2. **Android SDK Platform-Tools**：確保系統環境變數中包含 `adb`。
3. **USB 除錯模式**：手機須連線並授權電腦進行 ADB 除錯。

---

## 📂 專案目錄結構

```text
.
├── android-build-validator.py # 主程式
├── README.md                  # 本說明文件
├── configs/                   # [建議] 存放各專案的 JSON 設定檔
│   ├── project_A.json
│   └── project_B.json
└── reports/                   # [自動生成] 存放產出的 HTML 報表

```

---

## ⚙️ 設定檔範例 (JSON)

請確保您的 `.json` 檔案放置於 `configs/` 目錄下（或自定義路徑），格式如下：

```json
{
  "project_name": "核心系統測試專案",
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
    },
    {
      "name": "測試用 App",
      "package_name": "com.example.testapp",
      "version": "1.0.5"
    }
  ]
}

```

---

## 💻 使用說明 (Usage)

### 1. 顯示說明文件

查看所有可用的參數選項：

```bash
python android-build-validator.py --help
python android-build-validator.py --version

```

### 2. 啟動互動模式 (預設)

程式會檢查 `configs/` 資料夾。若有多個檔案，請輸入編號選擇：

```bash
python android-build-validator.py

```

### 3. 產出 HTML 報告

執行完畢後，報表將自動儲存於 `./reports/` 資料夾中：

```bash
python android-build-validator.py --html

```

### 4. 指定特定設定檔與路徑

```bash
python android-build-validator.py -c ./custom_folder/my_config.json --html

```

---

## 📊 報告狀態解析

| 狀態 (Status) | 顏色 (HTML) | 說明 |
| --- | --- | --- |
| **✅ Pass** | 綠色 | 安裝版本與預期設定完全符合。 |
| **⚠️ Mismatch** | 黃色 | 設備已安裝該應用，但版本號不符。 |
| **❌ Not Installed** | 紅色 | 在設備中找不到指定的 Package Name。 |

---

## ⚠️ 注意事項

1. **設備連線**：執行前請先確保 `adb devices` 指令能看到您的設備。若同時連接多台設備，腳本將針對預設裝置執行。
2. **編碼格式**：JSON 設定檔建議使用 `UTF-8` 編碼，以避免應用程式名稱出現亂碼。
3. **路徑權限**：在 Windows 系統下若無權限建立資料夾，請嘗試以管理員權限執行終端機。
4. **ADB 授權**：若手機彈出「允許 USB 除錯嗎？」的視窗，請務必點選「允許」。
