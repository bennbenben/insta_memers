#!/usr/bin/env bash
# Summary: this application uploads images to imgur based on specified album

var_date_time=$(date -d 'now' +%Y%m%d_%H%M)
proj_m4m_folder='C:\Users\bennb\Projects\m4m'
scripts_folder=$proj_m4m_folder'\scripts'
upload_folder=$proj_m4m_folder'\upload'



# Application start
cd /mnt/c/Users/bennb/Projects/m4m/scripts/
# python.exe app_upload.py $scripts_folder'\auth.ini' $upload_folder 'memes'
python.exe app_upload.py $scripts_folder'\auth.ini' $upload_folder 'm4m'
