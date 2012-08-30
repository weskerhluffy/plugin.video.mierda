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
import shelve

############VERSION#############

version = "0.1"

############VERSION#############








        
        
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
            
            
####Funciones
                
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
archivo_persistencia = None
carpetas = {}
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



if (modo == MODO_CARPETA):
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    pagina = opener.open(URL_CACA)
    parser_html = ParserHTML(pagina)
    
    archivo_persistencia = shelve.open("mierda")
    archivo_persistencia["carpetas"] = parser_html.carpetas
    archivo_persistencia.close()
    
    for carpeta in parser_html.carpetas:
         carpeta_li = xbmcgui.ListItem(carpeta.replace(".", " "), iconImage="DefaultFolder.png", thumbnailImage="")
         carpeta_li.setInfo(type="Video", infoLabels={ "Title": carpeta.replace(".", " ") })
         xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="%s?carpeta=%s&modo=%d" % (url_plugin, carpeta, MODO_ARCHIVO) , listitem=carpeta_li, isFolder=True)
else:
    archivo_persistencia = shelve.open("mierda")
    carpetas = archivo_persistencia["carpetas"] 
    
    
    for archivo in carpetas[params["carpeta"]]:
        carpeta_li = xbmcgui.ListItem(archivo, iconImage="DefaultFolder.png", thumbnailImage="")
        carpeta_li.setInfo(type="Video", infoLabels={ "Title": archivo })
        logger.debug("La url a la que e hara la peticion es " + URL_CACA + params["carpeta"])
#        xbmcplugin.addDirectoryItem(handle=handle_xbmc, url=URL_CACA + params["carpeta"] , listitem=carpeta_li, isFolder=False)
        xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="http://peliculas.mine.nu:8080/TV-XVID/The.Simpsons.S22E17.HDTV.XviD-LOL/Sample/the.simpsons.2217.hdtv-lol-sample.avi" , listitem=carpeta_li, isFolder=False)
    
    archivo_persistencia.close()
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
