import os
import smtplib

class Directory():
    """Working with Directory Changes"""
    def __init__(self, directory):
        self.directory = directory
        # self.pwd = os.getcwd() + "\\filelist.txt"
        self.pwd = "Path\\to\\changes\\registering\\directory"

    def get_files(self):
        filelist = []
        for foldername, subfolders, filenames in os.walk(self.directory):
            for filename in filenames:
                filelist.append(foldername +"\\" + filename)
        return filelist

    def write_in_file(self,filelist):
        with open(self.pwd, "w") as files:
            files.write(' '.join(filelist))

    def read_from_file(self):
        filelist = []
        with open(self.pwd, "r") as files:
            file_string = files.readline()
            for word in file_string.split():
                filelist.append(word)
        return filelist

    def compare_files(self, list1, list2):
        """Compare Files list for getting removed and added files"""
        c = []
        for i in list1:
            match = False
            for j in list2:
                if i == j:
                    match = True
            if not match:
                c.append(i)
        return c

    def file_and_directory(self, file):
        for foldername, subfolders, filenames in os.walk(self.directory):
            for filename in filenames:
                if filename == file:
                    return foldername + ': ' + filename

    def sent_email(self,addedFiles, removedFiles):
        smtp_srv = 'smtp.gmail.com'
        send_from = 'armanbaxajyan@gmail.com'
        passwd = 'rubenemin'
        send_to = 'arman.baghajyan@efusoft.com'
        message = 'Subject: File Statuse Update.\nFiles Changed \n'
        if len(addedFiles) > 0:
            message += 'ADDED FILES\n'
            for file in addedFiles:
                message += '{}\n'.format(file)

        if len(removedFiles) > 0:
            message += 'REMOVED FILES\n'
            for file in removedFiles:
                message += '{}\n'.format(file)
        smtpObj = smtplib.SMTP( smtp_srv, 587 )
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(send_from, passwd)
        smtpObj.sendmail(send_from, send_to, str(message))
        smtpObj.quit()

