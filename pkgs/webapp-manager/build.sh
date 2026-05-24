# Create a symlink so 'webapp-manager' works in the terminal
mkdir -p files/usr/bin
ln -s /usr/lib/WebappManager/WebappManager.py files/usr/bin/webapp-manager
chmod +x files/usr/lib/WebappManager/WebappManager.py
