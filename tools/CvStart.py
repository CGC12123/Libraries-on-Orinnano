import subprocess

def Cv_Start():
    cv_shs = ["echo 123456 | sudo -S chmod +x /home/c/Library/Cv_for_Orinnano/tools/bash/CvModeStart.sh",
              "/home/c/Library/Cv_for_Orinnano/tools/bash/CvModeStart.sh"]
    cv_sh = "bash -c '{}'".format("; ".join(cv_shs))
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', cv_sh], 
                      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':
    Cv_Start()