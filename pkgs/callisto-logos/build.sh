# Load in any docs, if required
mkdir -p files/usr/share/docs/callisto-logos
mkdir -p files/usr/share/licenses/callisto-logos

# Change Fedora logo to Callisto Logo
mkdir -p files/usr/share/icons/hicolor/scalable/apps
mkdir -p files/usr/share/icons/hicolor/scalable/places
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/distribution-logo.svg
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/callisto-logo.svg
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/fedora-logo-icon.svg
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/fedora-logo-sprite.svg
cp -f start-here.svg files/usr/share/icons/hicolor/scalable/apps/start-here.svg
cp -f start-here.svg files/usr/share/icons/hicolor/scalable/places/start-here.svg

mkdir -p files/usr/share/pixmaps
magick -background none -density 300 callisto-logo.svg -resize 240x240 files/usr/share/pixmaps/fedora-logo.png
magick -background none -density 300 callisto-logo.svg -resize 240x240 files/usr/share/pixmaps/system-logo-white.png
magick -background none -density 300 callisto-logo.svg -resize 128x128 files/usr/share/pixmaps/fedora-logo-small.png
cp -f callisto-logo.svg files/usr/share/pixmaps/fedora-logo-sprite.svg
