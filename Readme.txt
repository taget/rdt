cd init-vm

# init vm and start stream as noisy neighbor
./run.sh vm-init.yml

# show running vms
cd ..
sudo virsh list
$ sudo virsh list
 Id    Name                           State
----------------------------------------------------
 16    instance-00000027              running
 17    instance-00000028              running
 18    instance-00000029              running
 19    instance-0000002a              running
 20    instance-0000002b              running
 21    instance-0000002d              running
 22    instance-00000030              running
 23    instance-0000002e              running
 24    instance-0000002f              running
 25    instance-0000002c              running

# add running vms' domain ids to show_cmt.sh paramter
sudo ./show_cmt.py 16 17 18 ...

# kill noisy neighbor

cd init-vm
./run.sh kill-noisy.yml

