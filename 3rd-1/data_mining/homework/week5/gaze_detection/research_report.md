# 基於眼動和頭部姿態的視線追蹤系統技術報告

## 摘要

本研究開發了一個即時視線追蹤系統的概念驗證（Proof of Concept），用於判斷使用者是否正在觀看螢幕。系統結合 MediaPipe 面部特徵檢測與支援向量機（SVM）分類器，在測試集上達到 97.70% 的準確率。透過提取眼睛注視方向和頭部旋轉角度等 11 個特徵，系統能夠在即時視訊串流中預測使用者的注視狀態。目前資料集僅由單一使用者錄製，未來需要收集更多樣化資料以驗證模型的泛化能力。

---

## 1. 研究背景與目的

### 1.1 研究動機

在遠距工作、線上教育和人機互動領域中，準確偵測使用者是否專注於螢幕具有重要應用價值。本系統旨在開發一個基於普通網路攝影機的非侵入式視線追蹤解決方案。

### 1.2 研究目標

- 開發二元分類模型原型（觀看/未觀看螢幕）
- 驗證即時預測的技術可行性
- 提取可解釋的面部特徵，包括眼動和頭部姿態
- 建立資料處理和模型訓練流程
- 為未來大規模資料收集和模型優化奠定基礎

---

## 2. 系統架構

### 2.1 整體架構圖

```
輸入視訊
    ↓
MediaPipe 面部檢測
    ↓
特徵提取（11個特徵）
    ├─ 眼睛注視方向（8個）← 來自 Face Blendshapes
    └─ 頭部旋轉角度（3個）← 來自 Transformation Matrix
    ↓
特徵標準化
    ↓
SVM 分類器
    ↓
預測結果 + 平滑處理
    ↓
輸出（觀看/未觀看）
```

### 2.2 核心模組

#### 1. 特徵提取模組（`extract_features.py`）

**主要功能**：
- 處理視訊檔案，每隔 N 幀提取特徵
- 使用 MediaPipe Face Landmarker 檢測面部
- 提取 blendshapes（眼動特徵）和 transformation matrix（頭部姿態）
- 輸出 CSV 格式的特徵資料集

**核心函數**：
- `extract_features()`: 從單一視訊提取特徵
- `process_dataset()`: 批次處理資料集

#### 2. 模型訓練模組（`train_svm.py`）

**主要功能**：
- 載入並預處理資料（過濾眼睛閉合幀）
- 使用 Grid Search 尋找最佳 SVM 超參數
- 訓練 RBF kernel SVM 模型
- 評估模型並生成報告（混淆矩陣、ROC 曲線等）
- 保存訓練好的模型和 scaler

**核心函數**：
- `load_and_preprocess_data()`: 載入與預處理資料
- `train_svm_with_grid_search()`: 訓練與評估模型

#### 3. 即時預測模組（`realtime_prediction.py`）

**主要功能**：
- 從網路攝影機即時讀取畫面（1280×720）
- 實時提取面部特徵
- 使用訓練好的 SVM 模型進行預測
- 應用移動平均法平滑預測結果
- 顯示視覺化介面（預測結果、機率、頭部角度等）

**核心類別**：
- `GazePredictor`: 即時視線預測器
  - `extract_features()`: 從單幀提取特徵
  - `predict()`: 預測是否觀看螢幕
  - `get_smoothed_prediction()`: 平滑預測結果
  - `draw_ui()`: 繪製使用者介面
  - `run()`: 執行即時預測主迴圈

---

## 3. 特徵工程

### 3.1 特徵選擇

系統提取 **11 個特徵**，分為兩大類：

#### 3.1.1 眼睛注視特徵（8 個）

這些特徵來自 MediaPipe 的 Face Blendshapes，量化眼球在不同方向的移動程度：

