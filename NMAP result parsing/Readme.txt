Скрипт парсит результат вывода nmap, собирая в файл результат в виде IP - состояние проверяемого порта.
Проверка порта списка девайсов выолняется командой

nmap -p T:22 -Pn -iL all_devices.txt > scan_result.txt