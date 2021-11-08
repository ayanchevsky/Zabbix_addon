import argparse
import os
import shutil
from pyad import adcomputer
import sys
import json
import psutil
import win32api


class CompInfo:
    def __init__(self):
        self.name = os.getenv('COMPUTERNAME')
        self.group = self.__get_ADGroup()

    def __get_ADGroup(self):
        try:
            user = adcomputer.ADComputer.from_cn(self.name)
            group = str(user.get_attribute('distinguishedName')).split(',')
        except Exception:
            # print(ex)
            return ""
        return group[1][3:]

    def out_format_full(self, service, status, alert):
        return {"{#SRVNAME}": service, "{#SRVFNAME}": status['description'], "{#SRVINFO}": alert,
                "{#COMPNAME}": self.name, "{#GROUP}": self.group}  # , "{#LOGIN}": self.login}

    def get_service(self, service):
        if type(service) == str:
            status = get_status(service)
            return status['status']

        elif type(service) == dict:
            all_service = []
            for srv in service.keys():
                status = get_status(srv, service[srv]['full_name'])
                result = self.out_format_full(srv, status, service[srv]['alert'])
                all_service.append(result)
            return all_service

    def get_process(self, proces:list):
        all_process = []
        for i in proces:
            pr = self.__get_proces(i)
            all_process.append(pr)
        return all_process

    def __get_proces(self, pr_name):
        #all_process = []
        user = ""
        for pr in psutil.process_iter():
            if f"{pr_name}.exe".lower() != pr.name().lower():
                continue
            else:
                user = pr.username().split('\\')[1]
                break
        #all_process.append(
        if user != "":
            return {"{#PRNAME}": pr_name, "{#PRUSER}": user, "{#RPSTATUS}": "work", "{#PRGROUP}": self.group}
        else:
            return {"{#PRNAME}": pr_name, "{#PRUSER}": user, "{#RPSTATUS}": "stop", "{#PRGROUP}": self.group}


def get_status(name, full_name=''):
    service = {}
    try:
        service = psutil.win_service_get(name)
        service = service.as_dict()
    except Exception as ex:
        service['status'] = None
        service['description'] = full_name
        return service
    if full_name != '':
        service['description'] = full_name
    return service


def get_file_script():
    dir = os.environ["ProgramFiles"] + '\Zabbix Agent\service.json'
    if os.path.exists(r'\\dc.centrzaimov.ru\data\distrib\gpo\Service\service.json'):
        shutil.copyfile(r'\\dc.centrzaimov.ru\data\distrib\gpo\Service\service.json', dir)


def get_services():
    dir = os.environ["ProgramFiles"] + '\Zabbix Agent'
    os.chdir(dir)
    # dir = os.path.abspath(os.curdir) + r'\service.json'
    if os.path.exists('service.json'):
        with open('service.json', "r", encoding='UTF-8') as read_file:
            data = json.load(read_file)
        if len(data) > 0:
            return data[0]
        return None
    else:
        get_file_script()
        return get_services()


def main(argument1, argument2):
    pr = []
    monitoring_service = get_services()
    comp = CompInfo()
    if argument1.lower() == "service":
        result = comp.get_service(monitoring_service['Service'])
    elif argument1.lower() == "status" and argument2:
        result = comp.get_service(argument2)
    elif argument1.lower() == "process":
        process = monitoring_service['Process']
        pr = (list(i for i in process.keys()))
        result = comp.get_process(pr)
    elif argument1.lower() == "run" and argument2:
        process = comp.get_process([argument2, ])
        result = process[0]["{#RPSTATUS}"]
    elif argument1.lower() == "user":
        pr = ["explorer", ]
        user = comp.get_process(pr)
        result = user[0]["{#PRUSER}"]
    elif argument1.lower() == "group":
        result = comp.group
    elif argument1.lower() == "name":
        result = comp.name
    else:
        result = f"Неизвестный аргументы: {argument1} {argument2}"

    sys.stdout = os.fdopen(sys.stdout.buffer.fileno(), 'w', encoding='utf8')
    sys.stderr = os.fdopen(sys.stderr.buffer.fileno(), 'w', encoding='utf8')
    # print(str(result).replace("'", '"'))
    print(str(result).replace("'", '"'))
    # asd = str(service_out)
    # print(asd.encode('UTF-8').decode('UTF-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('arg1', nargs='?', default="Service")
    parser.add_argument('arg2', nargs='?', default="")
    args = parser.parse_args()
    main(args.arg1, args.arg2)
