#!/usr/bin/python
import subprocess ,getopt, sys
import pprint
from optparse import OptionParser
import time
 
def get_options():
    usage = "usage: python %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-m", "--mount",
                    action="store", dest="mount",type="string",
                    help="Mount the and map to destination")
    parser.add_option("-v", "--vagrantpass",type="string",action="store",
                    help="password for 1204 machine",default='vagrant')
    parser.add_option("-u", "--ubuntupass",type="string",action="store",
                    help="password for 1604 machine",default='ubuntu')
    parser.add_option("-o", "--only",
                  default="all",
                  help="machine to start or  [default: %default]")
    parser.add_option("-f", "--full",
                  default=False,
                  help="Start services in machine as well or  [default: %default]")
    options,args = parser.parse_args()
    option_dict = vars(options)
    return option_dict
def main():
    options = get_options()
    (m_12,m_16) = check_vm(options['only'])
    (s_12,s_16) = start_vm(options['only'],m_12,m_16)
    if options['full'] :
        #lets the machine start
        time.sleep(10) 
        (state_12,state_16) = start_services(options)
    if options['mount'] :
        mount_directory (options)
def check_vm(check):
    vagrant = 0 
    ubuntu  = 0
    if check == 'ad-12' or 'all' :
        vagrant_status = subprocess.check_output('vagrant status', cwd='/home/Desktop/',shell=True)
        if "running" in vagrant_status :
            vagrant = 1
            print ("runnning")
    if check == 'ad-16' or 'all' :
        ubuntu_status = subprocess.check_output('vagrant status', cwd='/home/Desktop',shell=True)
        if "running" in ubuntu_status :
            print ("runnning")
            ubuntu = 1
    return (vagrant,ubuntu)

def start_vm(start,m12,m16):
    m_12_status = 0
    m_16_status = 0
    if options['only'] == 'ad-12' or 'all' and  m12 !=0  :
       m_12_status = subprocess.check_output('VBoxManage startvm "ad-12_ad-1204_1521548672962_54098" --type headless',shell=True)
       if 'has been successfully started' in m_12_status :
            m_12_status = 1
    if options['only']== 'ad-16' or 'all' and m16 !=0 :
       m_16_status = subprocess.check_output('VBoxManage startvm "ad-16_ad-1604_1521440700846_20228" --type headless',shell=True)
       if 'has been successfully started' in m_16_status :
            m_16_status = 1
    return (m_12_status,m_16_status)

def start_service (option):
     #assume machine has been started
    if options['only'] == 'ad-12' or 'all':
       cmd = 'sshpass -p ' + option['vagrantpass'] + 'ssh vagrant@localhost cd /site/ad-local/ && make start-ad-all | lolcat'
       m_12_services = subprocess.check_output(cmd,shell=True)
    if options['only'] == 'ad-16' or 'all':
       cmd = 'sshpass -p ' + option['ubuntupass'] + 'ssh ubuntu@localhost cd /site/ad-local/ && make start-ad-all | lolcat'
       m_16_services = subprocess.check_output(cmd,shell=True)
    return (m_12_services,m_16_services)

def mount_directory (option):
    if options['only'] == 'ad-12' or 'all' :
        cmd = 'echo' + option['vagrantpass'] + '| sshfs ubuntu@localhost:/ /home/af/Desktop/ad_1604 -o password_stdin'
        m_12_mount = subprocess.check_output(cmd,shell=True)
    if options['only'] == 'ad-16' or 'all':
        cmd = 'echo' + option['ubuntupass'] + '| sshfs ubuntu@localhost:/ /home/af/Desktop/ad_1604 -o password_stdin'
if __name__ == "__main__":
    main()
