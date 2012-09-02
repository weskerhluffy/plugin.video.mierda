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
import math
import threading  
import random
import socket
import time
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
            
class HiloDialogo(threading.Thread):  
    logger = None
    def __init__(self, time_to_wait, title, text):  
          threading.Thread.__init__(self)  
          logging.basicConfig(level=logging.DEBUG)
          logger = logging.getLogger("HiloDialogo")
          logger.debug("Aventanto dialogo")
          self.time_to_wait = time_to_wait
          self.title = title
          self.text = text

    
    def run(self):  
            logger.debug('esperando ' + str(self.time_to_wait) + ' segs')
    
            pDialog = xbmcgui.DialogProgress()
            ret = pDialog.create(self.title)
    
            secs = 0
            percent = 0
            increment = 100 / self.time_to_wait
    
            cancelled = False
            while secs < self.time_to_wait:
                secs = secs + 1
                percent = increment * secs
                secs_left = str((self.time_to_wait - secs))
                remaining_display = ' Espere ' + secs_left + ' segs descargando video...'
                pDialog.update(percent, ' ' + self.text, remaining_display)
                xbmc.sleep(1000)
                if (pDialog.iscanceled()):
                     cancelled = True
                     break
    
            if cancelled == True:
                 logger.debug('espera cancelada')
            else:
                 logger.debug('Fin de la espera')
             
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
 
 
 
def dialogo_loading(time_to_wait, title, text):
        logger.debug('esperando ' + str(time_to_wait) + ' segs')

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
             logger.debug('espera cancelada')
             return False
        else:
             logger.debug('Fin de la espera')
             return True

def calcular_velocidad_internet():
    URL_PAG_VELOCIDAD = "http://testmy.net/results?align=&autoXi=&autoXiUL=&custom_packsize=&maxDFS=&maxUFS=&minDFS=&minUFS=&nfw=&noLoad=&noads=&nobar=&nobar=&out_size=&out_src=&out_url=&randGen=&smarTest=&special=1&ta=&test_type=download&test_type=download&testall=0&top=&ttime=Wed%20Aug%2029%202012%2023%3A43%3A58%20GMT-0500%20%28CDT%29&username=&x=5.072&xMes=2&z=3145728"
    velocidad = 0
    velocidad_str = ""
    lineas_pag_velocidad = []
    lineas_pag_velocidad = urllib.urlopen(URL_PAG_VELOCIDAD).read().split("\n")
    for linea_pag_velocidad in lineas_pag_velocidad:
#        logger.debug("Me corto las pelotas " + linea_pag_velocidad)
        if ("Your Speed ::" in linea_pag_velocidad):
            velocidad_str = re.sub(r".*Your Speed :: <span class=\"containerIndexX\"><font class=\"color\d+\">(\d+\.?\d*)</font>.*", r"\1", linea_pag_velocidad)
#                                      Your Speed :: <span class="containerIndexX"><font class="color22">5</font>
            logger.debug("La velocidad de internet es " + velocidad_str)
            velocidad = float(velocidad_str)
            velocidad *= 1000000
            break
    velocidad /= 8
    return velocidad

def calcular_total_a_bajar(url_descargas):
    total = 0
    tamano_archivo_txt = ""
    digitos_txt = ""
    factor_multiplicativo = ""
    tamano_archivo = 0
    lineas_pag_descargables = []
    lineas_pag_descargables = urllib.urlopen(url_descargas).read().split("\n")
    for linea_pag_descargables in lineas_pag_descargables:
#        logger.debug("La linea de descargables es " + linea_pag_descargables)
        if ("<tr><td valign=" in linea_pag_descargables and not "DIR" in linea_pag_descargables):
            tamano_archivo_txt = re.sub(r".*<td align=\"right\">\s*(\d+\.?\d*[MKG]?)\s*</td>.*", r"\1", linea_pag_descargables)
            logger.debug("El tamano del archivo %s", tamano_archivo_txt)
            (digitos_txt, factor_multiplicativo) = re.sub(r"(\d+\.?\d*)([MKG]?)", r"\1:\2", tamano_archivo_txt).split(":")
            tamano_archivo = float(digitos_txt)
            if(factor_multiplicativo == "K"):
                tamano_archivo *= 1000
            elif(factor_multiplicativo == "M"):
                tamano_archivo *= 1000000
            elif(factor_multiplicativo == "G"):
                tamano_archivo *= 1000000000
            else:
                tamano_archivo = tamano_archivo
            total += tamano_archivo
            logger.debug("El total en bytes %f" % tamano_archivo)
         
    return total

