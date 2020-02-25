echo "#########################################"
echo "#########Setup Optris PI camera##########"
echo "#########################################"

# UCV configuration
sudo bash -c 'echo "options uvcvideo nodrop=1" > /etc/modprobe.d/uvcvideo.conf'
sudo rmmod uvcvideo; sudo modprobe uvcvideo nodrop=1

if [[ $(command groups) != *"video"* ]]
then
    sudo usermod -a -G video $(whoami)

fi

# Install dependecies
sudo apt-get install cmake freeglut3-dev libusb-1.0-0-dev

# Install Libirimager
mkdir ~/build_libirimager && cd ~/build_libirimager
wget ftp.evocortex.com/libirimager-7.2.0-amd64.deb
sudo dpkg -i libirimager-7.2.0-amd64.deb

# Download calibration
sudo ir_download_calibration

# Generating configuration file
sudo ir_generate_configuration > `ir_find_serial`.xml
