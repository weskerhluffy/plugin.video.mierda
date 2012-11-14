# The documentation written by Voinage was used as a template for this addon
# http://wiki.xbmc.org/?title=HOW-TO_write_plugins_for_XBMC
#
# This addon is licensed with the GNU Public License, and can freely be modified
# http://www.gnu.org/licenses/gpl-2.0.html

#Info de debug http://wiki.xbmc.org/index.php?title=HOW-TO:Debug_Python_Scripts_with_Eclipse

#Streams:
#http://livetvstreaming.ucoz.com/news/ooo_spanish_stream_vlc_ooo/2012-09-01-1815
#http://blog.felipebarriga.cl/linux/tv-chilena-online-para-linux/


import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmcaddon
import  os, zipfile, commands
from urllib2 import Request, urlopen, URLError, HTTPError
import logging
from HTMLParser import HTMLParser
import shelve
import math
import threading  
import random
import socket
import time
############VERSION#############

version = "0.1"

############VERSION#############

####Constantes
REMOTE_DBG = False
URL_CACA = "http://antros.org.mx/videos/"
URL_PELOS = "http://antros.org.mx/videos/XVID1/"
MODO_INICIAL = 0
MODO_CARPETA = 1
MODO_ARCHIVO = 2
MODO_LISTA_FLUJO = 3
MODO_FLUJO = 4
MODO_ACCESO_ARCHIVO = 5
MODO_LISTA_PELOS = 6
MODO_PELO = 7
#FIXME: Obtener nombre automaticamente
__plugin__ = "plugin.video.crapvideo"

####Variables globales
sys = None
xbmc = None
logger = None
addon = None        
####Clases


class ParserArchivos(HTMLParser):
    logger = None
    def __init__(self, fh):
        """
        {fh} must be an input stream returned by open() or urllib2.urlopen()
        """
        HTMLParser.__init__(self)
        
        self.carpetas = {}
        logging.basicConfig(level=logging.DEBUG)
        ParserArchivos.logger = logging.getLogger("ParserArchivos")
        ParserArchivos.logger.debug("God bless")
        self.feed(fh.read())

    def handle_starttag(self, tag, attrs):
        archivo = ""
        carpeta = ""
#FIXME: MAyusculas y minusculas del codigo S#E#
        if tag == 'a' and attrs and len(attrs) == 1 and len(attrs[0]) == 2 and re.match(r".*S\d{2}E\d{2}.*", attrs[0][1]):
            ParserArchivos.logger.debug("Found link => %s" % attrs[0][1])
            (carpeta, archivo) = re.sub(r"(.*)(S\d{2}E\d{2}).*", r"\1|\2", attrs[0][1]).split("|")
            ParserArchivos.logger.debug("carpeta encontrada %s, archivo %s" % (archivo, carpeta))
            if not self.carpetas.has_key(carpeta):
                self.carpetas[carpeta] = {}
            self.carpetas[carpeta][archivo] = attrs[0][1]
            
class ParserFlujos(HTMLParser):
    logger = None

    def __init__(self, fh):
        """
        {fh} must be an input stream returned by open() or urllib2.urlopen()
        """
        HTMLParser.__init__(self)
        self.contenido_li = False
        self.flujos = []
        logging.basicConfig(level=logging.DEBUG)
        ParserArchivos.logger = logging.getLogger("ParserFlujos")
        self.feed(fh.read())

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            logger.debug("Se encontro una cagada")
            self.contenido_li = True
    def handle_endtag(self, tag):
        if tag == 'li':
            logger.debug("Se termino una cagada")
            self.contenido_li = False
    def handle_data(self, data):
        if self.contenido_li:
            logger.debug("El contenido de esta mierda " + data)
            self.flujos.append(data.split(","))
            
class ParserPelos(HTMLParser):
    logger = None

    def __init__(self, fh):
        """
        {fh} must be an input stream returned by open() or urllib2.urlopen()
        """
        HTMLParser.__init__(self)
        self.contenido_li = False
        self.pelos = {}
        logging.basicConfig(level=logging.DEBUG)
        ParserPelos.logger = logging.getLogger("ParserPelos")
        self.feed(fh.read())

    def handle_starttag(self, tag, attrs):
#TODO: Agregar icono
        if tag == 'a' and attrs and len(attrs) == 1 and len(attrs[0]) == 2 and re.match(r".*\.[12][09][0-9][0-9]\..*", attrs[0][1]):
            ParserPelos.logger.debug("Found link pelo => %s" % attrs[0][1])
            pelo = re.sub(r"(.*)\.[12][09][0-9][0-9]\..*", r"\1", attrs[0][1])
            ParserPelos.logger.debug("pelo encontrado %s con link %s" % (pelo, attrs[0][1]))
            self.pelos[pelo] = attrs[0][1]
            
