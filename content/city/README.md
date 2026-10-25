# 城市·摄影作品存放处

把照片放进对应城市文件夹，然后重跑 `python3 tools/build_city.py` 即可上线：

- `beijing/` 北京
- `shanghai/` 上海
- `wuhan/` 武汉

支持 jpg / jpeg / png / webp，按文件名排序展示。
如需给某张照片配说明文字，在同目录放 `captions.json`：
{"文件名.jpg": "说明文字"}
