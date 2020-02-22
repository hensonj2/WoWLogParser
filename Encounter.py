from datetime import timedelta
from datetime import datetime
from datetime import time
from re import sub

def Encounter(raid, line, info, boss, pulls, ifile):
    healIDs = ['740', '31884', '31821', '108280', '98008','62618','33206','64843','47788','115310','116849']
    timeStart = info[1]
    startDay = info[0].replace('/', '-')

    para = raid[boss]
    hparse = ''
    parse=[None] * 10
    end = 1
    while end:
        line = ifile.readline().replace('"','').replace('\n','').split(',')
        info = line[0].split(' ')
        if 'ENCOUNTER_START' in info[3]:
            print('Log Error: Encounter Start where End expected.')
            end
        if 'ENCOUNTER_END' in info[3]:
            writeResult(raid,boss,pulls,parse,startDay,hparse)
            print('Encounter ended with '+boss+ ' at '+info[1] +'\n' )
            end = 0
        if (info[3] == 'SPELL_CAST_SUCCESS') and (line[9] in healIDs):
            eTime = timeDif(timeStart, info[1])
            line[2] = sub('-\w*','',line[2])
            hparse = hparse + str(pulls) + ',' + eTime + ',' + line[10] + ',' + line[2] + '\r\n'
        for i in range(0,len(raid[boss])):
            if len(line) < 11:
                continue
            if (info[3] in raid[boss][i][0]) and (line[10] in raid[boss][i]):
                if "Player" not in line[5]:
                    continue
                line[6] = sub('-\w*','',line[6])
                if info[3] == 'SPELL_AURA_APPLIED' :
                    if raid[boss][i][2] == 'sum' :
                        if line[6] in parse[i]:
                            parse[i][line[6]] = parse[i][line[6]] + 1
                        else:
                            parse[i][line[6]] = 1
                    else:
                        if parse[i] is None:
                            parse[i] = ''
                        parse[i] = parse[i] + str(pulls) + ',' + timeDif(timeStart, info[1]) + ',' + line[6] + ',' + line[10] + '\r\n'

                elif info[3] == 'SPELL_DAMAGE' :
                    if raid[boss][i][2] == 'sum' :
                        if parse[i] is None:
                            parse[i] = {}
                        if line[6] in parse[i]:
                            parse[i][line[6]] = parse[i][line[6]] + int(line[29])
                        else:
                            parse[i][line[6]] = int(line[29])
                    elif raid[boss][i][2] == 'avg':
                        if parse[i] is None:
                            parse[i] = {}
                        if line[6] in parse[i]:
                            parse[i][line[6]]['dam'] = parse[i][line[6]]['dam'] + int(line[29])
                            parse[i][line[6]]['count'] = parse[i][line[6]]['count'] + 1
                        else:
                            parse[i][line[6]] = {}
                            parse[i][line[6]]['dam'] = int(line[29])
                            parse[i][line[6]]['count'] = 1
                    elif raid[boss][i][2] == 'hit' :
                        if parse[i] is None:
                            parse[i] = ''
                        parse[i] = parse[i] + str(pulls) + ',' + timeDif(timeStart, info[1]) + ',' + line[6] + ',' + '\r\n'
                    elif raid[boss][i][2] == 'dam':
                        if parse[i] is None:
                            parse[i] = ''
                        parse[i] = parse[i] + pulls + ',' + timeDif(timeStart, info[1]) + ',' + line[6] + ',' + line[29] + '\r\n'

                elif info[3] == 'SPELL_CAST_SUCCESS' :
                        parse[i] = parse[i] + pulls + ',' + timediff(timestart, info[1]) + ',' + line[10] + ',' + line[2] + '\r\n'

    return

def timeDif(b, e):
    begin = datetime.strptime(time.fromisoformat(b).strftime('%H:%M:%S'), '%X')
    end = datetime.strptime(time.fromisoformat(e).strftime('%H:%M:%S'), '%X')
    delta = str(end - begin)
    return delta

def writeResult(raid,boss,pulls,parse, startDay, hparse):
    hfile = open('results/'+startDay+'-'+boss+'-'+'Healing.csv', 'a+', newline='')
    hfile.write(hparse)
    hfile.close()

    rfile = [None] * 10

    k = len(raid[boss])
    for i in range(0,k) :
        if parse[i] is None:
            continue
        rfile[i] = open('results/'+startDay+'-'+boss+'-'+ raid[boss][i][1] +'.csv', 'a+', newline='')

        if (raid[boss][i][0] == 'SPELL_AURA_APPLIED'):
            if (raid[boss][i][2] == 'sum'):
                for j in parse[i]:
                    rfile[i].write(pulls+','+j+','+parse[i][j]+'\r\n')
            else:
                rfile[i].write(parse[i])

        elif (raid[boss][i][0] == 'SPELL_DAMAGE'):
            if (raid[boss][i][2] == 'sum'):
                for j in parse[i]:
                    rfile[i].write(str(pulls)+','+j+','+str(parse[i][j])+'\r\n')
            elif (raid[boss][i][2] == 'avg'):
                for j in parse[i]:
                    rfile[i].write(str(pulls)+','+j+','+ str(parse[i][j]['dam'] / parse[i][j]['count'])+'\r\n')
            else:
                rfile[i].write(parse[i])

        elif (raid[boss][i][0] == 'SPELL_CAST_SUCCESS') :
            rfile[i].write(parse[i])

        rfile[i].close()
    return
