import PySimpleGUI as sg
import requests as rq
import subprocess as subp
from json import dump
from json import load
from random import choice

url = "https://apidgp-gameplayer.games.dmm.com/v5/launch/cl"
myobj = {"product_id":"umamusume",
        "game_type":"GCL",
        "game_os":"win",
        "launch_type":"LIB",
        "mac_address":"",
        "hdd_serial":"",
        "motherboard":"",
        "user_os":"win"}

__PRGLOC,__LSECID,__LSESID,__MAC,__HDD,__MBB = ["" for i in range(6)]


def myobj_upd():
    myobj["mac_address"] = values["MACADDR"]
    myobj["hdd_serial"] = values["HDDSERIAL"]
    myobj["motherboard"] = values["MBBSERIAL"]
    


def serialgen():
    a = [str(chr(i)) for i in range(97,123)] + [str(i) for i in range(10)]
    b = ""
    for i in range(64):
        b+=choice(a)
    return b
    
def macgen():
    a = [str(chr(i)) for i in range(97,103)] + [str(i) for i in range(10)]
    b = ""
    b+=choice(a)
    b+=choice(a)
    for i in range(5):
        b+=":"
        b+=choice(a)
        b+=choice(a)
    return b

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Location of umamusume.exe'),sg.Push(), sg.InputText(__PRGLOC,key="PRGLOC")],
            [sg.Text('login_secure_id'),sg.Push(), sg.InputText(__LSECID,key='LSECID')],
            [sg.Text('login_session_id'),sg.Push(), sg.InputText(__LSESID,key='LSESID')],
            [sg.Text('mac_address'),sg.Push(), sg.InputText(__MAC,key='MACADDR')],
            [sg.Text('hdd_serial'),sg.Push(), sg.InputText(__HDD,key='HDDSERIAL')],
            [sg.Text('motherboard'),sg.Push(), sg.InputText(__MBB,key='MBBSERIAL')],
            [sg.Button('Run'),sg.Button('Save'),sg.Button('Load'),sg.Button('Randomize'),sg.Push()] ]

keys = ["PRGLOC","LSECID","LSESID","MACADDR","HDDSERIAL","MBBSERIAL"]
# Create the Window
window = sg.Window('UMPD launcher', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Save":
        with open('save.json','w') as f:
            dump(values, f)
            f.close()
        sg.Popup("Saved as save.json")
        continue
    if event == "Load":
        try:
            with open('save.json','r') as f:
                sval = load(f)
                for key in keys:
                    window[key].update(sval[key])
                f.close()
                sg.Popup("Loaded save.json")
        except Exception as er:
            sg.Popup(str(er))
        continue
    if event == "Randomize":
        window["MACADDR"].update(macgen())
        window["HDDSERIAL"].update(serialgen())
        window["MBBSERIAL"].update(serialgen())
        continue
    # print('You entered ', values[0])
    print(values)
    myobj_upd()
    req = rq.post(url, json=myobj,cookies={"login_secure_id":values["LSECID"],"login_session_id":values["LSESID"]})
    try:
        print(req.json())
        e_args = req.json()['data']['execute_args']
        #print(e_args)
        subp.Popen([values["PRGLOC"],[e_args]])
        sg.Popup("Done!")
    except Exception as er:
        sg.Popup(str(er)+"\n"+str(req.json()['error']))
    #print(values)

window.close()
