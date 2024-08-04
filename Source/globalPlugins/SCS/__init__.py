#The part that turns off the role announcement is a huge hack, and might break. Set this to False to get rid of it
lastRole=0
hook = True
is_exp=False
import api
import IAccessibleHandler
import time
from NVDAObjects import IAccessible
import os
from . import k
from . import bass
import controlTypes
import globalPluginHandler
import speech
import config
import ui
module_dir = os.path.abspath(os.path.dirname(__file__))
module_di = os.path.abspath(os.path.dirname(__file__))

from . import objdata
loc = os.path.abspath(os.path.dirname(objdata.__file__))
try:
 fconf=open(os.path.join(module_dir, "screenreadersounds.conf"), "r")
 this=int(fconf.read())
 fconf.close()
except:
 fconf=open(os.path.join(module_dir, "screenreadersounds.conf"), "w")
 this=0
 fconf.write("0")
 fconf.close()
if this==0:
        from . import objdata
        module_dir = os.path.abspath(os.path.dirname(__file__))
        loc = os.path.abspath(os.path.dirname(objdata.__file__))
elif this==1:
        from . import talkback
        from .talkback import one
        from .talkback.one import objdata
        module_dir = os.path.abspath(os.path.dirname(__file__)) + "/talkback/one/"
        loc = os.path.abspath(os.path.dirname(objdata.__file__))
elif this==2:
        from . import talkback
        from .talkback import two
        from .talkback.two import objdata
        module_dir = os.path.abspath(os.path.dirname(__file__)) + "/talkback/two/"
        loc = os.path.abspath(os.path.dirname(objdata.__file__))
old = None

soundTab = os.path.join(module_dir, "Tab.wav")
soundShiftTab = os.path.join(module_dir, "ShiftTab.wav")
soundClicked = os.path.join(module_dir, "clicked.wav")
media = os.path.join(module_dir, "media.wav")
soundScroll = os.path.join(module_dir, "scroll.wav")
soundChar=os.path.join(module_dir, "typekey.wav")
soundSpace=os.path.join(module_dir, "typekeyspace.wav")
pr=os.path.join(module_dir, "typekeypr.wav")
closed=os.path.join(module_dir, "closed.wav")
opened=os.path.join(module_dir, "opened.wav")
notext=os.path.join(module_dir, "notext.wav")
collapsed=os.path.join(module_dir, "collapsed.wav")
expanded=os.path.join(module_dir, "expanded.wav")
ec=os.path.join(module_dir, "eclose.wav")
delete=os.path.join(module_dir, "typekeyremove.wav")
lock=os.path.join(module_dir, "lock.wav")
lockscreen=os.path.join(module_dir, "lockscreen.wav")
unlockscreen=os.path.join(module_dir, "unlockscreen.wav")
error=os.path.join(module_dir, "error.wav")
end=os.path.join(module_dir, "end.wav")
is_set=False
def getSpeechTextForProperties2(reason=controlTypes.OutputReason, *args, **kwargs):
 role = kwargs.get('role', None)
 if 'role' in kwargs and role in sounds and os.path.exists(sounds[role]):
  del kwargs['role']
 return old(reason, *args, **kwargs)

def play(role):
 """plays sound for role."""
 f = sounds[role]
 if os.path.exists(f):
  bass.play(f)

