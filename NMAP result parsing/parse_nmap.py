#Script parses a result of NMAP and collects to file "IP" and "open/filtered"
import textfsm

with open('scan_result.txt') as source:
    all_scanned_hosts = source.read()

with open('nmap_template') as template:
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseText(all_scanned_hosts)

#print(fsm.header)
#print(result)

with open('FSM_parse_result.txt', 'w') as f:
   for x in result:
       f.write(x[0] + " " + x[1] + '\n')