class HiloDescarga(threading.Thread):  
    logger = None

    def __init__(self, url_a_bajar):  
          threading.Thread.__init__(self)  
          logging.basicConfig(level=logging.DEBUG)
          logger = logging.getLogger("HiloDescarga")
          logger.debug("Aventanto hilo de descarga")
          HiloDescarga.logger = logger
          self.url_a_bajar = url_a_bajar
    
    def run(self):  
        nombre_archivo = ""
        intentos = 0
        tiempo_dormir = 0
        logger = HiloDescarga.logger
        logger.debug("DEscargando archivo " + self.url_a_bajar)
        
        while (nombre_archivo == "" and intentos < 3):
            logger.debug("Intentando bajara archuvi %s" % self.url_a_bajar)
            try:
                nombre_archivo = urllib.urlretrieve(self.url_a_bajar)[0]
                logger.debug("El archivo %s se ha descargado " % nombre_archivo)
            except IOError as ioe:
                logger.warn("Hubo un error de conexion %s a %s, reintentando" % (self.url_a_bajar, ioe))
            if(nombre_archivo == ""):
                tiempo_dormir = random.randint(1, 10)
                logger.warn("El hilo se dormira %d segundos para volver a intentar " % tiempo_dormir)
                time.sleep(tiempo_dormir)
                intentos += 1
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


def get_urls_archivos(url_descargas):
    urls_archivos = []
    url_archivo = ""
    lineas_pag_descargables = []
    lineas_pag_descargables = urllib.urlopen(url_descargas).read().split("\n")
    for linea_pag_descargables in lineas_pag_descargables:
        if ("<tr><td valign=" in linea_pag_descargables and not "DIR" in linea_pag_descargables):
            url_archivo = re.sub(r".*href=\"(.+)\".*</a>.*", r"\1", linea_pag_descargables)
#            logger.debug("La url del archivo es " + url_archivo)
            urls_archivos.append(url_archivo)
    return urls_archivos

def get_url_pelo(url_descargas):
    url_archivo = ""
    lineas_pag_descargables = []
    lineas_pag_descargables = urllib.urlopen(url_descargas).read().split("\n")
    for linea_pag_descargables in lineas_pag_descargables:
        if ("<tr><td valign=" in linea_pag_descargables and "[VID]" in linea_pag_descargables):
            url_archivo = re.sub(r".*href=\"(.+)\".*</a>.*", r"\1", linea_pag_descargables)
            logger.debug("La url del archivo es " + url_archivo)
            return url_archivo



####Main
def fuck (_sys, _xbmc):
####Variables
#Inicializadas
    global sys
    global xbmc
    global logger
    global addon
    sys = _sys
    xbmc = _xbmc
    modo = MODO_INICIAL
    params = get_params()
    url_plugin = sys.argv[0]
    handle_xbmc = int(sys.argv[1])
    addon = xbmcaddon.Addon(id=__plugin__)

    #Sin inicializar
    velocidad_internet = 0
    total_a_descargar = 0
    urls_archivos_descargables = []
    hilos_archivos_descargables = []
    logger = None
    opener = None
    pagina = None
    parser_html = None
    carpeta_li = None
    archivo_persistencia = None
    url_descarga = ""
    carpetas = {}
    
    # append pydev remote debuggerm
    if REMOTE_DBG:
        # Make pydev debugger works for auto reload.
        # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
        try:
            import pysrc.pydevd as pydevd
        # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
            pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True, port=5678)
        except ImportError:
            sys.stderr.write("Error: " + 
                "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
            sys.exit(1)
    
    #Inicializando logger
          
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("mierda")
 #   logger.debug("kussou rumba %s" % params)
    
    #Configurando el timeout de los socketes
    socket.setdefaulttimeout(60)
    
    if(len(params) > 0 and params["modo"]):
        modo = int(params["modo"], 0)
    
    
    if (modo == MODO_INICIAL):
        logger.debug("Modo inicial")
        carpeta_li = xbmcgui.ListItem("Series", iconImage="DefaultFolder.png", thumbnailImage="")
        carpeta_li.setInfo(type="Video", infoLabels={ "Title": "Series" })
        xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="%s?modo=%d" % (url_plugin, MODO_CARPETA) , listitem=carpeta_li, isFolder=True)
        
        carpeta_li = xbmcgui.ListItem("Canales", iconImage="DefaultFolder.png", thumbnailImage="")
        carpeta_li.setInfo(type="Video", infoLabels={ "Title": "Canales" })
        xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="%s?modo=%d" % (url_plugin, MODO_LISTA_FLUJO) , listitem=carpeta_li, isFolder=True)
        
        carpeta_li = xbmcgui.ListItem("Peliculas", iconImage="DefaultFolder.png", thumbnailImage="")
        carpeta_li.setInfo(type="Video", infoLabels={ "Title": "Peliculas" })
        xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="%s?modo=%d" % (url_plugin, MODO_LISTA_PELOS) , listitem=carpeta_li, isFolder=True)
        
        carpeta_li = xbmcgui.ListItem("Pagos por evento", iconImage="DefaultFolder.png", thumbnailImage="")
        carpeta_li.setInfo(type="Video", infoLabels={ "Title": "PPV" })
        xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="%s?modo=%d" % (url_plugin, MODO_INICIAL) , listitem=carpeta_li, isFolder=True)
    
    
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    elif (modo == MODO_CARPETA):
        logger.debug("Modo carpeta")

        opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        pagina = opener.open(URL_CACA)
        parser_html = ParserArchivos(pagina)
        
        archivo_persistencia = shelve.open("mierda")
        archivo_persistencia["carpetas"] = parser_html.carpetas
        archivo_persistencia.close()
        
        for carpeta in parser_html.carpetas:
             carpeta_li = xbmcgui.ListItem(carpeta.replace(".", " "), iconImage="DefaultFolder.png", thumbnailImage="")
             carpeta_li.setInfo(type="Video", infoLabels={ "Title": carpeta.replace(".", " ") })
             xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="%s?carpeta=%s&modo=%d" % (url_plugin, carpeta, MODO_ARCHIVO) , listitem=carpeta_li, isFolder=True)
    
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
    elif (modo == MODO_ARCHIVO):
        logger.debug("Modo archivo")

        archivo_persistencia = shelve.open("mierda")
        carpetas = archivo_persistencia["carpetas"] 
        
        
        for archivo in carpetas[params["carpeta"]]:
            carpeta_li = xbmcgui.ListItem(archivo, iconImage="DefaultFolder.png", thumbnailImage="")
            carpeta_li.setInfo(type="Video", infoLabels={ "Title": archivo })
            logger.debug("La url a la que e hara la peticion es " + URL_CACA + params["carpeta"])
            xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="%s?carpeta=%s&archivo=%s&modo=%d" % (url_plugin, params["carpeta"] , archivo, MODO_ACCESO_ARCHIVO) , listitem=carpeta_li, isFolder=False)
        
        archivo_persistencia.close()
       
        xbmcplugin.endOfDirectory(int(sys.argv[1]))   
    elif (modo == MODO_ACCESO_ARCHIVO):
        logger.debug("Modo acceso archivo")
        archivo_persistencia = shelve.open("mierda")
        carpetas = archivo_persistencia["carpetas"]
        
        logger.debug("La carpeta es %s, el archivo es %s" % (params["carpeta"], params["archivo"]))
        url_descarga = URL_CACA + carpetas[params["carpeta"]][params["archivo"]]
        
        archivo_persistencia.close()
        
        
        logger.debug("Modo de reproduccion la url %s" % url_descarga)
    
        urls_archivos_descargables = get_urls_archivos(url_descarga)
        
    
        
        logger.debug("Empieza la descarga de poder")
        for url_archivo_descargable in urls_archivos_descargables:
            logger.debug("die die die my darling %s" % url_archivo_descargable)
    #https://www.assembla.com/wiki/show/oniontv-plugin/Script_to_play_a_video_file_in_XBMC
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
            playlist.add(url_descarga + url_archivo_descargable)
            xbmc.Player().play(playlist)
    elif (modo == MODO_LISTA_FLUJO):
        logger.debug("Modo lista flujo")

