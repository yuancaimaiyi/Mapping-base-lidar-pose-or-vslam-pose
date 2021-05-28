
DATASET_PATH=/media/orieange/8532225d-1d86-4a79-88ce-3e9b38ee5d8a/3D/colmap/wayz_data
COLMAP=/media/orieange/8532225d-1d86-4a79-88ce-3e9b38ee5d8a/3D/colmap/build/src/exe/colmap 
GPU_IDX=0

### fix position ,optimzie rotation

if [ ! -d $DATASET_PATH/sparse ]
then
    mkdir $DATASET_PATH/sparse
fi
if [ ! -d $DATASET_PATH/sparse_BA ]
then
    mkdir $DATASET_PATH/sparse_BA
fi


$COLMAP point_triangulator \
    --database_path $DATASET_PATH/colmap_db_camera4253.db \
    --image_path  $DATASET_PATH \
    --input_path $DATASET_PATH/model\
    --output_path $DATASET_PATH/sparse
    
######## t to C
if [ ! -d $DATASET_PATH/sparse_txt ]
then
    mkdir $DATASET_PATH/sparse_txt
fi

if [ ! -d $DATASET_PATH/sparse_txt_txt ]
then
    mkdir $DATASET_PATH/sparse_txt_txt
fi

echo "....start trans t to C ...."
$COLMAP model_converter \
    --input_path $DATASET_PATH/sparse \
    --output_path $DATASET_PATH/sparse_txt \
    --output_type TXT
cp -r $DATASET_PATH/sparse_txt/cameras.txt $DATASET_PATH/sparse_txt/points3D.txt $DATASET_PATH/sparse_txt_txt
python3 $DATASET_PATH/trans.py \
    --input_path $DATASET_PATH/sparse_txt/images.txt \
    --output_path $DATASET_PATH/sparse_txt_txt \
    --flag 1
echo " .....tans t to C done..... "
$COLMAP bundle_adjuster  --input_path $DATASET_PATH/sparse_txt_txt --output_path $DATASET_PATH/sparse_BA --BundleAdjustment.function_tolerance 0.0001 --BundleAdjustment.refine_focal_length 0 --BundleAdjustment.refine_extra_params 0  
############ C to t
if [ ! -d $DATASET_PATH/sparse_BA_txt ]
then
    mkdir $DATASET_PATH/sparse_BA_txt
fi 

if [ ! -d $DATASET_PATH/sparse_BA_txt_txt ]
then
    mkdir $DATASET_PATH/sparse_BA_txt_txt
fi 
echo "start trans C to t"
$COLMAP model_converter \
    --input_path $DATASET_PATH/sparse_BA \
    --output_path $DATASET_PATH/sparse_BA_txt \
    --output_type TXT

cp -r $DATASET_PATH/sparse_BA_txt/cameras.txt $DATASET_PATH/sparse_BA_txt/points3D.txt $DATASET_PATH/sparse_BA_txt_txt
python3 $DATASET_PATH/trans.py \
    --input_path $DATASET_PATH/sparse_BA_txt/images.txt \
    --output_path $DATASET_PATH/sparse_BA_txt_txt \
    --flag 0
if [ ! -d $DATASET_PATH/sparse_BA_txt_txt_last ]
then
    mkdir $DATASET_PATH/sparse_BA_txt_txt_last
fi 
$COLMAP point_triangulator \
    --database_path $DATASET_PATH/colmap_db_camera4253.db \
    --image_path  $DATASET_PATH \
    --input_path $DATASET_PATH/sparse_BA_txt_txt\
    --output_path $DATASET_PATH/sparse_BA_txt_txt_last
################### sparse_BA_txt_txt is final result



