from pymongo import MongoClient
from flask import jsonify
from datetime import datetime

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://admin:admin@cursojs.awfzm.mongodb.net/?retryWrites=true&w=majority")
        self.ipcaCollection = self.client["fullstack-challenge"]["ipca"]

    def getAllIpcaValues(self):
        ipcaValues = self.ipcaCollection.find({}, {"_id": 0, "data": 1, "valor": 1})
        response = []
        for ipca in ipcaValues:
            response.append(ipca)

        return response

    def insertIpca(self, values):
        response = self.ipcaCollection.insert_many(values)
        return response

    def findWithDateRange(self, startDate, finalDate):
        allIpcaValues = self.ipcaCollection.find({}, {"_id": 0, "data": 1, "valor": 1})
        response = []
        for value in allIpcaValues:
            if startDate <= datetime.strptime(value['data'], "%d/%m/%Y") <= finalDate:
                value['valor'] = value['valor'].replace('-', '')
                response.append(value)

        return response
