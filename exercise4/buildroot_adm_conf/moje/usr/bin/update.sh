#!/bin/sh

mkdir /mnt/rootfs
mount /dev/mmcblk0p2 /mnt/rootfs
cd /mnt/rootfs
rm -rf *
cd /mnt/sdcard
umount /dev/mmcblk0p2
cat rootfs.ext4 > /dev/mmcblk0p2
mount /dev/mmcblk0p2 /mnt/rootfs
resize2fs /dev/mmcblk0p2
