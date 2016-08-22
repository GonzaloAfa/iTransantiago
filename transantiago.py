# -*- coding: utf-8 -*-
import time, urllib, urllib2, json

url = 'http://www.transantiago.cl/predictor/prediccion?'
urlLocation = 'http://www.transantiago.cl/restservice/rest/getpuntoparada?'

def getParada(bot, cid, parada):

    req = urllib2.Request(url + 'codsimt='+str(parada))
    response = urllib2.urlopen(req)

    if response.code == 200:

        data = json.loads(response.read())
        response.close()

        text = ''

        if data[u'respuestaParadero'] == 'Paradero invalido.':
            text = "Paradero invalido."
        else:
            for item in data['servicios']['item']:
                text = text + item['servicio']+ "\n"

                if item['respuestaServicio'] == u'Fuera de horario de operacion para este paradero':
                    text = text + "Fuera de horario \n"
                else:
                    if item['respuestaServicio'] ==  u'No hay buses que se dirijan al paradero.':
                        text = text + 'No hay buses \n'
                    else:
                        text = text + item['horaprediccionbus1']+" "+ item['distanciabus1']+" m \n"

                        if item['codigorespuesta'] == '00':
                            text = text + item['horaprediccionbus2']+" "+ item['distanciabus2']+" m \n"
        print text
        bot.send_message(cid, text)

    elif response.code == 500:
        bot.send_message(cid, 'Tenemos dificultades técnicas... un gatito moridó los cables del servidor')


def getLocationParada(bot, cid, lat, lon):

    print urlLocation+'lat='+str(lat)+'&lon='+str(lon)+'&bip=0'
    req = urllib2.Request(urlLocation+'lat='+str(lat)+'&lon='+str(lon)+'&bip=0')
    response = urllib2.urlopen(req)

    if response.code == 200:

        for item in json.loads(response.read()):

            if item[u'distancia'] < 0.3:

                print (item[u'name']).encode('utf-8')

                bot.send_message(cid, "Parada "+str(item[u'cod'])+" "+(item[u'name']).encode('utf-8'))
                bot.send_location(cid, item[u'pos'][0], item[u'pos'][1])

            else:
                print "La parada "+ str(item[u'cod']) +" está muy lejos"

        bot.send_message(cid, 'Estas son todas las paradas')
        response.close()

    if response.code == 500:
        bot.send_message(cid, 'Se cayó el... oh! una ʕ•́ᴥ•̀ʔっ ')