| 特徵名稱 | 描述 | 值域 |
|---------|------|------|
| `eyeLookUpLeft` | 左眼向上看的程度 | [0, 1] |
| `eyeLookUpRight` | 右眼向上看的程度 | [0, 1] |
| `eyeLookDownLeft` | 左眼向下看的程度 | [0, 1] |
| `eyeLookDownRight` | 右眼向下看的程度 | [0, 1] |
| `eyeLookInLeft` | 左眼向內（鼻側）看的程度 | [0, 1] |
| `eyeLookInRight` | 右眼向內（鼻側）看的程度 | [0, 1] |
| `eyeLookOutLeft` | 左眼向外（太陽穴側）看的程度 | [0, 1] |
| `eyeLookOutRight` | 右眼向外（太陽穴側）看的程度 | [0, 1] |

**註**：值越接近 1，表示該方向的眼動越明顯；0 表示無該方向的眼動。

#### 3.1.2 頭部旋轉特徵（3 個）

從 MediaPipe 的 4×4 齊次變換矩陣中提取的 Euler 角度（單位：弧度）：

| 特徵名稱 | 描述 | 值域 | 物理意義 |
|---------|------|------|---------|
| `head_pitch` | 俯仰角 | [-π/2, π/2] | 點頭（上下）<br>**正值：低頭**<br>**負值：抬頭** |
| `head_yaw` | 偏航角 | [-π, π] | 轉頭（左右）<br>正值：向右轉<br>負值：向左轉 |
| `head_roll` | 翻滾角 | [-π, π] | 傾斜（左右）<br>正值：向右傾<br>負值：向左傾 |

**註**：角度正負方向由 MediaPipe 座標系統定義，已透過實際測試驗證。

### 3.2 頭部旋轉角度計算原理

#### 3.2.1 為什麼可以使用 Transformation Matrix 計算頭部姿態？

