#!/usr/bin/env bash
# Summary: this application downloads images from a pre-defined library in IMGUR, performs image resizing, and uploads it to another pre-defined IG story
# Steps: 
## 1. Downloads from IMGUR (app_extract.py)
## 2. Local image resizing (app_transform.py)
## 3. Uploads to IG story (app_egress.py)

# Initialize variables
## Key variables
var_date_time=$(date -d 'now' +%Y%m%d_%H%M)
log=$date_time'.log'
num_of_memes=1

## Folder and file paths
var_date=$(date -d 'now' +%Y%m%d)
proj_m4m_folder='C:\Users\bennb\Projects\m4m'
scripts_folder=$proj_m4m_folder'\scripts'
logs_folder=$proj_m4m_folder'\logs'
data_folder=$proj_m4m_folder'\data'

extract_data_folder=$data_folder'\extract_'$var_date
transform_data_folder=$data_folder'\transform_'$var_date
egress_data_folder=$data_folder'\egress_'$var_date


# Application start
## Initialize application
#echo "[SHELL] $(date +'%Y-%m-%d %H:%M:%S') Application (m4m_app) is starting" > $logs_folder$log
#echo "[SHELL] $(date +'%Y-%m-%d %H:%M:%S') Creating all data folders: $extract_data_folder, $transform_data_folder, $egress_data_folder" >> $logs_folder$log
cd /mnt/c/Users/bennb/Projects/m4m/scripts/

## Extract
#echo "[SHELL] $(date +'%Y-%m-%d %H:%M:%S') Executing app_extract.py with $num_of_memes memes" >> $logs_folder$log
python.exe app_extract.py $var_date_time $scripts_folder'\auth.ini' $extract_data_folder $num_of_memes

## Transform
#echo "[SHELL] $(date +'%Y-%m-%d %H:%M:%S') Executing app_extract.py with $num_of_memes memes" >> $logs_folder$log
python.exe app_transform.py $var_date_time $extract_data_folder $transform_data_folder

## Egress
#echo "[SHELL] $(date +'%Y-%m-%d %H:%M:%S') Executing app_extract.py with $num_of_memes memes" >> $logs_folder$log
python.exe app_egress.py $transform_data_folder
