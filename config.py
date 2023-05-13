import ftplib
ftp = ftplib.FTP(host='#YOUR_HOST_IP_ADDRESS#', timeout=10)
ftp.login(user='#YOUR_USER_NAME#', passwd='#YOUR_PASSWORD#')
