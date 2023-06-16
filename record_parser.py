import json
from termcolor import colored
from datetime import datetime
import os

#path to speedrunigt records
directory = 'speedrunigt\\records'

def format_milliseconds(millis):

    if(millis < 0):
        millis = abs(millis)

    seconds = (millis/1000) % 60
    seconds = int(seconds)
    minutes = (millis/(1000*60)) % 60
    minutes = int(minutes)
    hours = (millis/(1000*60*60)) % 24

    str_seconds = str(seconds)
    str_minutes = str(minutes)
    str_hours = str(int(hours))
    if (seconds < 10):
        str_seconds = '0'+str(seconds)
    if (minutes < 10):
        str_minutes = '0'+str(minutes)
    if (hours < 10):
        str_hours = '0'+str(int(hours))
    return str_hours+':'+str_minutes+':'+str_seconds

runs = []

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f) and 'json' in filename:

        record_file = open(f)
        data = json.load(record_file)
        if "RandomSpeedrun" not in data['world_name'] or data['is_completed'] == False:
            continue
        runs.append({
            'date': datetime.fromtimestamp(float(data['date'] / 1000)),
            'name': data['world_name'],
            'rta': format_milliseconds(data['final_rta']),
            'igt': format_milliseconds(data['final_igt']),
            'enter_nether': format_milliseconds(data['timelines'][0]['igt']),
            'enter_bastion': format_milliseconds(data['timelines'][1]['igt']),
            'enter_fortress': format_milliseconds(data['timelines'][2]['igt']),
            'first_portal': format_milliseconds(data['timelines'][3]['igt']),
            'enter_stronghold': format_milliseconds(data['timelines'][4]['igt']),
            'enter_end': format_milliseconds(data['timelines'][6]['igt']),
            'kill_dragon': format_milliseconds(data['timelines'][7]['igt']),
            'milliseconds': {
                'igt': data['final_igt'],
                'rta': data['final_rta'],
                'nether': data['timelines'][0]['igt'],
                'bastion': data['timelines'][1]['igt'],
                'fortress': data['timelines'][2]['igt'],
                'portal': data['timelines'][3]['igt'],
                'stronghold': data['timelines'][4]['igt'],
                'end': data['timelines'][6]['igt'],
                'dragon': data['timelines'][7]['igt']
            }
            })

        record_file.close()

global fastest_structure_split
global fastest_stronghold_end
global fastest_end_kill
global fastest_portal_stronghold

