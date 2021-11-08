# Zabbix_addon
Аддон для Zabbix агента для мониторинга служб и сервисов на рабочих компьютерах

Данные подгружает из файла service.json
Вызов аддона из агента:

    Получить JSON данные для сервера по всем службам из файла для autodiscovery:
    UserParameter=Service.Discovery,"C:\Program Files\Zabbix Agent\service.exe" "service"
    
    Получить данные для сервера по конкретной службе:
    UserParameter=Service[*],"C:\Program Files\Zabbix Agent\service.exe" "status" "$1"
    
    Получить JSON данные для сервера по всем процессам из файла для autodiscovery:
    UserParameter=Process.Discovery,"C:\Program Files\Zabbix Agent\service.exe" "process"
    
    Получить данные для сервера по конкретному процессу:
    UserParameter=Process[*],"C:\Program Files\Zabbix Agent\service.exe" "run" "$1"
    
    Получить данные для сервера по логину активного пользователя:
    UserParameter=UserInfo[*],"C:\Program Files\Zabbix Agent\service.exe" "$1"
