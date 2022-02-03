#!/usr/bin/env bash
# Summary: this application downloads images from a pre-defined library in IMGUR, performs image resizing, and uploads it to another pre-defined IG story
# Steps: 
## 1. Downloads from IMGUR (app_extract.py)
## 2. Local image resizing (app_transform.py)
## 3. Uploads to IG story (app_egress.py)

# Initialize variables
## Key variables
date_time=$(date -d 'now' +%Y%m%d_%M%H)
log=$date_time'.log'
num_of_memes=1

## Folder and file paths
proj_m4m_folder='C:\Users\bennb\Projects\m4m'

scripts_folder=$proj_folder'\scripts'
logs_folder=$proj_folder'\logs'
data_folder=$proj_folder'\data'

extract_data_folder=$data_folder'\extract_'$date_time
transform_data_folder=$data_folder'\transform_'$date_time
egress_data_folder=$data_folder'\egress_'$date_time


# Application start
## Initialize application
echo "[SHELL] $(date +'%Y-%m-%d %H:%M:%S') Application (m4m_app) is starting" > $logs_folder$log
echo "[SHELL] $(date +'%Y-%m-%d %H:%M:%S') Creating all data folders: $extract_data_folder, $transform_data_folder, $egress_data_folder" >> $logs_folder$log
mkdir -p $extract_data_folder $transform_data_folder $egress_data_folder
cd $scripts_folder

## Extract
echo "[SHELL] $(date +'%Y-%m-%d %H:%M:%S') Executing app_extract.py with $num_of_memes memes" >> $logs_folder$log
python.exe app_extract.py $date_time $scripts_folder'\auth.ini' $extract_data_folder $num_of_memes

## Transform
echo "[SHELL] $(date +'%Y-%m-%d %H:%M:%S') Executing app_extract.py with $num_of_memes memes" >> $logs_folder$log
python.exe app_transform.py $date_time ($(ls $extract_data_folder)) $transform_data_folder

## Egress
echo "[SHELL] $(date +'%Y-%m-%d %H:%M:%S') Executing app_extract.py with $num_of_memes memes" >> $logs_folder$log
python.exe app_egress.py $date_time $scripts_folder'\auth.ini' $extract_data_folder $num_of_memes
