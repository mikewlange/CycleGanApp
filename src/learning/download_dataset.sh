#!/bin/bash

git clone https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.git
cd pytorch-CycleGAN-and-pix2pix
./datasets/download_cyclegan_dataset.sh vangogh2photo
cd datasets/vangogh2photo/

for D in `find ./* -type d`
do
  mkdir $D/real;
  mv $D/*.jpg $D/real/;
  mv $D ../../../;
done

cd ../../../
rm -rf pytorch-CycleGAN-and-pix2pix
