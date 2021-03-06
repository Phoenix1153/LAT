python main.py \
  --batchsize 100 \
  --epoch 80 \
  --lr 0.00005 \
  --enable_lat 'False' \
  --test_flag 'False' \
  --adv_flag 'False' \
  --train_data_path "/media/dsg3/dsgprivate/lat/data/sampled_imagenet/" \
  --model_path "/media/dsg3/dsgprivate/yuhang/model/alexnet/eat/" \
  --pro_num 1 \
  --alpha 0 \
  --epsilon 0 \
  --dataset "imagenet" \
  --model "alexnet" \
  --dropout 'True' \
  --test_data_path "/media/dsg3/dsgprivate/lat/sampled_imagenet/test/alexnet/test_data_cln.p" \
  --test_label_path "/media/dsg3/dsgprivate/lat/sampled_imagenet/test/alexnet/test_label.p" \
  --logfile 'log8.txt'
