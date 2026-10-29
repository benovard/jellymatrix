import configparser
import os
import requests

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config/rgb_options.ini')

def getSongInfo():
  config = configparser.ConfigParser()
  config.read(CONFIG_PATH)

  if not config.has_section('jellyfin'):
    return None

  jellyfin = config['jellyfin']
  server_url = jellyfin.get('server_url', '').strip().rstrip('/')
  api_key = jellyfin.get('api_key', '').strip()
  device = jellyfin.get('device', '').strip()

  if not server_url or not api_key:
    return None

  headers = {"X-Emby-Token": api_key, "accept": "application/json"}
  response = requests.get(f"{server_url}/Sessions", headers=headers, timeout=5)

  if response.status_code != 200:
    return None

  for session in response.json():
    if device and device.lower() not in session.get("DeviceName", "").lower():
      continue
    item = session.get("NowPlayingItem")
    if item:
      item_id = item.get("AlbumId") or item.get("Id")
      if item_id:
        return f"{server_url}/Items/{item_id}/Images/Primary?maxWidth=500&api_key={api_key}"

  return None
