import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import logging
import os
import time
from directorylisting import Directory


class DirectoryCheckSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "DitectoryCheck"
    _svc_display_name_ = "Directory Check"
    _svc_description_ = "Checks given directory for any added or removed files and sending email"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('Stopping service ...')
        self.stop_requested = True

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        while not self.stop_requested:
            time.sleep(30)
            try:
                FilesInDirectory = Directory("C:\\Users\\a.baghajyan\\Downloads\\file-change-action-master\\Folder")
                get_list = FilesInDirectory.get_files()

                if not os.path.isfile("C:\\Users\\a.baghajyan\\Downloads\\file-change-action-master\\filelist.txt"):
                    FilesInDirectory.write_in_file(get_list)

                lastlist = FilesInDirectory.read_from_file()
                added = FilesInDirectory.compare_files(get_list, lastlist)

                removed = FilesInDirectory.compare_files(lastlist, get_list)
                if len(added + removed) > 0:
                    FilesInDirectory.sent_email(added, removed)
                    FilesInDirectory.write_in_file(get_list)
                else:
                    print("NOTHING TO SEND")
            except Exception as Error:
                print(Error)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DirectoryCheckSvc)
