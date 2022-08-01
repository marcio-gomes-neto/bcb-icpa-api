from flask import Blueprint, jsonify, request, Response
from flask_cors import cross_origin
from datetime import date, datetime
from application.repository.databaseService import Database
import requests
import io
import xlwt

ipcaRequestRoute = Blueprint('ipcaRequest', __name__)
databaseService = Database()

@ipcaRequestRoute.route('/ipca/getIpcaValues')
@cross_origin(supports_credentials=True)
def getIpcaValues():
    args = request.args
    finalDate = args.get('finalDate')
    startDate = args.get('startDate')
    format = args.get('format')

    if None in (finalDate, startDate, format):
        return jsonify("finalDate, startDate and format cannot be null"), 400
    if format != 'json' and 'excel':
        return jsonify("format must be json or excel"), 400

    try:
        finalDate = datetime.strptime(finalDate, "%d/%m/%Y")
        startDate = datetime.strptime(startDate, "%d/%m/%Y")
    except ValueError:
        return jsonify("finalDate and startDate must be in dd/mm/yyyy format"), 400

    delta = finalDate - startDate
    if delta.days > 365:
        return jsonify("IPCA search cannot be higher than 1 year"), 400
    if finalDate < startDate:
        return jsonify("finalDate cannot be lower than startDate"), 400

    ipcaValues = databaseService.findWithDateRange(startDate, finalDate)

    if format == 'json':
        return jsonify({'values': ipcaValues, 'type': 'json', 'startDate': startDate, 'finalDate': finalDate})

    if format == 'excel':
        return jsonify({'values': ipcaValues, 'type': 'json', 'startDate': startDate, 'finalDate': finalDate})

@ipcaRequestRoute.route('/ipca/downloadExcel')
@cross_origin(supports_credentials=True)
def excelDownload():
    args = request.args
    finalDate = args.get('finalDate')
    startDate = args.get('startDate')

    finalDate = datetime.strptime(finalDate, "%d/%m/%Y")
    startDate = datetime.strptime(startDate, "%d/%m/%Y")

    ipcaValues = databaseService.findWithDateRange(startDate, finalDate)

    output = io.BytesIO()
    workbook = xlwt.Workbook()
    sh = workbook.add_sheet('IPCA Report')

    sh.write(0, 0, 'IPCA DATE')
    sh.write(0, 1, 'IPCA VALUE')

    idx = 0
    for value in ipcaValues:
        sh.write(idx+1, 0, str(value['data']))
        sh.write(idx+1, 1, str(value['valor']))
        idx += 1

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition": "attachment;filename=ipca_report.xls"})


@ipcaRequestRoute.route('/ipca/downloadJson')
@cross_origin(supports_credentials=True)
def JSONDownload():
    args = request.args
    finalDate = args.get('finalDate')
    startDate = args.get('startDate')

    finalDate = datetime.strptime(finalDate, "%d/%m/%Y")
    startDate = datetime.strptime(startDate, "%d/%m/%Y")

    ipcaValues = databaseService.findWithDateRange(startDate, finalDate)

    return Response(str(ipcaValues), mimetype='application/json', headers={'Content-Disposition': 'attachment;filename=ipca_report.json'})