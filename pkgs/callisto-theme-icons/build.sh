# Clone icon theme and install it to the package files directory
mkdir -p files/usr/share/icons
git clone --depth 1 https://github.com/vinceliuice/Tela-icon-theme.git
./Tela-icon-theme/install.sh -c -d ./files/usr/share/icons -n "Tela (Callisto)"

echo "Cleaning up temporary files..."
rm -rf Tela-icon-theme                                              # Remove the cloned repository after installation
rm -rf "files/usr/share/icons/Tela (Callisto)/icon-theme.cache"     # Remove the cache as its generated on the target system

# Fix all symbolic links to point to the correct location in the package files directory
rm -rf "files/usr/share/icons/Tela (Callisto)/scalable@2x"      
rm -rf "files/usr/share/icons/Tela (Callisto)/16@2x"      
rm -rf "files/usr/share/icons/Tela (Callisto)/22@2x"      
rm -rf "files/usr/share/icons/Tela (Callisto)/24@2x"      
rm -rf "files/usr/share/icons/Tela (Callisto)/32@2x"      

ln -s "/usr/share/icons/Tela (Callisto)/scalable" "files/usr/share/icons/Tela (Callisto)/scalable@2x"  
ln -s "/usr/share/icons/Tela (Callisto)/16" "files/usr/share/icons/Tela (Callisto)/16@2x"  
ln -s "/usr/share/icons/Tela (Callisto)/22" "files/usr/share/icons/Tela (Callisto)/22@2x"  
ln -s "/usr/share/icons/Tela (Callisto)/24" "files/usr/share/icons/Tela (Callisto)/24@2x"  
ln -s "/usr/share/icons/Tela (Callisto)/32" "files/usr/share/icons/Tela (Callisto)/32@2x"  

ls -al "files/usr/share/icons/Tela (Callisto)"

# Customize the icons for Callisto OS
echo "Customizing icons for Callisto OS..."
for dir in 'files/usr/share/icons/Tela (Callisto)/32/status/' 'files/usr/share/icons/Tela (Callisto)/24/panel/' 'files/usr/share/icons/Tela (Callisto)/22/panel/' 'files/usr/share/icons/Tela (Callisto)/16/panel/'; do 
    sudo cp -f ../callisto-theme-branding/start-here.svg "$dir"; 
done
