# Change Fedora logo to Callisto Logo
mkdir -p files/usr/share/icons/hicolor/scalable/apps
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/distribution-logo.svg
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/callisto-logo.svg
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/fedora-logo-icon.svg
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/fedora-logo-sprite.svg

mkdir -p files/usr/share/pixmaps
cp -f callisto-logo.png files/usr/share/pixmaps/fedora-logo.png
cp -f callisto-logo.png files/usr/share/pixmaps/system-logo-white.png
cp -f callisto-logo-small.png files/usr/share/pixmaps/fedora-logo-small.png

# Change "start-here" application launcher icon to a modified logo
mkdir -p files/usr/share/icons/breeze-dark/places/16 \
            files/usr/share/icons/breeze-dark/places/22 \
            files/usr/share/icons/breeze-dark/places/24 \
            files/usr/share/icons/breeze-dark/places/32 \
            files/usr/share/icons/breeze-dark/places/64 \
            files/usr/share/icons/breeze-dark/places/96 \
            files/usr/share/icons/breeze/places/16 \
            files/usr/share/icons/breeze/places/22 \
            files/usr/share/icons/breeze/places/24 \
            files/usr/share/icons/breeze/places/32 \
            files/usr/share/icons/breeze/places/64 \
            files/usr/share/icons/breeze/places/96
            
cp -f start-here.svg files/usr/share/icons/hicolor/scalable/start-here.svg
cp -f start-here.svg files/usr/share/icons/breeze-dark/places/16/start-here-kde-symbolic.svg
cp -f start-here.svg files/usr/share/icons/breeze-dark/places/22/start-here-kde-symbolic.svg
cp -f start-here.svg files/usr/share/icons/breeze-dark/places/24/start-here-kde-symbolic.svg
cp -f start-here.svg files/usr/share/icons/breeze-dark/places/32/start-here-kde-symbolic.svg
cp -f start-here.svg files/usr/share/icons/breeze-dark/places/64/start-here-kde-symbolic.svg
cp -f start-here.svg files/usr/share/icons/breeze-dark/places/96/start-here-kde-symbolic.svg

cp -f start-here.svg files/usr/share/icons/breeze/places/16/start-here-kde-symbolic.svg
cp -f start-here.svg files/usr/share/icons/breeze/places/22/start-here-kde-symbolic.svg
cp -f start-here.svg files/usr/share/icons/breeze/places/24/start-here-kde-symbolic.svg
cp -f start-here.svg files/usr/share/icons/breeze/places/32/start-here-kde-symbolic.svg
cp -f start-here.svg files/usr/share/icons/breeze/places/64/start-here-kde-symbolic.svg
cp -f start-here.svg files/usr/share/icons/breeze/places/96/start-here-kde-symbolic.svg