python attack.py \
  --attack 'pgd' \
  --generate 'True' \
  --droplast 'False' \
  --model 'densenet' \
  --enable_lat 'False' \
  --modelpath "/media/dsg3/yuhang/model/densenet/without_dropout/naive_param.pkl" \
  --model_batchsize 64 \
  --dropout 'False' \
  --dataset 'cifar10' \
  --attack_batchsize 64 \
  --attack_epsilon 8 \
  --attack_alpha 16 \
  --attack_iter 10 \
  --attack_momentum 1.0 \
  --savepath "/media/dsg3/dsgprivate/lat/test_pgd/densenet/" \
  --lat_epsilon 0.6 \
  --lat_pronum 7 \
  
