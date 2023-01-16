from application.restAPIs import api

from flask_restful import Resource
import pandas as pd


class UserData(Resource):
    def get(self,medicine_name):
        datas = df.loc[df['Medication_Name'].str.contains(medicine_name, case=False)]
        return datas.reset_index().to_dict(orient='index')
    
    def post(self):
        pass
    
    def put(self):
        pass
    
    def delete(self):
        pass
    
api.add_resource(UserData,"/api/medicine/<string:USER_ID>")
