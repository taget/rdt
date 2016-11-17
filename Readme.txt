cd init-vm

# init vm and start stream as noisy neighbor
./run.sh vm-init.yml

# show running vms
cd ..
sudo virsh list

# add running vms' domain ids to show_cmt.sh paramter
./show_cmt.sh 1 2 3

# kill noisy neighbor

cd init-vm
./run.sh kill-noisy.yml