#Add all the roles, looking for name.wav.
sounds = {}
for role in [x for x in dir(controlTypes) if x.startswith('ROLE_')]:
 r = os.path.join(loc, role[5:].lower()+".wav")
 sounds[getattr(controlTypes, role)] = r
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
 def __init__(self, *args, **kwargs):
  globalPluginHandler.GlobalPlugin.__init__(self, *args, **kwargs)
  global old
  try:
   old = speech.getSpeechTextForProperties
  except:
   old = speech.getPropertiesSpeech

  if 'objsounds' not in config.conf:

   config.conf['objsounds'] = {"enabled": True}
 def event_typedCharacter(self, obj, nextHandler, ch):
  global lastRole
  if config.conf['objsounds']['enabled'] == u'False' or config.conf['objsounds']['enabled'] == False:
   nextHandler()
   return
  if hook:
   if obj.role==controlTypes.Role.LIST or obj.role==controlTypes.Role.TREEVIEW:
    if k.is_pressed("right") or k.is_pressed("left") or k.is_pressed("down") or k.is_pressed("up"):
     bass.play(error)
   if obj.role==controlTypes.Role.BUTTON or obj.role==controlTypes.Role.CHECKBOX or obj.role==controlTypes.Role.TOGGLEBUTTON or obj.role==controlTypes.Role.MENUITEM or obj.role==controlTypes.Role.LISTITEM:
    if k.is_pressed("space") or k.is_pressed("enter"):
     bass.play(soundClicked)
   if obj.role==controlTypes.Role.EDITABLETEXT:
    if k.is_pressed("space"):
     bass.play(soundSpace)
    if k.is_pressed("up")or k.is_pressed("down"):
     bass.play("objdata/listitem.wav")

    if ord(ch)==8 or ord(ch)==127:
     bass.play(delete)
    if ord(ch)==36 or ord(ch)==35:
     bass.play(end)


    if ord(ch)>=32 and os.path.isfile(soundChar):
     if obj.states==controlTypes.State.PROTECTED:
      bass.play(pr)
      return
     bass.play(soundChar)
  lastRole=obj.role
  nextHandler()


 def event_gainFocus(self, obj, nextHandler):
  global is_exp
  global lastRole
  global is_set
  ##huge hack. Why is configobj not saving the boolean as a boolean?
  if config.conf['objsounds']['enabled'] == u'False' or config.conf['objsounds']['enabled'] == False:
   nextHandler()
   return

  if hook:
   if obj.appModule.appName=="explorer":
    if is_exp==False:
     bass.play(opened)
     is_exp=True
   else:
    if is_exp==True:
     bass.play(closed)
     is_exp=False
   if lastRole==controlTypes.Role.EDITABLETEXT or lastRole==controlTypes.Role.DOCUMENT:
    bass.play(ec)
   elif lastRole==controlTypes.Role.TREEVIEW:
    bass.play(collapsed)
   speech.getSpeechTextForProperties = getSpeechTextForProperties2
  if obj.role==controlTypes.Role.TREEVIEWITEM or obj.role==controlTypes.Role.MENUITEM:
    if k.is_pressed("right"):
     bass.play(expanded)
    elif k.is_pressed("left"):
     bass.play(collapsed)
  if k.is_pressed("right")or k.is_pressed("down"):
   bass.play(soundTab)
  elif k.is_pressed("left")or k.is_pressed("up"):
   bass.play(soundShiftTab)
  elif k.is_pressed("page_up")or k.is_pressed("page_down"):
   bass.play(soundScroll)
   nextHandler()
   return
  if k.is_pressed("home")or k.is_pressed("end"):
   bass.play(end)
   nextHandler()
   return

  if obj.name=='' or obj.name==None:
   bass.play(notext)
#  if isinstance(obj, IAccessibleHandler.SecureDesktopNVDAObject):
#   lastRole=3591
#   bass.play(lock)
#   time.sleep(0.300)
#   bass.play(lockscreen)
#   return
  play(obj.role)
  if lastRole==3591:
   bass.play(unlockscreen)
  lastRole=obj.role
  nextHandler()
  if hook:

   try:
    speech.getSpeechTextForProperties = old
   except:
    speech.getPropertiesSpeech = old


 def script_toggle(self, gesture):
  config.conf['objsounds']['enabled'] = not (str2bool(config.conf['objsounds']['enabled']))
  if config.conf['objsounds']['enabled']:
   ui.message(_("on"))
  else:
   k.remove_all_hotkeys()

   ui.message(_("off"))
  print(config.conf['objsounds']['enabled'])
  
 def script_thb(self, gesture):
    global this
    if this > 0:
        this -= 1
        update_conf_file(module_di, this)
    if this==0:
        ui.message("Apple VoiceOver")
    elif this==1:
        ui.message("Google TalkBack 5.0.7")
    elif this==2:
        ui.message("Google TalkBack 6+")

 def script_thn(self, gesture):
    global this
    if this < 2:
        this += 1
        update_conf_file(module_di, this)
    if this==0:
        ui.message("Apple VoiceOver")
    elif this==1:
        ui.message("Google TalkBack 5.0.7")
    elif this==2:
        ui.message("Google TalkBack 6+")
 __gestures = {
  "kb:NVDA+Alt+O": "toggle",
  "kb:NVDA+Alt+Z": "thb",
  "kb:NVDA+Alt+X": "thn",

 }

def str2bool(s):
 if s == 'True' or s == True: return True
 if s == 'False' or s == False: return False
def update_conf_file(module_di, this):
    with open(os.path.join(module_di, "screenreadersounds.conf"), "w+") as fconf:
        fconf.write(str(this))