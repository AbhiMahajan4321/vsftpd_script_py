# vsftpd_script.py
# Python automated script to install vsftpd on ubuntu (cloud aws) 

# Steps to install vsftpd in AWS ubuntu

# Make sure to add inbound rules in security groups 
# 1. Select the instance
# 2. Go to security
# 3. Open security groups
# 4. Open inbound rules

# 5. Add passive minimin port to passive maximum port, Port = 9000-10000, CIDR Blocks = 0.0.0.0/0  
# 6. Add FTPS (Secured), Port = 990, CIDR Blocks = 0.0.0.0/0  
# 7. Add FTP, Port = 21, CIDR Blocks = 0.0.0.0/0  

# download the code/file on ubuntu using, "git clone <code link>" command

# open the code directory, run it as "sudo python3 <file>"