MediaPipe Face Landmarker 提供的 **facial transformation matrix** 是基於 **metric 3D face model** 計算得出的變換矩陣。根據 [MediaPipe 3D Face Transform 官方說明](https://developers.googleblog.com/en/mediapipe-3d-face-transform/)，這個矩陣將標準面部模型（canonical face model）的 3D 座標轉換到相機座標系統中。

**核心概念**：
- MediaPipe 使用預訓練的 3D 面部模型，該模型定義了面部特徵點的標準位置
- 透過檢測影像中的面部特徵點，系統計算出將標準模型對齊到實際面部的變換
- 這個變換包含了**旋轉**（頭部姿態）和**平移**（頭部位置）資訊
- 因此，從變換矩陣中提取旋轉部分，即可得到頭部的 3D 旋轉角度

**應用價值**：
這使得我們無需額外的深度感測器或特殊硬體，僅透過普通 RGB 攝影機就能獲得準確的頭部姿態估計。

#### 3.2.2 Transformation Matrix 結構

MediaPipe 輸出的 facial transformation matrix 是一個 **4×4 齊次變換矩陣**：

$$
\mathbf{T} = \begin{bmatrix}
r_{11} & r_{12} & r_{13} & t_x \\
r_{21} & r_{22} & r_{23} & t_y \\
r_{31} & r_{32} & r_{33} & t_z \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

其中：
- **R**（左上角 3×3）：**旋轉矩陣**，描述頭部相對於相機的旋轉狀態
  $$
  \mathbf{R} = \begin{bmatrix}
  r_{11} & r_{12} & r_{13} \\
  r_{21} & r_{22} & r_{23} \\
  r_{31} & r_{32} & r_{33}
  \end{bmatrix}
  $$
- **t**（右側 3×1）：**平移向量**，描述頭部中心點的 3D 位置
  $$
  \mathbf{t} = \begin{bmatrix} t_x \\ t_y \\ t_z \end{bmatrix}
  $$
- 最後一行 $[0, 0, 0, 1]$：齊次座標標準形式

#### 3.2.3 從旋轉矩陣提取 Euler 角度

從 3×3 旋轉矩陣 $\mathbf{R}$ 中提取 Euler 角度的標準數學公式如下：

**計算三個基礎角度**：

$$
\text{angle}_x = \arctan2\left(-R_{2,0}, \sqrt{R_{2,1}^2 + R_{2,2}^2}\right)
$$

$$
\text{angle}_y = \arctan2(R_{1,0}, R_{0,0})
$$

$$
\text{angle}_z = \arctan2(R_{2,1}, R_{2,2})
$$

**語義映射（基於實際觀察）**：

由於 MediaPipe 的座標系統特性，我們需要根據實際頭部動作與角度變化的對應關係進行映射：

$$
\begin{aligned}
\text{head\_pitch} &= \text{angle}_z \quad \text{（點頭動作：上下）} \\
\text{head\_yaw} &= \text{angle}_x \quad \text{（轉頭動作：左右）} \\
\text{head\_roll} &= \text{angle}_y \quad \text{（傾斜動作：左右）}
\end{aligned}
$$

#### 3.2.4 實作細節

實際程式碼實作：

```python
# Extract head rotation from transformation matrix (pitch, yaw, roll)
if detection_result.facial_transformation_matrixes:
    # Get the 4x4 transformation matrix
    matrix = np.array(detection_result.facial_transformation_matrixes[0]).reshape(4, 4)

    # Extract rotation angles from rotation matrix (top-left 3x3)
    R = matrix[:3, :3]

    # Calculate Euler angles in radians
    # Based on observation:
    # - Nodding up/down should be PITCH
    # - Turning left/right should be YAW
    # - Tilting side to side should be ROLL
    angle_x = np.arctan2(-R[2, 0], np.sqrt(R[2, 1]**2 + R[2, 2]**2))
    angle_y = np.arctan2(R[1, 0], R[0, 0])
    angle_z = np.arctan2(R[2, 1], R[2, 2])

    # Map to correct semantic names based on observed behavior:
    # angle_z was moving when nodding → this is pitch
    # angle_x was moving when turning left/right → this is yaw
    # angle_y was moving when tilting → this is roll
    row_data['head_pitch'] = angle_z  # Nodding up/down
    row_data['head_yaw'] = angle_x    # Turning left/right
    row_data['head_roll'] = angle_y   # Tilting side to side
```

**註**：角度映射是根據實際觀察到的頭部動作與角度變化的對應關係調整的，以確保語義正確性。

### 3.3 眼睛閉合檢測

系統額外使用兩個 blendshape 特徵來檢測眼睛是否閉合：

- `eyeBlinkLeft`：左眼閉合程度
- `eyeBlinkRight`：右眼閉合程度

當任一眼睛的 blink 值超過閾值（預設 0.5）時，系統判定為「眼睛閉合」狀態，此時不進行視線預測。

---

## 4. 資料集與處理

### 4.1 資料集結構

```
dataset/
├── yes/        # 觀看螢幕的視訊
│   ├── video1.mp4
│   ├── video2.mp4
│   └── ...
└── no/         # 未觀看螢幕的視訊
    ├── video1.mp4
    ├── video2.mp4
    └── ...
```

### 4.2 資料處理流程

實作於 `extract_features.py`，處理流程如下：

1. **幀採樣**：每隔 5 幀提取一次特徵（`frame_interval=5`），降低運算負擔
2. **特徵提取**：
   - 使用 MediaPipe Face Landmarker 檢測面部
   - 提取 8 個眼睛注視特徵（blendshapes）
   - 提取 2 個眼睛閉合特徵（用於過濾）
   - 計算 3 個頭部旋轉角度（從 transformation matrix）
3. **資料標記**：根據視訊來源資料夾自動標記為 "yes" 或 "no"
4. **資料過濾**：濾除眼睛閉合的幀（`eyeBlink > 0.5`）
5. **資料合併**：將所有視訊的特徵合併為單一 CSV 檔案

### 4.3 資料集統計

經過處理和過濾後的資料集統計：

- **總樣本數**：4,125 個樣本（過濾眼睛閉合後）
- **訓練集**：3,300 個樣本（80%）
  - Yes（觀看螢幕）：約 1,980 個（60%）
  - No（未觀看螢幕）：約 1,320 個（40%）
- **測試集**：825 個樣本（20%）
  - Yes（觀看螢幕）：495 個（60%）
  - No（未觀看螢幕）：330 個（40%）
- **特徵數量**：11 個（8 個眼動 + 3 個頭部旋轉）

### 4.4 輸出格式

```csv
video_path,label,frame_number,timestamp,eyeLookUpLeft,eyeLookUpRight,...,head_pitch,head_yaw,head_roll
dataset/yes/video1.mp4,yes,0,0.0,0.123,0.234,...,0.056,-0.023,0.012
dataset/yes/video1.mp4,yes,5,0.167,0.145,0.256,...,0.067,-0.034,0.015
...
```

---

## 5. 模型訓練與優化

### 5.1 演算法選擇

選用 **Support Vector Machine (SVM)** 作為分類器，理由如下：

- 在中小型資料集上表現優異
- 對高維特徵空間有良好的泛化能力
- RBF kernel 能處理非線性決策邊界
- 訓練速度快，適合即時應用

### 5.2 超參數調整

使用 **Grid Search with Cross-Validation** 尋找最佳參數組合：

#### 搜尋空間

```python
param_grid = {
    'C': [0.1, 1, 10, 100, 1000],
    'gamma': [0.001, 0.01, 0.1, 1, 'scale', 'auto']
}

svm = SVC(kernel='rbf', random_state=42, probability=True)
grid_search = GridSearchCV(
    svm,
    param_grid,
    cv=5,  # 5-fold cross-validation
    scoring='accuracy',
    n_jobs=-1
)
```

**參數說明**：
- **C**：正則化參數，控制誤分類的懲罰程度（值越大，懲罰越重）
- **gamma**：RBF kernel 參數，控制單一訓練樣本的影響範圍（值越大，影響範圍越小）

#### 交叉驗證策略

採用 **5-fold Cross-Validation**，將訓練集分為 5 個子集，每次用 4 個子集訓練、1 個子集驗證，確保模型泛化能力。

### 5.3 最佳參數

根據 Grid Search 結果（共測試 30 組參數組合），前 10 名參數組合為：

| 排名 | C | gamma | 平均準確率 | 標準差 |
|------|---|-------|-----------|--------|
| 1 | 1000 | 1 | 0.9842 | ±0.0028 |
| 1 | 100 | 1 | 0.9842 | ±0.0028 |
| 3 | 100 | auto | 0.9839 | ±0.0015 |
| 3 | 100 | scale | 0.9839 | ±0.0015 |
| 3 | 100 | 0.1 | 0.9839 | ±0.0012 |
| 6 | 10 | 1 | 0.9836 | ±0.0024 |
| 7 | 1 | 1 | 0.9830 | ±0.0024 |
| 8 | 1000 | 0.1 | 0.9809 | ±0.0015 |
| 9 | 1000 | scale | 0.9803 | ±0.0010 |
| 10 | 1000 | auto | 0.9800 | ±0.0015 |

**最終選擇**：`C=100, gamma=1`

**選擇理由**：
- 與 `C=1000, gamma=1` 具有相同的準確率（0.9842）
- 較小的 C 值意味著較低的模型複雜度，有助於避免過度擬合
- 考慮模型複雜度與穩定性的平衡

---

## 6. 模型評估

### 6.1 資料集劃分

- **訓練集**：3,300 個樣本（80%）
- **測試集**：825 個樣本（20%）
- **劃分方式**：Stratified sampling，確保兩類別比例一致
- **隨機種子**：42（確保可重現性）

### 6.2 測試集表現

在獨立測試集（825 個樣本）上的評估結果：

| 指標 | 數值 | 說明 |
|------|------|------|
| **Accuracy（準確率）** | 97.70% | 正確分類的樣本比例 |
| **Precision（精確率）** | 97.98% | 預測為「觀看」中真正觀看的比例 |
| **Recall（召回率）** | 98.18% | 實際觀看中被正確預測的比例 |
| **F1 Score** | 98.08% | Precision 和 Recall 的調和平均 |
| **AUC** | 99.64% | ROC 曲線下面積，衡量分類能力 |

### 6.3 混淆矩陣

|  | 預測 No | 預測 Yes |
|---|---:|---:|
| **實際 No** | 320 | 10 |
| **實際 Yes** | 9 | 486 |

**矩陣解讀**：
- **True Negative (TN)**: 320 - 正確識別「未觀看螢幕」
- **False Positive (FP)**: 10 - 實際未觀看，但誤判為「觀看」
- **False Negative (FN)**: 9 - 實際觀看，但誤判為「未觀看」
- **True Positive (TP)**: 486 - 正確識別「觀看螢幕」

**錯誤率分析**：
- **Type I Error（False Positive Rate）**: $\frac{10}{330} = 3.03\%$
- **Type II Error（False Negative Rate）**: $\frac{9}{495} = 1.82\%$
- **總錯誤樣本**：19 個（10 + 9），總錯誤率為 $\frac{19}{825} = 2.30\%$

### 6.4 分類報告

| 類別 | Precision | Recall | F1-Score | Support |
|---|---:|---:|---:|---:|
| **No** | 0.97 | 0.97 | 0.97 | 330 |
| **Yes** | 0.98 | 0.98 | 0.98 | 495 |
| **Accuracy** | | | 0.98 | 825 |
| **Macro avg** | 0.98 | 0.98 | 0.98 | 825 |
| **Weighted avg** | 0.98 | 0.98 | 0.98 | 825 |

**類別分析**：
- **No（未觀看螢幕）**：330 個樣本（40%）
  - Precision: 0.97（預測為 No 的樣本中，97% 確實是 No）
  - Recall: 0.97（實際 No 樣本中，97% 被正確識別）
  - F1-score: 0.97

- **Yes（觀看螢幕）**：495 個樣本（60%）
  - Precision: 0.98（預測為 Yes 的樣本中，98% 確實是 Yes）
  - Recall: 0.98（實際 Yes 樣本中，98% 被正確識別）
  - F1-score: 0.98

**觀察**：
- 兩類別的表現均衡，無明顯偏差
- \"Yes\" 類別的 precision 和 recall 略高於 \"No\"，可能因為訓練樣本較多
- Macro average 和 weighted average 皆為 0.98，表示模型在兩類別上都有優異表現

### 6.5 ROC 曲線與 AUC

- **AUC = 0.9964**：模型具有極佳的分類能力（接近完美的 1.0）
- ROC 曲線接近左上角，表示在各種閾值下都能保持高 True Positive Rate 與低 False Positive Rate
- AUC > 0.99 表示模型能非常有效地區分「觀看」與「未觀看」兩種狀態

**AUC 解讀**：
- AUC = 0.5：隨機猜測
- AUC = 0.7-0.8：可接受
- AUC = 0.8-0.9：良好
- **AUC = 0.9964：優異**（本模型）

---

## 7. 即時預測系統

### 7.1 系統功能

1. **即時視訊處理**：從網路攝影機讀取畫面（1280×720 解析度）
2. **面部檢測**：使用 MediaPipe Face Landmarker
3. **特徵提取**：實時計算 11 個特徵
4. **預測與平滑**：使用滑動平均（window size = 10）減少預測抖動
5. **視覺化介面**：顯示預測結果、機率、頭部旋轉角度等資訊

### 7.2 使用者介面元素

- **狀態指示**：
  - 綠色 "WATCHING SCREEN"：使用者正在觀看
  - 紅色 "NOT WATCHING"：使用者未觀看
  - 灰色 "EYES CLOSED"：偵測到眼睛閉合

- **機率條**：顯示「觀看」與「未觀看」的預測機率

- **頭部旋轉角度**（角度單位）：
  - Yaw: 左右轉頭角度
  - Pitch: 上下點頭角度
  - Roll: 左右傾斜角度

- **快捷鍵**：
  - `q`：退出程式
  - `s`：截圖保存
  - `r`：重置預測歷史

### 7.3 預測平滑機制

為避免單幀誤判導致的結果抖動，系統採用 **移動平均法**：

```python
def get_smoothed_prediction(self, prediction):
    """
    Apply moving average to smooth predictions.

    Args:
        prediction: Current prediction (0 or 1)

    Returns:
        smoothed_prediction: Smoothed prediction
    """
    self.prediction_history.append(prediction)

    # Return majority vote
    if len(self.prediction_history) == 0:
        return prediction

    avg = np.mean(self.prediction_history)
    return 1 if avg >= 0.5 else 0
```

**機制說明**：
- 使用 `deque(maxlen=10)` 儲存最近 10 次預測結果
- 計算這 10 次預測的平均值
- 若平均值 ≥ 0.5，則最終預測為「觀看」；否則為「未觀看」
- 此機制能有效提升使用者體驗，減少畫面閃爍

---

## 8. 技術挑戰與解決方案

### 8.1 特徵工程挑戰

**問題**：MediaPipe 提供的 transformation matrix 文檔不完整，角度映射不明確。

**解決方案**：
1. 實際測試各種頭部動作（點頭、轉頭、傾斜）
2. 觀察哪個計算出的角度與實際動作對應
3. 根據觀察結果重新映射角度語義：
   - `angle_z` → `pitch`（點頭時變化）
   - `angle_x` → `yaw`（轉頭時變化）
   - `angle_y` → `roll`（傾斜時變化）

### 8.2 即時性能表現

**觀察**：MediaPipe 面部檢測在普通硬體上表現優異，即使在 1280×720 解析度下也能保持流暢運行。

**系統配置**：
- 解析度：1280×720（平衡畫質與效能）
- 檢測設定：`num_faces=1`（單人檢測）
- 效能：在一般 CPU 上即可達到流暢即時的處理速度（無需 GPU）

**結論**：MediaPipe 的優化使其適合即時應用，不構成性能瓶頸。

### 8.3 光線與角度變化

**問題**：不同光線條件和極端頭部角度會影響檢測準確性。

**解決方案**：
- 訓練資料涵蓋多種場景
- 使用標準化處理特徵
- 設定眼睛閉合檢測避免無效幀

---

## 9. 實驗結果分析

### 9.1 初步結果分析

在當前有限資料集上的表現：

1. **測試準確率**：97.70%
2. **低誤報率**：False Positive Rate 為 3.03%
3. **AUC**：0.9964，顯示模型在當前資料集上具有良好的區分能力
4. **即時性**：能在普通網路攝影機上實現流暢運行

**重要提醒**：由於資料集僅來自單一使用者，上述結果主要反映模型在特定條件下的表現，泛化能力有待進一步驗證。

### 9.2 與相關研究比較

**註**：本節待補充。完整的比較分析需要在相同的測試環境和資料集上進行實驗，才能公正評估不同方法的性能差異。

**本研究成果**：
- 方法：MediaPipe + SVM
- 準確率：97.70%
- 優勢：基於普通網路攝影機，無需專用硬體

---

## 10. 應用場景

### 10.1 線上教育

- 監測學生是否專注聽課
- 提供專注度報告給教師
- 自動暫停視訊當學生分心

### 10.2 遠距工作

- 協助管理注意力
- 統計螢幕使用時間
- 提醒用戶休息（長時間未看螢幕）

### 10.3 駕駛安全

- 偵測駕駛是否注視前方
- 疲勞駕駛警告
- 分心預警系統

### 10.4 人機互動

- 智慧型裝置自動喚醒/休眠
- 基於注視的內容推薦
- 無接觸式介面控制

---

## 11. 限制與未來改進

### 11.1 當前限制

1. **單一使用者**：目前僅支援單人檢測
2. **正面角度**：極端側臉角度（yaw > 60°）準確率下降
3. **光線依賴**：昏暗環境下 MediaPipe 檢測可能失效
4. **二元分類**：無法區分「看螢幕不同區域」

### 11.2 改進方向

**擴充資料集以提升泛化能力**：
- **當前限制**：資料集僅由單一使用者錄製，可能導致模型過度擬合特定個體的面部特徵和行為模式
- **改進方案**：
  - 收集多位不同年齡、性別、種族的使用者資料
  - 涵蓋不同光線條件（自然光、室內光、昏暗環境）
  - 包含不同姿勢和距離的場景
  - 增加配戴眼鏡、不同髮型等變異因素
- **預期效果**：提升模型對未見過使用者的預測準確性，增強實際應用的穩健性

---

## 12. 結論與未來工作

本研究開發了一個基於眼動和頭部姿態的視線追蹤系統概念驗證（Proof of Concept），目前在有限資料集上取得以下成果：

1. **技術實作**：
   - 採用有效的特徵組合（8 個眼動特徵 + 3 個頭部旋轉角度）
   - 解決 MediaPipe transformation matrix 的角度映射問題，透過實際觀察驗證語義正確性
   - 在測試集上達到 97.70% 的準確率，AUC 為 0.9964

2. **實用性**：
   - 無需專用硬體，僅需普通網路攝影機
   - MediaPipe 在一般 CPU 上即可流暢運行
   - 開源實作，易於復現與擴展

3. **技術特點**：
   - 結合 blendshapes 與 transformation matrix 的混合特徵
   - 驗證了頭部姿態在視線追蹤中的重要性
   - 使用移動平均法平滑預測，提升使用者體驗

**當前限制**：
本系統仍處於早期開發階段（Work in Progress），主要限制為資料集僅由單一使用者錄製，模型的泛化能力尚未充分驗證。

**未來工作**：
- **首要任務**：收集多樣化資料集（不同使用者、光線條件、環境）以驗證和提升模型泛化能力
- 在更大規模資料集上重新訓練和評估模型
- 進行跨使用者測試以評估實際應用可行性
- 探索更多應用場景（教育、安全、健康等領域）

---

## 參考文獻

1. Google for Developers. "MediaPipe 3D Face Transform." *Google Developers Blog*. https://developers.googleblog.com/en/mediapipe-3d-face-transform/
2. MediaPipe Face Landmarker Documentation. Google AI. https://developers.google.com/mediapipe/solutions/vision/face_landmarker
3. Transformation Matrix and Euler Angles. https://en.wikipedia.org/wiki/Euler_angles
4. Support Vector Machines. Scikit-learn Documentation. https://scikit-learn.org/stable/modules/svm.html
5. Rotation Matrix to Euler Angles. https://en.wikipedia.org/wiki/Rotation_matrix

---

## 附錄

### A. 完整特徵列表

```python
features = [
    'eyeLookUpLeft', 'eyeLookUpRight',
    'eyeLookDownLeft', 'eyeLookDownRight',
    'eyeLookInLeft', 'eyeLookInRight',
    'eyeLookOutLeft', 'eyeLookOutRight',
    'head_pitch', 'head_yaw', 'head_roll'
]
```

### B. 系統需求

- Python 3.8+
- MediaPipe 0.10.0+
- OpenCV 4.5+
- scikit-learn 1.0+
- NumPy, Pandas

### C. 訓練指令範例

```bash
# 特徵提取
python extract_features.py

# 模型訓練（需要 train_svm.py）
python train_svm.py

# 即時預測
python realtime_prediction.py
```

