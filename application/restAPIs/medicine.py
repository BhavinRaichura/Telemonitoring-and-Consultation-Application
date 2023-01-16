from application.restAPIs import api

from flask_restful import Resource
import pandas as pd


df = pd.read_csv('/home/bhavin/Desktop/tmcs (copy)/application/static/csv-files/TM_2021.csv')
df.drop(index=1, axis=0, inplace=True)
dic = df.to_dict()


class Meddata(Resource):
    def get(self,medicine_name):
        datas = df.loc[df['Medication_Name'].str.contains(medicine_name, case=False)]
        return datas.head().reset_index().to_dict(orient='index')
    
    def post(self):
        pass
    
    def get(self):
        pass
    
api.add_resource(Meddata,"/api/medicine/<string:medicine_name>")