#        logger.debug("Modo lista de flujos %s" % addon.getAddonInfo('path'))
        
        parser_html = ParserFlujos(open(addon.getAddonInfo('path') + "/plantillas_html/series.html", "r"))
        logger.debug("Los flujos encontrados son %s" % parser_html.flujos)
        
        for flujo in parser_html.flujos:
            carpeta_li = xbmcgui.ListItem(flujo[0], iconImage="DefaultFolder.png", thumbnailImage="")
            carpeta_li.setInfo(type="Video", infoLabels={ "Title": flujo[0] })
            logger.debug("La url a la que e hara la peticion es " + flujo[1])
            xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="%s?flujo=%s&modo=%d" % (url_plugin, flujo[1], MODO_FLUJO) , listitem=carpeta_li, isFolder=False)
        
        xbmcplugin.endOfDirectory(int(sys.argv[1]))   

    elif (modo == MODO_FLUJO):
        logger.debug("Modo   flujo")
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.add(params["flujo"])
        xbmc.Player().play(playlist)
    elif (modo == MODO_LISTA_PELOS):
        logger.debug("Modo lista pelos")
        
        opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        pagina = opener.open(URL_PELOS)
        parser_html = ParserPelos(pagina)
        
        for pelo in parser_html.pelos:
             carpeta_li = xbmcgui.ListItem(pelo.replace(".", " "), iconImage="DefaultFolder.png", thumbnailImage="")
             carpeta_li.setInfo(type="Video", infoLabels={ "Title": pelo.replace(".", " ") })
             xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="%s?carpeta=%s&modo=%d&url_pelo=%s" % (url_plugin, pelo, MODO_PELO, parser_html.pelos[pelo]) , listitem=carpeta_li, isFolder=True)
    
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    elif (modo == MODO_PELO):
        logger.debug("Modo pelo %s" % params["url_pelo"])
        
        url_archivo_descargable = get_url_pelo(URL_PELOS + params["url_pelo"])
        url_archivo_descargable = URL_PELOS + params["url_pelo"] + "/" + url_archivo_descargable
        
        logger.debug("die die die my darling %s" % url_archivo_descargable)
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.add(url_archivo_descargable)
        xbmc.Player().play(playlist)
        
        
    else:
        logger.error("Modo desconocido, abortando")
        sys.exit(1)

