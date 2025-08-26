1. sudo apt-get update 
install python3
2. install vosk small model, like en 0.15
# Go to home folder (or your project dir)
cd ~

# Make a directory for vosk models
mkdir -p vosk_models && cd vosk_models

# Download the small English model (about 50MB)
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip

# Unzip the model
unzip vosk-model-small-en-us-0.15.zip

# Rename for convenience
mv vosk-model-small-en-us-0.15 model

3. install rapidfuzz model

then, 
basc cmnd
sudo apt-get update
sudo apt-get install python3-dev python3-pip portaudio19-dev espeak -y
pip3 install vosk pyttsx3 pyaudio rapidfuzz pyyaml

4. open virtual environment if problem to install pyyaml
then active virtual environment

5. create sudo nano qna.yml file
6. create sudo nano diu_asstn.py file and pest code
7. then set vosk path and qna.yml path 


8. check your audio is correct 
python3 - <<'EOF'
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(i, p.get_device_info_by_index(i).get('name'))
EOF
then set mic index your py code

8. run code, python3 diu_asstn.py

auto ran setup
1. execute bash, 
chmod +x /home/rasel/diu_asstn.py
2.create service file,
sudo nano /etc/systemd/system/diu_asstn.service

3. then pest this  file:
[Unit]
Description=DIU Voice Assistant
After=network.target sound.target

[Service]
ExecStart=/usr/bin/python3 /home/rasel/diu_asstn.py
WorkingDirectory=/home/rasel
StandardOutput=journal
StandardError=journal
Restart=always
User=rasel
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target

ctrl+0 and enter then ctrl+x

4. enable and start service :

sudo systemctl daemon-reload
sudo systemctl enable diu_asstn.service
sudo systemctl start diu_asstn.service

5. check status:
systemctl status diu_asstn.service

6. sudo reboot 
after rebbot your auto run assistant is ready

