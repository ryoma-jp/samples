# データ読み込み処理のサンプル

## 概要

* データ読み込み処理のサンプル

## 実行手順

	$ cd docker  
	$ docker build -t data_loader/tensorflow:21.03-tf2-py3 .  
	$ ./docker_run.sh  
	# cd /work  
	# ./run.sh  


## JSON dataset format

```json
{
    "name": "dataset name",
    "root_dir": "<root directory of dataset>",
    "task": "image_classification", (see Task section)
    "metadata": [
        {
            "id": 0,
            "file_path": "<relative path of sample data from root_dir>",
            "annotation": {
                "class_id": 0,
                "class_name": "class name",
            },
        },
        {
            "id": 1,
            "file_path": "<relative path of sample data from root_dir>",
            "annotation": {
                "class_id": 1,
                "class_name": "class name",
            },
        },
        ...
    ],
}
```

### Task

|Name|Description|
|:--|:--|
|image_classification|画像分類<br>annotationにはclass_nameとclass_idを付与する|

# 参考

* [How to load Matlab .mat files in Python](https://towardsdatascience.com/how-to-load-matlab-mat-files-in-python-1f200e1287b5)
* [The SARCOS data](http://www.gaussianprocess.org/gpml/data/)
* [COCO](https://cocodataset.org/#home)
* [Movie Genre Classification based on Poster Images with Deep Neural Networks](https://www.cs.ccu.edu.tw/~wtchu/projects/MoviePoster/index.html)
* [JSON dataset Format](https://support.etlworks.com/hc/en-us/articles/360014078293-JSON-dataset-Format)