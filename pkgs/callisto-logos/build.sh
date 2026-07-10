# Load in any docs, if required
mkdir -p files/usr/share/docs/callisto-logos
mkdir -p files/usr/share/licenses/callisto-logos

# Change logo files everywhere fedora-logos does
mkdir -p files/usr/share/anaconda/boot/
cp -f anaconda/boot/splash.png files/usr/share/anaconda/boot/splash.png
cp -f anaconda/boot/syslinux-splash.png files/usr/share/anaconda/boot/syslinux-splash.png

mkdir -p files/usr/share/anaconda/pixmaps/
cp -f anaconda/pixmaps/anaconda_header.png files/usr/share/anaconda/pixmaps/anaconda_header.png
cp -f anaconda/pixmaps/progress_first.png files/usr/share/anaconda/pixmaps/progress_first.png
cp -f anaconda/pixmaps/sidebar-bg.png files/usr/share/anaconda/pixmaps/sidebar-bg.png
magick -background none -density 300 callisto-logo.svg -resize 128x128 files/usr/share/anaconda/pixmaps/sidebar-logo.png
cp -f anaconda/pixmaps/progress_first.png files/usr/share/anaconda/pixmaps/splash.png
cp -f firstboot/pixmaps/topbar-bg.png files/usr/share/anaconda/pixmaps/topbar-bg.png

mkdir -p files/usr/share/firstboot/themes/generic
cp -f firstboot/firstboot-left.png files/usr/share/firstboot/themes/generic/firstboot-left.png
cp -f firstboot/workstation.png files/usr/share/firstboot/themes/generic/workstation.png

mkdir -p files/usr/share/icons/hicolor/scalable/apps
mkdir -p files/usr/share/icons/hicolor/scalable/places
mkdir -p files/usr/share/icons/hicolor/48x48/apps/
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/distribution-logo.svg
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/callisto-logo.svg
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/anaconda.svg
magick -background none -density 300 callisto-logo.svg -resize 49x49 files/usr/share/icons/hicolor/48x48/apps/anaconda.png
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/fedora-logo-icon.svg
cp -f callisto-logo.svg files/usr/share/icons/hicolor/scalable/apps/fedora-logo-sprite.svg
cp -f start-here.svg files/usr/share/icons/hicolor/scalable/apps/start-here.svg
cp -f start-here.svg files/usr/share/icons/hicolor/scalable/places/start-here.svg

mkdir -p files/usr/share/icons/oxygen/48x48/apps/
magick -background none -density 300 callisto-logo.svg -resize 49x49 files/usr/share/icons/oxygen/48x48/apps/anaconda.png

mkdir -p files//usr/share/kde4/apps/ksplash/Themes/Leonidas/2048x1536
cp -f ksplash/logo.png files/usr/share/kde4/apps/ksplash/Themes/Leonidas/2048x1536/logo.png

mkdir -p files//usr/share/pixmaps/bootloader
magick -background none -density 300 callisto-logo.svg -resize 128x128 files/usr/share/pixmaps/bootloader/fedora.icns
cp -f fedora.vol files/usr/share/pixmaps/bootloader/fedora.vol
cp -f fedora-media.vol files/usr/share/pixmaps/bootloader/fedora-media.vol

mkdir -p files/usr/share/pixmaps
mkdir -p files/usr/share/pixmaps/splash
magick -background none -density 300 callisto-logo.svg -resize 128x128 files/usr/share/pixmaps/fedora-logo-small.png
cp -f callisto-logo.svg files/usr/share/pixmaps/fedora-logo-sprite.svg
magick -background none -density 300 callisto-logo.svg -resize 240x240 files/usr/share/pixmaps/fedora-logo.png
magick -background none -density 300 callisto-logo.svg -resize 240x240 files/usr/share/pixmaps/system-logo-white.png
cp -f splash/gnome-splash.png files/usr/share/pixmaps/splash/gnome-splash.png

mkdir -p files/usr/share/plymouth/themes/charge
cp -f progress/progress-00.png files/usr/share/plymouth/themes/charge/progress-00.png
cp -f progress/progress-01.png files/usr/share/plymouth/themes/charge/progress-01.png
cp -f progress/progress-02.png files/usr/share/plymouth/themes/charge/progress-02.png
cp -f progress/progress-03.png files/usr/share/plymouth/themes/charge/progress-03.png
cp -f progress/progress-04.png files/usr/share/plymouth/themes/charge/progress-04.png   
cp -f progress/progress-05.png files/usr/share/plymouth/themes/charge/progress-05.png
cp -f progress/progress-06.png files/usr/share/plymouth/themes/charge/progress-06.png
cp -f progress/progress-07.png files/usr/share/plymouth/themes/charge/progress-07.png
cp -f progress/progress-08.png files/usr/share/plymouth/themes/charge/progress-08.png
cp -f progress/progress-09.png files/usr/share/plymouth/themes/charge/progress-09.png
cp -f progress/progress-10.png files/usr/share/plymouth/themes/charge/progress-10.png
cp -f progress/progress-11.png files/usr/share/plymouth/themes/charge/progress-11.png
cp -f progress/progress-12.png files/usr/share/plymouth/themes/charge/progress-12.png
cp -f progress/progress-13.png files/usr/share/plymouth/themes/charge/progress-13.png
cp -f progress/progress-14.png files/usr/share/plymouth/themes/charge/progress-14.png
cp -f progress/progress-15.png files/usr/share/plymouth/themes/charge/progress-15.png
cp -f progress/progress-16.png files/usr/share/plymouth/themes/charge/progress-16.png
cp -f progress/progress-17.png files/usr/share/plymouth/themes/charge/progress-17.png
cp -f progress/progress-18.png files/usr/share/plymouth/themes/charge/progress-18.png
cp -f progress/progress-19.png files/usr/share/plymouth/themes/charge/progress-19.png
cp -f progress/progress-20.png files/usr/share/plymouth/themes/charge/progress-20.png
cp -f progress/progress-21.png files/usr/share/plymouth/themes/charge/progress-21.png
cp -f progress/progress-22.png files/usr/share/plymouth/themes/charge/progress-22.png
cp -f progress/progress-23.png files/usr/share/plymouth/themes/charge/progress-23.png
cp -f progress/progress-24.png files/usr/share/plymouth/themes/charge/progress-24.png
cp -f progress/progress-25.png files/usr/share/plymouth/themes/charge/progress-25.png
cp -f progress/progress-26.png files/usr/share/plymouth/themes/charge/progress-26.png
cp -f progress/progress-27.png files/usr/share/plymouth/themes/charge/progress-27.png
cp -f progress/progress-28.png files/usr/share/plymouth/themes/charge/progress-28.png
cp -f progress/progress-29.png files/usr/share/plymouth/themes/charge/progress-29.png
cp -f progress/progress-30.png files/usr/share/plymouth/themes/charge/progress-30.png
cp -f progress/progress-31.png files/usr/share/plymouth/themes/charge/progress-31.png
cp -f progress/progress-32.png files/usr/share/plymouth/themes/charge/progress-32.png

magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-00.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-01.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-02.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-03.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-04.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-05.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-06.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-07.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-08.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-09.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-10.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-11.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-12.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-13.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-14.png
magick -background none -density 300 callisto-logo.svg -resize 135x135 files/usr/share/plymouth/themes/charge/throbber-15.png