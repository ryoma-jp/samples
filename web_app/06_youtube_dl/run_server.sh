#! /bin/bash

# --- download images ---
IMAGE_DIR="media/images"
if [ -e ${IMAGE_DIR} ]; then
	echo "--- Skip Download Images (Images are already exist) ---"
else
	echo "--- Download Images ---"
	docker-compose run web /code/tools/prepare_images/run.sh --dataset kitti --dataset_dir /code/tools/prepare_images/download/ --image_dir /code/media/images/ --log /tmp/prepare_images.log
	STAT_BUILD=$?
	echo ${STAT_BUILD}
	if [ ! ${STAT_BUILD} -eq 0 ]; then
		echo "[ERROR] Failed to download images: (exit-status = ${STAT_BUILD})"
		exit
	fi
	echo "--- Download Images DONE ---"
fi

# --- create local_settings.py ---
echo "--- Create local_settings.py ---"
docker-compose run web python tools/create_local_settings/create_local_settings.py --output_file djangoproject/local_settings.py
STAT_BUILD=$?
echo ${STAT_BUILD}
if [ ! ${STAT_BUILD} -eq 0 ]; then
	echo "[ERROR] Failed to create local_settings.py: (exit-status = ${STAT_BUILD})"
	exit
fi
echo "--- Create local_settings.py DONE ---"

# --- check database file ---
if [ -e "db.sqlite3" ]; then
	DB_NOT_EXIST=false
else
	DB_NOT_EXIST=true
fi
echo "DB_NOT_EXIST=${DB_NOT_EXIST}"

# --- run server ---
echo "--- Run Server ---"
docker-compose up -d
STAT_BUILD=$?
if [ ! ${STAT_BUILD} -eq 0 ]; then
	echo "[ERROR] \"docker-compose up -d\" is failed: (exit-status = ${STAT_BUILD})"
	exit
fi
echo "--- Run Server DONE ---"

# --- migration ---
echo "--- Database Migration ---"
docker-compose exec web python manage.py makemigrations app
STAT_BUILD=$?
if [ ! ${STAT_BUILD} -eq 0 ]; then
	echo "[ERROR] \"docker-compose exec web python manage.py makemigrations app\" is failed: (exit-status = ${STAT_BUILD})"
	exit
fi

docker-compose exec web python manage.py migrate
STAT_BUILD=$?
if [ ! ${STAT_BUILD} -eq 0 ]; then
	echo "[ERROR] \"docker-compose exec web python manage.py migrate\" is failed: (exit-status = ${STAT_BUILD})"
	exit
fi
echo "--- Database Migration DONE ---"

# --- create superuser (for debug)
#   パスワードは00-generate_init_password.shで自動生成する
#   データベース未作成時のみ実行する
if "${DB_NOT_EXIST}"; then
	echo "--- Create Superuser ---"
	docker-compose exec web python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'mXlBZn1bEe')"
	STAT_BUILD=$?
	if [ ! ${STAT_BUILD} -eq 0 ]; then
		echo "[ERROR] createsuperuser is failed: (exit-status = ${STAT_BUILD})"
		exit
	fi
	echo "--- Create Superuser DONE ---"
fi

# --- show containers ---
docker-compose ps