def get_urls_archivos(url_descargas):
    urls_archivos = []
    url_archivo = ""
    lineas_pag_descargables = []
    lineas_pag_descargables = urllib.urlopen(url_descargas).read().split("\n")
    for linea_pag_descargables in lineas_pag_descargables:
        if ("<tr><td valign=" in linea_pag_descargables and not "DIR" in linea_pag_descargables):
            url_archivo = re.sub(r".*href=\"(.+)\".*</a>.*", r"\1", linea_pag_descargables)
            logger.debug("La url del archivo es " + url_archivo)
            urls_archivos.append(url_archivo)
    return urls_archivos

####Constantes
REMOTE_DBG = False
URL_CACA = "http://antros.org.mx/videos/"
MODO_CARPETA = 0
MODO_ARCHIVO = 1
MODO_REPRODUCIR = 2

####Variables
#Inicializadas
modo = MODO_CARPETA
params = get_params()
url_plugin = sys.argv[0]
handle_xbmc = int(sys.argv[1])
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
hilo_dialogo = None
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

#Configurando el timeout de los socketes
socket.setdefaulttimeout(60)

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

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
elif (modo == MODO_ARCHIVO):
    archivo_persistencia = shelve.open("mierda")
    carpetas = archivo_persistencia["carpetas"] 
    
    
    for archivo in carpetas[params["carpeta"]]:
        carpeta_li = xbmcgui.ListItem(archivo, iconImage="DefaultFolder.png", thumbnailImage="")
        carpeta_li.setInfo(type="Video", infoLabels={ "Title": archivo })
        logger.debug("La url a la que e hara la peticion es " + URL_CACA + params["carpeta"])
        xbmcplugin.addDirectoryItem(handle=handle_xbmc, url="%s?carpeta=%s&archivo=%s&modo=%d" % (url_plugin, params["carpeta"] , archivo, MODO_REPRODUCIR) , listitem=carpeta_li, isFolder=False)
    
    archivo_persistencia.close()
   
    xbmcplugin.endOfDirectory(int(sys.argv[1]))   
else:
    archivo_persistencia = shelve.open("mierda")
    carpetas = archivo_persistencia["carpetas"]
    
    logger.debug("La carpeta es %s, el archivo es %s" % (params["carpeta"], params["archivo"]))
    url_descarga = URL_CACA + carpetas[params["carpeta"]][params["archivo"]]
    
    archivo_persistencia.close()
    
    
    logger.debug("Modo de reproduccion la url %s" % url_descarga)
#    velocidad_internet = calcular_velocidad_internet()
#    logger.debug("La velocidad de internet es %d" % velocidad_internet)
    total_a_descargar = calcular_total_a_bajar(url_descarga)
    logger.debug("El total a descargar es %d", total_a_descargar)
    urls_archivos_descargables = get_urls_archivos(url_descarga)
    
 #   hilo_dialogo = HiloDialogo(math.ceil(total_a_descargar / velocidad_internet + ((total_a_descargar * 0.1) / velocidad_internet)), "mierda", "caca")
 #   hilo_dialogo.start()
    
    #dialogo_loading(math.ceil(total_a_descargar / velocidad_internet + ((total_a_descargar * 0.1) / velocidad_internet)), "mierda", "caca")
    logger.debug("Empieza la descarga de poder")
    for url_archivo_descargable in urls_archivos_descargables:
        logger.debug("die die die my darling %s" % url_archivo_descargable)
#https://www.assembla.com/wiki/show/oniontv-plugin/Script_to_play_a_video_file_in_XBMC
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.add(url_descarga + url_archivo_descargable)
        xbmc.Player().play(playlist)
#        hilos_archivos_descargables.append(HiloDescarga(url_descarga + url_archivo_descargable))
#        hilos_archivos_descargables[-1].start()
    

