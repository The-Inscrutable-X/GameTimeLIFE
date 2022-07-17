#Name: Honer
from tree import *
import PySimpleGUI as sg
import os

try:
  # Root.kjhdkjberesifduhk() #this creates an error
  Root = load_json_tree()
except:
  Root = GXP('root', 0)
  Root.insert(('technical', 100)).insert(('programming', 100), ('engineering', 200), ('physics', 300), ('maths', 400))
  Root.insert(('meditation', 30)).insert(('art', 20),('music', 10))
  Root.save()

print('examine0', Root.get_cached_xp(), Root.get_stacked_xp(), Root.xp)
# Root.find('art').delete()
print('examine1', Root.get_cached_xp())
print(print_xp_tree(Root))



sg.theme('Light Green 6')
layout = [
  [sg.Text('Create An Event', key='text')],
  [sg.Text(print_xp_tree(Root), key='tree_text')],
  [sg.Text('Event_Name'), sg.InputText(key="Event_Name")],
  [sg.Text('Event_Category'), sg.InputText(key="Event_Category")],
  [sg.Text('Event_XP'), sg.InputText(key="Event_XP")],
  [sg.Button('Ok')]
]
window = sg.Window('GameTimeBasicGui', layout=layout, finalize=True)

state = 'create_event'
while True:
  event, values = window.read()
  if event == 'End' or event == sg.WIN_CLOSED:
    break

  if state == 'create_event':
    if event == 'Ok':
      # print(values['Event_Name'], values['Event_Category'], values["Event_XP"])
      try:
        name =  values['Event_Name']
        parent =  values['Event_Category']
        xp = int(values["Event_XP"]) 
        Root.find(parent).insert((name,xp))
        window['tree_text'].update(print_xp_tree(Root))
        Root.save()
      except Exception as e:
        print('Invalid entries inputted')
        event = 'End'
        print('Exception is: {}'.format(e))
        raise(e)
        break

  
window.close()
"""
├─┬┐
└┐││
│└┬┐
├┐││
"""

