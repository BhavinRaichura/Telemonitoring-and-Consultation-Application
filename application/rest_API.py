from application import api
from flask_restful import Resource


class API_Medicine_data(Resource):
    
    def __init__(self):
        pass

    def get(self,med):
        dic={}
        dic['asdf']=22
        return dic[med]
    
    def post(self,USER_ID, MEETING_ID, MED_ID):
        pass
    
    def delete(self, USER_ID,MEETING_ID, MED_ID):
        pass



class API_patient_history(Resource):
    def __init__(self, user):
        self.USER_ID = user
    
    def get(self):
        pass




api.add_resource(API_Medicine_data, '/api/medicine-list/<string:med>/')
api.add_resource(API_patient_history, '/api/patient-history/<string:user>/')

