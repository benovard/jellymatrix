#!/bin/bash

echo "Ensure packages are installed:"
sudo apt-get install libopenjp2-7 python3-dbus

echo "Blacklist soundcard..."
sudo touch /etc/modprobe.d/alsa-blacklist.conf
sudo echo "blacklist snd_bcm2835" >> /etc/modprobe.d/alsa-blacklist.conf

echo "Installing pillow library:"
pip install pillow || pip install --break-system-packages pillow

echo "Installing flask library:"
pip install flask || pip install --break-system-packages flask

echo "Installing requests library:"
pip install requests || pip install --break-system-packages requests

install_path=$(pwd)

echo "Creating config file if missing:"
[ -f ./config/rgb_options.ini ] || cp ./config/rgb_options.example.ini ./config/rgb_options.ini
echo "...done"

echo "Downloading rgb-matrix software setup:"
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.py > rgb-matrix.sh

sed -n '/REBOOT NOW?/q;p' < rgb-matrix.sh > rgb-matrix-jellymatrix.sh

echo "Running rgb-matrix software setup:"
sudo bash rgb-matrix-jellymatrix.sh

echo "Removing rgb-matrix setup script:"
sudo rm rgb-matrix.sh
echo "...done"

echo "Removing jellymatrix service if it exists:"
sudo systemctl stop jellymatrix
sudo rm -rf /etc/systemd/system/jellymatrix.*
sudo systemctl daemon-reload
echo "...done"

echo "Removing jellymatrix-client service if it exists:"
sudo systemctl stop jellymatrix-client
sudo rm -rf /etc/systemd/system/jellymatrix-client.*
sudo systemctl daemon-reload
echo "...done"

echo "Creating jellymatrix service:"
sudo cp ./config/jellymatrix.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=python3 ${install_path}/python/displayCoverArt.py" /etc/systemd/system/jellymatrix.service
sudo systemctl daemon-reload
sudo systemctl start jellymatrix
sudo systemctl enable jellymatrix
echo "...done"

echo "Creating jellymatrix-client service:"
sudo cp ./config/jellymatrix-client.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=python3 ${install_path}/python/client/app.py" /etc/systemd/system/jellymatrix-client.service
sudo systemctl daemon-reload
sudo systemctl start jellymatrix-client
sudo systemctl enable jellymatrix-client
echo "...done"

echo -n "In order to finish setup a reboot is necessary..."
echo -n "REBOOT NOW? [y/N] "
read
if [[ ! "$REPLY" =~ ^(yes|y|Y)$ ]]; then
        echo "Exiting without reboot."
        exit 0
fi
echo "Reboot started..."
reboot
sleep infinity
