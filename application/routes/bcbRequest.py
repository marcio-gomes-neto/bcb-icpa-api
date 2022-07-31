from flask import Blueprint, jsonify
from datetime import date, datetime
from application.repository.databaseService import Database
import requests

bcbRequestRoute = Blueprint('bcbRequest', __name__)
databaseService = Database()


@bcbRequestRoute.route('/bcb')
def index():
    return jsonify('BCB REQUESTS ROUTES')

@bcbRequestRoute.route('/bcb/getIpcaDataFromBcb')
def getAllIPCAData():
    today = date.today()
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial=01/01/1500&dataFinal=' + today.strftime("%d/%m/%Y")
    response = requests.get(url)
    return jsonify(response.json())

@bcbRequestRoute.route('/bcb/upsertIpcaData')
def upsertIpcaData():
    today = date.today()
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial=01/01/1500&dataFinal=' + today.strftime("%d/%m/%Y")

    response = requests.get(url)
    responseData = response.json()

    ipcaValues = databaseService.getAllIpcaValues()

    newValues = []
    for bcbIpcaData in responseData:
        add = True
        for dbIpcaValues in ipcaValues:
            if bcbIpcaData['data'] == dbIpcaValues['data']:
                add = False
        if add:
            newValues.append(bcbIpcaData)

    if len(newValues) > 0:
        databaseService.insertIpca(newValues)

    return jsonify('Added ' + str(len(newValues)) + ' new values')