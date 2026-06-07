# Clone icon theme and install it to the package files directory
mkdir -p files/usr/share/icons
git clone --depth 1 https://github.com/vinceliuice/Tela-icon-theme.git
./Tela-icon-theme/install.sh -c -d ./files/usr/share/icons -n "Tela (Callisto)"
rm -rf Tela-icon-theme
ls -al "files/usr/share/icons/Tela (Callisto)"

# Customize the icons for Callisto OS
echo "Customizing icons for Callisto OS..."
for dir in 'files/usr/share/icons/Tela (Callisto)/32/status/' 'files/usr/share/icons/Tela (Callisto)/24/panel/' 'files/usr/share/icons/Tela (Callisto)/22/panel/' 'files/usr/share/icons/Tela (Callisto)/16/panel/'; do 
    sudo cp -f ../callisto-theme-branding/start-here.svg "$dir"; 
done
