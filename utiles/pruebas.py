import os 
for root,dirs,files in os.walk('//xabistation/homes/zuri/Photos/MobileBackup/'):
    for file in files:
        print(os.path.join(root, file))