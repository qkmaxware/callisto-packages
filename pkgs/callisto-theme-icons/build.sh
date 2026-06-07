# Clone icon theme and install it to the package files directory
mkdir -p files/usr/share/icons
git clone --depth 1 https://github.com/vinceliuice/Tela-icon-theme.git
./Tela-icon-theme/install.sh -c -d ./files/usr/share/icons -n "Tela (Callisto)"

echo "Cleaning up temporary files..."
rm -rf Tela-icon-theme                                              # Remove the cloned repository after installation
rm -rf "files/usr/share/icons/Tela (Callisto)/icon-theme.cache"     # Remove the cache as its generated on the target system
rm -rf "files/usr/share/icons/Tela (Callisto)/scalable@2x"          # Remove the scalable@2x symbolic link
ln -s "/usr/share/icons/Tela (Callisto)/scalable" "files/usr/share/icons/Tela (Callisto)/scalable@2x"    # Create a new symbolic link for scalable@2x pointing to scalable
ls -al "files/usr/share/icons/Tela (Callisto)"

# Customize the icons for Callisto OS
echo "Customizing icons for Callisto OS..."
for dir in 'files/usr/share/icons/Tela (Callisto)/32/status/' 'files/usr/share/icons/Tela (Callisto)/24/panel/' 'files/usr/share/icons/Tela (Callisto)/22/panel/' 'files/usr/share/icons/Tela (Callisto)/16/panel/'; do 
    sudo cp -f ../callisto-theme-branding/start-here.svg "$dir"; 
done
