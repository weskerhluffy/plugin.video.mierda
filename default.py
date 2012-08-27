# The documentation written by Voinage was used as a template for this addon
# http://wiki.xbmc.org/?title=HOW-TO_write_plugins_for_XBMC
#
# This addon is licensed with the GNU Public License, and can freely be modified
# http://www.gnu.org/licenses/gpl-2.0.html

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon
import weblogin,gethtml,os,zipfile,commands
from urllib2 import Request, urlopen, URLError, HTTPError


############VERSION#############

version = "1.55"

############VERSION#############




def getunzipped(theurl, thedir):
  name = os.path.join(thedir, 'temp.zip')
  try:
    name, hdrs = urllib.urlretrieve(theurl, name)
  except IOError, e:
    print "Can't retrieve %r to %r: %s" % (theurl, thedir, e)
    return
  try:
    z = zipfile.ZipFile(name)
  except zipfile.error, e:
    print "Bad zipfile (from %r): %s" % (theurl, e)
    return
  for n in z.namelist():
    dest = os.path.join(thedir, n)
    destdir = os.path.dirname(dest)
    if not os.path.isdir(destdir):
      os.makedirs(destdir)
    data = z.read(n)
    f = open(dest, 'w')
    f.write(data)
    f.close()
  z.close()
  os.unlink(name)

def countdown(time_to_wait,title='',text=''):
    return do_xbmc_wait(time_to_wait,title,text)

def do_xbmc_wait(time_to_wait,title,text):
        req = auth(url)
        print 'esperando '+str(time_to_wait)+' segs'

        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create(title)

        secs=0
        percent=0
        increment = 100 / time_to_wait

        cancelled = False
        while secs < time_to_wait:
            secs = secs + 1
            percent = increment*secs
            secs_left = str((time_to_wait - secs))
            remaining_display = ' Espere '+secs_left+' segs descargando video...'
            pDialog.update(percent,' '+text,remaining_display)
            xbmc.sleep(1000)
            if (pDialog.iscanceled()):
                 cancelled = True
                 break

        if cancelled == True:
             print 'espera cancelada'
             return False
        else:
             print 'Fin de la espera'
             return True
    

def START():
        if username == None and password == None:
                buscar = '<a href="(.+?)" class="download_regular_usual"'
                conectado = False
                if os.path.exists(cookiedel):
                        os.remove(cookiedel)
                return buscar,conectado
        elif username != None and password != None:
                logged_in = weblogin.doLogin(cookiedir, username , password)
                if logged_in == False:
                    dialog = xbmcgui.Dialog()
                    dialog.ok(" Opciones avanzadas", "Los parametros incorrectos..")
                buscar = '<a href="(.+?)" class="download_premium_but"'
                conectado = True
                return buscar,conectado

def auth(url):
    user = usera
    passw = passa
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, user, passw)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    return opener

def setmodo(url):     
        modo = 1
        if "moviesgen.php" in url:
            modo = 1
            return modo
        if "adultosmoviesgen.php" in url:
            modo = 1
            return modo
        elif "series.php" in url:
            modo = 1
            return modo
        elif "seriesgen.php" in url:
            modo = 1
            return modo
        elif "temporadas.php" in url:
            modo = 1
            return modo
        elif "seriescap.php" in url:
            modo = 2
            return modo
        elif "listado.php" in url:
            modo = 2
            return modo
        elif "adultoslistado.php" in url:
            modo = 2
            return modo

def busqueda(source):     
        buscar = ""
        if "regular" in source:
            buscar = '<a href="(.+?)" class="download_regular_usual"'
            return buscar
        elif "2shared.com" in source:
            buscar = '">http://dc(.+?)</div>'
            return buscar
        elif "Bayfiles" in source:
            buscar = '<a class="highlighted-btn" href="(.+?)">Download</a>'
            return buscar


def CATEGORIES(upmega):
        addDir("Peliculas", "http://movies.humexico.org/xbmc/moviesgen.php", 1, "")
        addDir("Series", "http://movies.humexico.org/xbmc/seriesgen.php", 1, "")
        if porno == "1":
            addDir("Adultos", "http://movies.humexico.org/xbmc/adultosmoviesgen.php", 1, "")

def INDEX(url):
    try:
        url=url.replace(' ','%20')
        modo = setmodo(url)
        req = auth(url)
        req.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
        link=req.open(url)
        link=link.read()
        match=re.compile('Title: <a href="(.+?)">(.+?)</a> <a href="(.+?)">.+?</a><br>').findall(link)
        for url, name, iconimage in match:
          url = url+'&user='+usera
          url = url+'&poster='+iconimage
          addDir(name,url,modo,iconimage)
    except URLError, e:
        print e.code
        if e.code == 401:
            dialog = xbmcgui.Dialog()
            dialog.ok("    Servicio Expirado", "Tu cuenta "+usera+" a vencido, por favor Renueva.")
            print "Tu cuenta esta vencida"    

