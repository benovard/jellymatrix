# Jellymatrix

### Overview
Jellymatrix is a fork of [Spotipi](https://github.com/ryanwa18/spotipi) by ryanwa18. It displays the album artwork of whatever is currently playing on your Jellyfin server on an LED matrix attached to a Raspberry Pi.

### Requirements
* Raspberry Pi with an Adafruit RGB Matrix Bonnet or HAT. I suggest a Zero W or Zero 2 W due to low cost and ability to use WiFi.
* A 32x32 or 64x64 LED matrix panel, properly powered
* A Jellyfin server on your network

### Getting Started
* SSH to your Raspberry Pi and clone the repository:
```
git clone https://github.com/benovard/jellymatrix.git
cd jellymatrix
```
* Install the software (installs and enables the jellymatrix and jellymatrix-client systemd services):
```
sudo bash setup.sh
```
* Reboot when prompted.

### Configure Jellyfin
* In your Jellyfin dashboard, go to **API Keys** and generate a new key.
* Navigate to `http://<raspberrypi_hostname or ip_address>` (ex. `http://raspberrypi.local`) in a web browser.
* Under **Jellyfin Server**, enter your server URL (ex. `http://192.168.0.1:8096`), paste the API key, and optionally set a device filter so only a specific client's playback is displayed (leave blank to show any active session).
* Play something in Jellyfin — the album art appears on the matrix within a few seconds. When nothing is playing, a default image is shown.

### Troubleshooting
* **Matrix completely blank, but `systemctl status jellymatrix` shows active (running):** if your Adafruit HAT/Bonnet does **not** have the PWM jumper soldered, `hardware_mapping` in `config/rgb_options.ini` must be `adafruit-hat`, not `adafruit-hat-pwm`. The `-pwm` variant leaves the panel's output-enable line undriven, resulting in a perfectly dark panel with no errors. Edit the file, then run `sudo systemctl restart jellymatrix`.
* **Default image shows even while music plays:** check the Jellyfin Server settings in the web UI (server URL and API key). If multiple people use your server, set the device filter to your player's device name. Also inspect logs with `journalctl -u jellymatrix -n 50`.
* **Matrix goes blank for a couple of seconds after changing a setting in the web UI:** normal — the display service restarts to apply matrix configuration changes.
* **Everything looks fine but the server can't be reached:** the display loop polls your Jellyfin server once per second with a 5 second timeout, so an unreachable server degrades to the default image rather than a frozen display.

### Credits
* [Spotipi](https://github.com/ryanwa18/spotipi) by ryanwa18 — the original Spotify-powered version of this project.
