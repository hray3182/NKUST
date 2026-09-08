# NKUST 課程與作業

受 [panpan](https://github.com/pan93412/nkust-homework) 啟發，所以也把一些在學校完成的東西整理上來。

目錄依學年、學期及課程分類，例如 `3rd-1` 為三年級上學期、`3rd-2` 為三年級下學期。保留既有課程路徑，避免破壞作業中的相對路徑。

## 取得專案

```sh
git clone --recurse-submodules git@github.com:hray3182/NKUST.git
```

既有 checkout 同步主專案後，執行 `git submodule update --init --recursive`，取得主專案指定的子模組版本。

## Python 環境

`.venv/` 保留在各課程的本機目錄，不納入 Git。依賴設定與 `uv.lock` 納入版本控制；不要把虛擬環境複製到其他機器。

有 `pyproject.toml` 和 `uv.lock` 的課程，進入該目錄執行：

```sh
uv sync --locked
```

只有 `requirements.txt` 的課程，進入該目錄執行：

```sh
uv venv --python 3.12
uv pip install -r requirements.txt
```

- `3rd-1/data_compress/requirements.txt`：涵蓋 `hw2` 與 `final`；可在作業目錄建立環境後以 `uv pip install -r ../requirements.txt` 安裝。
- `3rd-1/python_app/homework/python_trade/src`：使用此目錄的 `pyproject.toml` 與 `uv.lock`。
- `3rd-2/deep_learning`：共用的 Keras / TensorFlow 環境，供 `0528_in_class` 使用；執行 `uv run --locked python 0528_in_class/main.py`。
- `3rd-2/deep_learning/0325_in_class`、`0521_in_class`：各自使用該目錄的環境設定。
- `3rd-2/deep_learning/week7`：使用該目錄的 `requirements.txt` 建立 PyTorch 環境。

鎖檔固定解析出的套件版本；GPU 驅動、外部資料及課程程式的執行仍需按各課程需求準備。既有程式未因整理而修改，也未重新執行完整模型訓練。

## 本機資料與成果

程式碼、課堂筆記、報告與小型成果圖片納入 Git。以下檔案保留本機並由 `.gitignore` 排除：

- Python 虛擬環境、快取、編譯產物。
- gaze detection 的作業 ZIP、MediaPipe 模型、`output_features/` 和訓練產生的 `.pkl`；模型下載及特徵生成方式見該課程 README。
- deep learning week7 的作業 ZIP 與 `cats_and_dogs_small/`。需自行準備資料集，目錄為 `{train,validation,test}/{cats,dogs}/`。

排除 Git 不代表刪除本機檔案。報告、評估結果與成果圖片仍保留於版本控制。
