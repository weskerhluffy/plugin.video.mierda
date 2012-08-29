# The documentation written by Voinage was used as a template for this addon
# http://wiki.xbmc.org/?title=HOW-TO_write_plugins_for_XBMC
#
# This addon is licensed with the GNU Public License, and can freely be modified
# http://www.gnu.org/licenses/gpl-2.0.html

#Info de debug http://wiki.xbmc.org/index.php?title=HOW-TO:Debug_Python_Scripts_with_Eclipse

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmcaddon
import weblogin, gethtml, os, zipfile, commands
from urllib2 import Request, urlopen, URLError, HTTPError
import logging
from HTMLParser import HTMLParser

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

def countdown(time_to_wait, title='', text=''):
    return do_xbmc_wait(time_to_wait, title, text)

def do_xbmc_wait(time_to_wait, title, text):
        req = auth(url)
        print 'esperando ' + str(time_to_wait) + ' segs'

        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create(title)

        secs = 0
        percent = 0
        increment = 100 / time_to_wait

        cancelled = False
        while secs < time_to_wait:
            secs = secs + 1
            percent = increment * secs
            secs_left = str((time_to_wait - secs))
            remaining_display = ' Espere ' + secs_left + ' segs descargando video...'
            pDialog.update(percent, ' ' + text, remaining_display)
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
                return buscar, conectado
        elif username != None and password != None:
                logged_in = weblogin.doLogin(cookiedir, username , password)
                if logged_in == False:
                    dialog = xbmcgui.Dialog()
                    dialog.ok(" Opciones avanzadas", "Los parametros incorrectos..")
                buscar = '<a href="(.+?)" class="download_premium_but"'
                conectado = True
                return buscar, conectado

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
        addDir("Caca", "http://movies.humexico.org/xbmc/seriesgen.php", 1, "")
        if porno == "1":
            addDir("Adultos", "http://movies.humexico.org/xbmc/adultosmoviesgen.php", 1, "")

def INDEX(url):
    try:
        url = url.replace(' ', '%20')
        modo = setmodo(url)
        req = auth(url)
        req.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
        link = req.open(url)
        link = link.read()
        match = re.compile('Title: <a href="(.+?)">(.+?)</a> <a href="(.+?)">.+?</a><br>').findall(link)
        for url, name, iconimage in match:
          url = url + '&user=' + usera
          url = url + '&poster=' + iconimage
          addDir(name, url, modo, iconimage)
    except URLError, e:
        print e.code
        if e.code == 401:
            dialog = xbmcgui.Dialog()
            dialog.ok("    Servicio Expirado", "Tu cuenta " + usera + " a vencido, por favor Renueva.")
            print "Tu cuenta esta vencida"    

def VIDEOLINKS(url, name):
    try:
        url = url.replace(' ', '%20')
        s = url
        list_s = s.split('poster=')
        resultado = '/'.join(list_s[1:])
        source = gethtml.get(url, usera, passa, cookiedir)
        buscar = busqueda(source)
        match = re.compile(buscar).findall(source)
        for url in match:
            if "http://dc" in buscar:
              url = "http://dc" + url
            else:
              pass
            addLink(name, url, resultado)
    except URLError, e:
        print e.code
        if e.code == 401:
            dialog = xbmcgui.Dialog()
            dialog.ok("    Servicio Expirado", "Tu cuenta " + usera + " a vencido, por favor Renueva.")
            print "Tu cuenta esta vencida" 
                
def get_params():
        param = {}
        paramstring = sys.argv[2]
        if len(paramstring) >= 2:
                params = sys.argv[2]
                cleanedparams = params.replace('?', '')
                if (params[len(params) - 1] == '/'):
                        params = params[0:len(params) - 2]
                pairsofparams = cleanedparams.split('&')
                param = {}
                for i in range(len(pairsofparams)):
                        splitparams = {}
                        splitparams = pairsofparams[i].split('=')
                        if (len(splitparams)) == 2:
                                param[splitparams[0]] = splitparams[1]
                                
        return param



def addLink(name, url, iconimage):
        ok = True
        liz = xbmcgui.ListItem("Play", iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        liz.setProperty('IsPlayable', 'true')
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
        countdown(10, "Espere por Favor", "descargando video...")
        return ok

def addDir(name, url, mode, iconimage):
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
        return ok
        
        
####Clases


class ParserHTML(HTMLParser):
    logger = None
    def __init__(self, fh):
        """
        {fh} must be an input stream returned by open() or urllib2.urlopen()
        """
        HTMLParser.__init__(self)
        self.carpetas = {}
        self.feed(fh.read())
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger("ParserHTML")
        logger.debug("God bless")
    def handle_starttag(self, tag, attrs):
        archivo = ""
        carpeta = ""
        if tag == 'a' and attrs and len(attrs) == 1 and len(attrs[0]) == 2 and re.match(r".*S\d{2}E\d{2}.*", attrs[0][1]):
            logger.debug ("Found link => %s" % attrs[0][1])
            (carpeta, archivo) = re.sub(r"(.*)(S\d{2}E\d{2}).*", r"\1|\2", attrs[0][1]).split("|")
            logger.debug("carpeta encontrada %s, archivo %s" % (archivo, carpeta))
            if not self.carpetas.has_key(carpeta):
                self.carpetas[carpeta] = {}
            self.carpetas[carpeta][archivo] = attrs[0][1]
      
        
####Constantes
REMOTE_DBG = True
URL_CACA = "http://peliculas.mine.nu:8080/TV-XVID/"
MODO_CARPETA = 0
MODO_ARCHIVO = 1

####Variables
#Inicializadas
modo = MODO_CARPETA
params = get_params()
url_plugin = sys.argv[0]
handle_xbmc = int(sys.argv[1])
#Sin inicializar
lineas_pagina = ()
logger = None
opener = None
pagina = None
parser_html = None
carpeta_li = None
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

#Inicializando logger
      
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mierda")
logger.debug("kussou rumba %s" % params)

if(len(params) > 0 and params["modo"]):
    modo = int(params["modo"], 0)

#FIXME: Guardar el objeto parser en session
opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
pagina = opener.open(URL_CACA)
parser_html = ParserHTML(pagina)

if (modo == MODO_CARPETA):

    
    for carpeta in parser_html.carpetas:
         carpeta_li = xbmcgui.ListItem(carpeta.replace(".", " "), iconImage="DefaultFolder.png", thumbnailImage="")
         carpeta_li.setInfo(type="Video", infoLabels={ "Title": carpeta.replace(".", " ") })
         xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="%s?carpeta=%s&modo=%d" % (url_plugin, carpeta, MODO_ARCHIVO) , listitem=carpeta_li, isFolder=True)
else:
    for archivo in parser_html.carpetas[params["carpeta"]]:
        carpeta_li = xbmcgui.ListItem(archivo, iconImage="DefaultFolder.png", thumbnailImage="")
        carpeta_li.setInfo(type="Video", infoLabels={ "Title": archivo })
        logger.debug("La url a la que e hara la peticion es " + URL_CACA + params["carpeta"])
#        xbmcplugin.addDirectoryItem(handle=handle_xbmc, url=URL_CACA + params["carpeta"] , listitem=carpeta_li, isFolder=False)
        xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="http://peliculas.mine.nu:8080/TV-XVID/The.Simpsons.S22E17.HDTV.XviD-LOL/Sample/the.simpsons.2217.hdtv-lol-sample.avi" , listitem=carpeta_li, isFolder=False)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