def VIDEOLINKS(url,name):
    try:
        url=url.replace(' ','%20')
        s = url
        list_s = s.split('poster=')
        resultado = '/'.join(list_s[1:])
        source = gethtml.get(url,usera,passa,cookiedir)
        buscar = busqueda(source)
        match=re.compile(buscar).findall(source)
        for url in match:
            if "http://dc" in buscar:
              url = "http://dc"+url
            else:
              pass
            addLink(name,url,resultado)
    except URLError, e:
        print e.code
        if e.code == 401:
            dialog = xbmcgui.Dialog()
            dialog.ok("    Servicio Expirado", "Tu cuenta "+usera+" a vencido, por favor Renueva.")
            print "Tu cuenta esta vencida" 
                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param



def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem("Play", iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        countdown(10,"Espere por Favor","descargando video...")
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        

REMOTE_DBG = True 

# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)

      
params=get_params()
url=None
name=None
mode=None
username=None
password=None
upmega=None
conectado = False
buscar = ""
cookiedir="/var/mobile/Library/Preferences/XBMC/addons/plugin.video.megafilms"
cookiedel = os.path.join(cookiedir,'cookies.lwp')
upurl = "http://home.humexico.org/upmega.zip"

folder = os.path.dirname(cookiedir)
if not os.path.exists(folder):
  cookiedir=os.getcwd()
  cookiedel=cookiedir+"\cookies.lwp"
  print "Detectando que no es un appletv cambiando ruta de cookies"
  print cookiedir
else:
  print "Dejando el cookie path appletv satisfactoriamente detectado"
  print cookiedir

print "Cookiedel: " + cookiedel

#check if user has enabled use-login setting
usrsettings = xbmcaddon.Addon(id="plugin.video.megafilms")
use_account = usrsettings.getSetting('use-account')
use_accountmega = usrsettings.getSetting('use-accountmega')
upmega_yes = usrsettings.getSetting('upmega')

if upmega_yes == 'true':
     upmega = usrsettings.getSetting('upmega')

if use_account == 'true':
     username = usrsettings.getSetting('username')
     password = usrsettings.getSetting('password')
     hidesucces = usrsettings.getSetting('hide-successful-login-messages')
     ##Eliminar esto para la proxima version##
     if os.path.exists(cookiedel):
       os.remove(cookiedel)
       print "borrando cookies: "+ cookiedel
     ##Eliminar esto para la proxima version##
if use_accountmega == 'true':
     usera = usrsettings.getSetting('usernamemega')
     passa = usrsettings.getSetting('passwordmega')

############Version y Adultos#################
f = urllib.urlopen("http://www.megafilms.org/opcio.php?user="+usera)
adultos = f.read()
f.close()
adu = len("adultos=")
#print "adultos: ",adultos[adu]
versionscan = adu + len("<br>version=") + 1
#print "version: ",adultos[versionscan:versionscan+4]
versioncurrent = adultos[versionscan:versionscan+4]
cort = versionscan + len("<br>cortesia=") + 1 + 3
#print "cortesia: ",adultos[cort]

if version >= versioncurrent:
    print "estamos en la version correcta"
else:
    print "no estamos en la version correcta, actualizando.."
    print "version nueva: " + versioncurrent
    print os.getcwd()
    print "Bajando actualizacion.."
    getunzipped(upurl,cookiedir)
    dialog = xbmcgui.Dialog()
    dialog.ok("Version Incorrecta", "Nueva Actualizacion Encontrada - Descargando...\nNueva version: "+versioncurrent+" - Reinicia MegaFilms porfavor.")
    #xbmc.restart()

porno = adultos[adu]
cortesia = adultos[cort]
print porno + " " + version + " " + cortesia
############Version y Adultos#################

#buscar,conectado=START()
print "hide: ",upmega

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        #print "buscar: ",buscar
        #print "conectado: ", conectado
        CATEGORIES(upmega)
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)

elif mode==3:
        print "Bajando actualizacion.."
        getunzipped(upurl,cookiedir)
        dialog = xbmcgui.Dialog()
        dialog.ok("Descargando Actualizacion...", "Actualizacion descargada reiniciar MegaFilms")

xbmcplugin.endOfDirectory(int(sys.argv[1]))
