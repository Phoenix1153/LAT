python main.py \
  --batchsize 128 \
  --epoch 30 \
  --lr 0.001 \
  --enable_lat 'True' \
  --test_flag 'False' \
  --train_data_path "/media/dsg3/dsgprivate/lat/data/sampled_imagenet/" \
  --model_path "/media/dsg3/dsgprivate/yuhang/model/resnet18/new_plat/" \
  --pro_num 1 \
  --alpha 0 \
  --epsilon 0 \
  --dataset "imagenet" \
  --model "resnet" \
  --dropout 'True' \
  --test_data_path "/media/dsg3/dsgprivate/lat/sampled_imagenet/test/alexnet/test_adv(eps_0.031).p" \
  --test_label_path "/media/dsg3/dsgprivate/lat/sampled_imagenet/test/alexnet/test_label.p" \
  --logfile './log_newplat/newplat1.txt' 
python main.py \
  --batchsize 128 \
  --epoch 20 \
  --lr 0.0005 \
  --enable_lat 'True' \
  --test_flag 'False' \
  --train_data_path "/media/dsg3/dsgprivate/lat/data/sampled_imagenet/" \
  --model_path "/media/dsg3/dsgprivate/yuhang/model/resnet18/new_plat/" \
  --pro_num 3 \
  --alpha 0 \
  --epsilon 1.0 \
  --dataset "imagenet" \
  --model "resnet" \
  --dropout 'True' \
  --test_data_path "/media/dsg3/dsgprivate/lat/sampled_imagenet/test/alexnet/test_adv(eps_0.031).p" \
  --test_label_path "/media/dsg3/dsgprivate/lat/sampled_imagenet/test/alexnet/test_label.p" \
  --logfile './log_newplat/newplat2.txt' 
python main.py \
  --batchsize 128 \
  --epoch 50 \
  --lr 0.0005 \
  --enable_lat 'True' \
  --test_flag 'False' \
  --train_data_path "/media/dsg3/dsgprivate/lat/data/sampled_imagenet/" \
  --model_path "/media/dsg3/dsgprivate/yuhang/model/resnet18/new_plat/" \
  --pro_num 5 \
  --alpha 0.7 \
  --epsilon 0.3 \
  --dataset "imagenet" \
  --model "resnet" \
  --dropout 'True' \
  --test_data_path "/media/dsg3/dsgprivate/lat/sampled_imagenet/test/alexnet/test_adv(eps_0.031).p" \
  --test_label_path "/media/dsg3/dsgprivate/lat/sampled_imagenet/test/alexnet/test_label.p" \
  --logfile './log_newplat/newplat3.txt' 