newlist = sorted(runs, key=lambda d: d['milliseconds']['igt']) 
newlist.reverse()
fastest_structure_split = 9999999
fastest_stronghold_end = 9999999
fastest_end_kill = 9999999
fatest_portal_stronghold = 9999999
iter = 0
for run in newlist:
    igt_diff = 0
    bastion_diff = 0
    fortress_diff = 0
    nether_diff = 0
    portal_diff = 0
    end_diff = 0
    kill_diff = 0
    stronghold_diff = 0

    if(run['milliseconds']['fortress'] > run['milliseconds']['bastion']):
        if(run['milliseconds']['fortress'] - run['milliseconds']['bastion'] < fastest_structure_split):
            fastest_structure_split = run['milliseconds']['fortress'] - run['milliseconds']['bastion']
    else:
        if(run['milliseconds']['bastion'] - run['milliseconds']['fortress'] < fastest_structure_split):
            fastest_structure_split = run['milliseconds']['bastion'] - run['milliseconds']['fortress']

    if(run['milliseconds']['end'] - run['milliseconds']['stronghold'] < fastest_stronghold_end):
        fastest_stronghold_end = run['milliseconds']['end'] - run['milliseconds']['stronghold']
    
    if((run['milliseconds']['dragon'] - run['milliseconds']['end']) < fastest_end_kill):
        fastest_end_kill = run['milliseconds']['dragon'] - run['milliseconds']['end']

    if(run['milliseconds']['stronghold'] - run['milliseconds']['portal'] < fatest_portal_stronghold):
        if(run['milliseconds']['stronghold'] != run['milliseconds']['portal']):
            fastest_portal_stronghold = run['milliseconds']['stronghold'] - run['milliseconds']['portal']
    


    list_len = newlist.__len__()
    if(list_len > 0 and iter == list_len-1):
        igt_diff = newlist[list_len-2]['milliseconds']['igt'] - run['milliseconds']['igt']
        bastion_diff = newlist[list_len-2]['milliseconds']['bastion'] - run['milliseconds']['bastion']
        fortress_diff = newlist[list_len-2]['milliseconds']['fortress'] - run['milliseconds']['fortress']
        nether_diff = newlist[list_len-2]['milliseconds']['nether'] - run['milliseconds']['nether']
        if(newlist[list_len-2]['milliseconds']['portal'] > 0 and run['milliseconds']['portal'] > 0):
            portal_diff = newlist[list_len-2]['milliseconds']['portal'] - run['milliseconds']['portal']
        end_diff = newlist[list_len-2]['milliseconds']['end'] - run['milliseconds']['end']
        if(newlist[list_len-2]['milliseconds']['dragon'] > 0 and run['milliseconds']['dragon'] > 0):
            kill_diff = newlist[list_len-2]['milliseconds']['dragon'] - run['milliseconds']['dragon']
        stronghold_diff = newlist[list_len-2]['milliseconds']['stronghold'] - run['milliseconds']['stronghold']


    print(colored(run['date'], 'yellow'))
    print('World name:',run['name'])
    print('RTA:',run['rta'])

    if(igt_diff > 0 or igt_diff < 0):
        if(igt_diff > 0):
            print('IGT:',run['igt'],colored('|','magenta'), colored('-'+format_milliseconds(igt_diff),'green'))
        else:
            print('IGT:',run['igt'],colored('|','magenta'), colored('+'+format_milliseconds(igt_diff),'red'))
    else:
        print('IGT:',run['igt'])

    if(nether_diff > 0 or nether_diff < 0):
        if(nether_diff > 0):
            print('Enter nether:',run['enter_nether'],colored('|','magenta'), colored('-'+format_milliseconds(nether_diff),'green'))
        else:
            print('Enter nether:',run['enter_nether'],colored('|','magenta'), colored('+'+format_milliseconds(nether_diff),'red'))
    else:
        print('Enter nether:',run['enter_nether'])

    if(bastion_diff > 0 or bastion_diff < 0):
        if(bastion_diff > 0):
            print('Enter bastion:',run['enter_bastion'],colored('|','magenta'), colored('-'+format_milliseconds(bastion_diff),'green'))
        else:
            print('Enter bastion:',run['enter_bastion'],colored('|','magenta'), colored('+'+format_milliseconds(bastion_diff),'red'))
    else:
        print('Enter bastion:',run['enter_bastion'])

    if(fortress_diff > 0 or fortress_diff < 0):
        if(fortress_diff > 0):
            print('Enter fortress:',run['enter_fortress'],colored('|','magenta'), colored('-'+format_milliseconds(fortress_diff),'green'))
        else:
            print('Enter fortress:',run['enter_fortress'],colored('|','magenta'), colored('+'+format_milliseconds(fortress_diff),'red'))
    else:
        print('Enter fortress:',run['enter_fortress'])

    if(portal_diff > 0 or portal_diff < 0):
        if(portal_diff > 0):
            print('First portal:',run['first_portal'],colored('|','magenta'), colored('-'+format_milliseconds(portal_diff),'green'))
        else:
            print('First portal:',run['first_portal'],colored('|','magenta'), colored('+'+format_milliseconds(portal_diff),'red'))
    else:
        print('First portal:',run['first_portal'])

    if(stronghold_diff > 0 or stronghold_diff < 0):
        if(stronghold_diff > 0):
            print('Enter stronghold:',run['enter_stronghold'],colored('|','magenta'), colored('-'+format_milliseconds(stronghold_diff),'green'))
        else:
            print('Enter stronghold:',run['enter_stronghold'],colored('|','magenta'), colored('+'+format_milliseconds(stronghold_diff),'red'))
    else:
        print('Enter stronghold:',run['enter_stronghold'])

    if(end_diff > 0 or end_diff < 0):
        if(end_diff > 0):
            print('Enter end:',run['enter_end'],colored('|','magenta'), colored('-'+format_milliseconds(end_diff),'green'))
        else:
            print('Enter end:',run['enter_end'],colored('|','magenta'), colored('+'+format_milliseconds(end_diff),'red'))
    else:
        print('Enter end:',run['enter_end'])

    if(kill_diff > 0 or kill_diff < 0):
        if(kill_diff > 0):
            print('Kill dragon:',run['kill_dragon'],colored('|','magenta'), colored('-'+format_milliseconds(kill_diff),'green'))
        else:
            print('Kill dragon:',run['kill_dragon'],colored('|','magenta'), colored('+'+format_milliseconds(kill_diff),'red'))
    else:
        print('Kill dragon:',run['kill_dragon'])

    iter += 1



print(colored('Fastest structure split','cyan'), colored(format_milliseconds(fastest_structure_split),'cyan'))
print(colored('Fastest stronghold to end','cyan'), colored(format_milliseconds(fastest_stronghold_end),'cyan'))
print(colored('Fastest dragon kill','cyan'), colored(format_milliseconds(fastest_end_kill),'cyan'))
print(colored('Fastest portal to stronghold','cyan'), colored(format_milliseconds(fastest_portal_stronghold),'cyan'))


