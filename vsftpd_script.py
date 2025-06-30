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


import os
import subprocess
import sys

def run_cmd(command, check=True):
    print(f"\n[+] Executing: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)

    if result.returncode != 0:
        print(f"[!] ERROR executing: {command}")
        print(f"    {result.stderr.strip()}")
        if check:
            sys.exit(1)
    else:
        if result.stdout.strip():
            print(f"[✓] Output: {result.stdout.strip()}")
        else:
            print("[✓] Success")

def ensure_root():
    if os.geteuid() != 0:
        print("❌ This script must be run as root (use sudo).")
        sys.exit(1)

def install_vsftpd():
    print("\n📦 Installing vsftpd...")
    run_cmd("apt update -y")
    run_cmd("apt install vsftpd -y")

def configure_vsftpd():
    print("\n⚙️  Configuring /etc/vsftpd.conf to avoid FileZilla errors...")

    vsftpd_config = """
listen=YES
listen_ipv6=NO
anonymous_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=YES
chroot_local_user=YES
allow_writeable_chroot=YES
pam_service_name=vsftpd
user_sub_token=$USER
local_root=/home/$USER
pasv_enable=YES
pasv_min_port=9000
pasv_max_port=10000
    """.strip()

    try:
        with open("/etc/vsftpd.conf", "w") as conf_file:
            conf_file.write(vsftpd_config)
        print("[✓] /etc/vsftpd.conf written successfully")
    except Exception as e:
        print(f"[!] Failed to write config: {e}")
        sys.exit(1)

    run_cmd("systemctl restart vsftpd")
    run_cmd("systemctl enable vsftpd")

def disable_firewall():
    print("\n🚫 Disabling UFW firewall to avoid FTP port issues...")
    run_cmd("ufw disable", check=False)  # Okay if ufw is not installed/enabled

def create_ftp_user(username="ftpuser", password="ftp@123"):
    print(f"\n👤 Creating FTP user '{username}'...")

    run_cmd(f"useradd -m {username}", check=False)  # Ignore if user exists
    run_cmd(f"echo '{username}:{password}' | chpasswd")

    ftp_dir = f"/home/{username}"
    files_dir = f"{ftp_dir}/files"

    run_cmd(f"mkdir -p {files_dir}")
    run_cmd(f"chown nobody:nogroup {ftp_dir}")
    run_cmd(f"chmod a-w {ftp_dir}")
    run_cmd(f"chown {username}:{username} {files_dir}")

    print(f"\n✅ FTP user created: {username}")
    print(f"   Password: {password}")
    print(f"   FTP Root: {ftp_dir}")

def main():
    ensure_root()
    install_vsftpd()
    configure_vsftpd()
    disable_firewall()
    create_ftp_user()
    print("\n🎉 vsftpd installation and setup complete! Use FileZilla with passive mode and login using port 21.")

if __name__ == "__main__":
    main()
