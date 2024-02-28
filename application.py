from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required
from faker import Faker
import random
import os
from flask_cors import CORS
from flask import current_app


from flask import Flask
import os
def create_app(config_name, settings_module='config.ProductionConfig'):
    app=Flask(__name__)
    app.config.from_object(settings_module)
    return app


settings_module = os.getenv('APP_SETTINGS_MODULE','config.ProductionConfig')
application = create_app('default', settings_module)
app_context=application.app_context()
app_context.push()




import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime, Date
from sqlalchemy.sql import func

db = SQLAlchemy()

db.init_app(application)
db.create_all()

CORS(application)


from datetime import datetime
from datetime import timedelta
import math
import random
import uuid
from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
#from candidato.modelos.modelos import db, Candidato, CandidatoSchema, Estado
from sqlalchemy import desc, asc

import os
import requests
import json
from faker import Faker

#################################################################################
######################################   AUTH   #################################
#################################################################################

class VistaSignIn(Resource):   
    def post(self):
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_AUTH']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, res_code

class VistaLogIn(Resource):
    def post(self):
        print("Gateway Login")
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_AUTH']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        if res_code==200:
            id_usuario=response.get("id")
            token=response.get("token")
            tipo=response.get("tipo")
            headers={'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}
            if tipo=='EMPRESA':
                path='/miempresa/'+str(id_usuario)
                response2, res_code2 = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{path}",
                                    headers=headers, tiempoespera=5000)
                if res_code2==200:
                    id_empresa=response2.get("id")
                    response["empresa"]=response2
            elif tipo=='CANDIDATO':
                print("tipo Candidato")
                path='/micandidato/'+str(id_usuario)
                response2, res_code2 = send_get_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                    headers=headers, tiempoespera=5000)
                print("tipo Candidato Despues")
                if res_code2==200:
                    id_candidato=response2.get("id")
                    response["candidato"]=response2
            return response, res_code                  
        else:
            print(response)
            return response, res_code

class VistaLogIn2(Resource):
    def post(self):
        print("Gateway Login")
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_AUTH']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        if res_code==200:
            id_usuario=response.get("id")
            token=response.get("token")
            headers={'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}
            path='/miempresa/'+str(id_usuario)
            response2, res_code2 = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{path}",
                                   headers=headers, tiempoespera=5000)
            if res_code2==200:
                id_empresa=response2.get("id")
                path='/empresas/'+str(id_empresa)+'/proyectos'
                response3, res_code3 = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{path}",
                                   headers=headers, tiempoespera=5000)
                if res_code3==200:
                    response2["proyectos"]=response3
                    response["empresa"]=response2
                else:
                    response["empresa"]=response2
                print(response)
                return response, res_code    
            else:
                print(response)
                return response, res_code
        else:
            print(response)
            return response, res_code
        
class VistaUsuario(Resource):   
    def get(self, id_usuario):
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_AUTH']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, res_code

    def put(self, id_usuario):
        headers=request.headers
        body=request.json
        response, res_code = send_put_request(url=f"{current_app.config['HOST_PORT_AUTH']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, res_code

    def delete(self, id_usuario):
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_AUTH']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, res_code

class VistaAuthorization(Resource):
    @jwt_required()
    def post(self):
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_AUTH']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, res_code
        

class VistaAuthPing(Resource):
    def get(self):
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_AUTH']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, res_code

#################################################################################
####################################   EMPRESAS   ###############################
#################################################################################

class VistaEmpresaUsuario(Resource):
    #@authorization_required()
    def get(self, id_usuario):
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, res_code

class VistaEmpresaDetalleUsuario(Resource):
    def get(self, id_usuario):
        print("Gateway Consultar Detalle Empresa de un Usuario")
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        print(response)
        return response, res_code

class VistaPerfilesStr(Resource):
    def post(self, id_proy):
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, res_code

class VistaPerfiles(Resource):
    def post(self, id_proy):
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, res_code
        
class VistaProyecto(Resource):
    def get(self, id_proy):
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, res_code

class  VistaEntrevistasCandidatos(Resource):
    def post(self, id_cand):
        print("Gateway: obteniendo las entrevistas de un Candidato")
        print("request.json")
        print(request.json)
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        if res_code==200:
            print("200")
            lstEV=response["Entrevistas"]
            lstCand=[]
            for e in lstEV:
                lstCand.append(e["id_cand"])
            if len(lstCand)!=0:
                headers={}
                body={"lstCandidatos":lstCand}
                path='/candidatos/lista'
                response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                       body=body, headers=headers, tiempoespera=5000)              
                if res_code2==200:
                    lstDetCandidatos=response2["lstDetCandidatos"]
                    for e in lstEV:
                        for c in lstDetCandidatos:
                            if e["id_cand"]==c["id"]:
                                e["candidato"]=c["nombres"] + " "+ c["apellidos"]
                print(response)
                return response, 200
            else:
                print(response)
                return response, 200
        else:
            print("Error")
            return response, res_code

    def get(self, id_cand):
        print("Gateway: GET. Obteniendo las entrevistas de un Candidato")
        print("request.json")
        print(request.json)
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        if res_code==200:
            print("200")
            lstEV=response["Entrevistas"]
            lstCand=[]
            for e in lstEV:
                lstCand.append(e["id_cand"])
            if len(lstCand)!=0:
                headers={}
                body={"lstCandidatos":lstCand}
                path='/candidatos/lista'
                response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                       body=body, headers=headers, tiempoespera=5000)              
                if res_code2==200:
                    lstDetCandidatos=response2["lstDetCandidatos"]
                    for e in lstEV:
                        for c in lstDetCandidatos:
                            if e["id_cand"]==c["id"]:
                                e["candidato"]=c["nombres"] + " "+ c["apellidos"]
                print(response)
                return response, 200
            else:
                print(response)
                return response, 200
        else:
            print("error")
            return response, res_code

class VistaEntrevistasEmpresas(Resource):
    def post(self, id_empresa):
        print("Gateway: obteniendo las entrevistas de una empresa")
        patron=request.json.get("candidato")
        print("--"+patron+"--")
        if patron!="":
            print("Patron <> Vacio")
            if patron=="NO ASIGNADO":
                lstNumCand=[0]
            else:
                headers=request.headers
                body={"patron": patron}
                responseX, res_codeX = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}/candidatos/like",
                                    body=body, headers=headers, tiempoespera=5000)
                if res_codeX==200:
                    lstNumCand=responseX["lstNumCandidatos"]
                else:
                    lstNumCand=[-1]
        else:
            print("Patron Vacio")
            lstNumCand=[-1]

        headers=request.headers
        body=request.json
        body["lstNumCand"]=lstNumCand
        print("Mensajes")
        print(body)
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 body=body, headers=headers, tiempoespera=5000)
        print("Despues")
        print(response)
        if res_code==200:
            lstEV=response["Entrevistas"]
            lstCand=[]
            for e in lstEV:
                lstCand.append(e["id_cand"])
            if len(lstCand)!=0:
                headers={}
                body={"lstCandidatos":lstCand}
                path='/candidatos/lista'
                response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                       body=body, headers=headers, tiempoespera=5000)              
                if res_code2==200:
                    lstDetCandidatos=response2["lstDetCandidatos"]
                    for e in lstEV:
                        for c in lstDetCandidatos:
                            if e["id_cand"]==c["id"]:
                                e["candidato"]=c["nombres"] + " "+ c["apellidos"]
                print(response)
                return response, 200
            else:
                print(response)
                return response, 200
        else:
            return response, res_code

class VistaLasEntrevistas(Resource):
    def post(self):
        print("Gateway: obteniendo todas las entrevistas")
        patron=request.json.get("candidato")
        if patron!="":
            if patron=="NO ASIGNADO":
                lstNumCand=[0]
            else:
                headers=request.headers
                body={"patron": patron}
                responseX, res_codeX = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}/candidatos/like",
                                    body=body, headers=headers, tiempoespera=5000)
                if res_codeX==200:
                    lstNumCand=responseX["lstNumCandidatos"]
                else:
                    lstNumCand=[-1]
        else:
            lstNumCand=[-1]

        headers=request.headers
        body=request.json
        body["lstNumCand"]=lstNumCand
        print("Mensajes")
        print(body)
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 body=body, headers=headers, tiempoespera=5000)
        print("Despues")
        print(response)
        if res_code==200:
            lstEV=response["Entrevistas"]
            lstCand=[]
            for e in lstEV:
                lstCand.append(e["id_cand"])
            if len(lstCand)!=0:
                headers={}
                body={"lstCandidatos":lstCand}
                path='/candidatos/lista'
                response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                       body=body, headers=headers, tiempoespera=5000)              
                if res_code2==200:
                    lstDetCandidatos=response2["lstDetCandidatos"]
                    for e in lstEV:
                        for c in lstDetCandidatos:
                            if e["id_cand"]==c["id"]:
                                e["candidato"]=c["nombres"] + " "+ c["apellidos"]
                print(response)
                return response, 200
            else:
                print(response)
                return response, 200
        else:
            return response, res_code

class VistaEntrevistas(Resource):
    def post(self):
        print("Gateway: creando entrevista")
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, res_code
    
    def get(self):
        print("Gateway: Obteniendo Todas Las Entrevistas")
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, res_code

class VistaEntrevistasPuesto(Resource):
    def get(self, id_proyperfil):
        print("Gateway: Lista Entrevistas de un Puesto")
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        print(response)
        if res_code==200:
            lstEV=response["Entrevistas"]
            lstCand=[]
            for e in lstEV:
                lstCand.append(e["id_cand"])
            if len(lstCand)!=0:
                headers={}
                body={"lstCandidatos":lstCand}
                path='/candidatos/lista'
                response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                       body=body, headers=headers, tiempoespera=5000)              
                if res_code2==200:
                    lstDetCandidatos=response2["lstDetCandidatos"]
                    for e in lstEV:
                        for c in lstDetCandidatos:
                            if e["id_cand"]==c["id"]:
                                e["candidato"]=c["nombres"] + " "+ c["apellidos"]
                print(response)
                return response, 200
            else:
                print(response)
                return response, 200
        else:
            return response, res_code

class VistaEntrevistasResultado(Resource):
    def post(self, id_entrevista):
        print("Gateway: Guardar Resultados de una entrevista")
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, res_code
    
    def get(self, id_entrevista):
        print("Gateway: Obtener Resultados de una entrevista")
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        print(response)
        if res_code==200:
            EV=response["Entrevista"]
            headers={}
            path='/candidato/'+str(EV["id_cand"])
            response2, res_code2 = send_get_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                   headers=headers, tiempoespera=5000)              
            if res_code2==200:
                EV["candidato"]=response2["nombres"] + " "+ response2["apellidos"]
            print(response)
            return response, 200
        else:
            return response, res_code

class VistaEvaluaciones(Resource):
    def post(self):
        print("Gateway: creando evaluacion")
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, res_code

class VistaEvalsPuesto(Resource):
    def get(self, id_proyperfil):
        print("Gateway: Obtener Evaluaciones de un PerfilProyecto")
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        print(response)
        if res_code==200:
            lstEvals=response["lstEvals"]
            lstCand=[]
            order: int =1
            for e in lstEvals:
                lstCand.append(e["id_cand"])
                e['num']=order
                order=order+1
            if len(lstCand)!=0:
                headers={}
                body={"lstCandidatos":lstCand}
                path='/candidatos/lista'
                response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                       body=body, headers=headers, tiempoespera=5000)              
                if res_code2==200:
                    lstDetCandidatos=response2["lstDetCandidatos"]
                    for e in lstEvals:
                        for c in lstDetCandidatos:
                            if e["id_cand"]==c["id"]:
                                e["candidato"]=c["nombres"] + " "+ c["apellidos"]
                print(response)
                return response, 200
            else:
                print(response)
                return response, 200
        else:
            return response, res_code
                  
class VistaAsignaCandidato(Resource):
    def post(self, id_proyperfil):
        print("Gateway: Asignacion Candidato PerfilProyecto")
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, res_code
    
class VistaPerfilProyectoDet(Resource):
    def get(self, id_proyperfil):
        print("Gateway: Obtener Perfil proyecto detallado")
        print(id_proyperfil)
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        print(response)
        if res_code==200:
            perfil=response["Perfil"]
            print(perfil)
            if perfil['id_cand']==0:
               perfil['candidato']='NO ASIGNADO'
            else:
                headers={}
                path='/candidato/'+str(perfil['id_cand'])
                response2, res_code2 = send_get_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                    headers=headers, tiempoespera=5000)              
                if res_code2==200:
                    cand=response2["nombres"]+' '+response2["apellidos"]
                    perfil['candidato']=cand
                else:
                    perfil['candidato']='NO SE PUDO CONSULTAR'
        return response, res_code
    
class VistaEmpresaPuestosOfrecidosNoAsignados(Resource):
    def post(self, id_empresa):
        print("Gateway: Obtener Puestos Ofrecidos por una Empresa No Asignados")

        headers=request.headers
        body=request.json
        print("Mensajes")
        print(body)
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 body=body, headers=headers, tiempoespera=5000)
        print("Despues")
        if res_code==200:
            lstPuestos=response["Puestos"]
            for p in lstPuestos:
                p["candidato"]="NO ASIGNADO"
            print(response)
            return response, 200
        else:
            return response, res_code

class VistaEmpresaPuestosOfrecidosAsignados(Resource):
    def post(self, id_empresa):
        print("Gateway: Obtener Puestos Ofrecidos por una Empresa Asignados")
        patron=request.json.get("candidato")
        if patron!="":
            if patron=="NO ASIGNADO":
                lstNumCand=[0]
            else:
                headers=request.headers
                body={"patron": patron}
                responseX, res_codeX = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}/candidatos/like",
                                    body=body, headers=headers, tiempoespera=5000)
                if res_codeX==200:
                    lstNumCand=responseX["lstNumCandidatos"]
                else:
                    lstNumCand=[-1]
        else:
            lstNumCand=[-1]

        headers=request.headers
        body=request.json
        body["lstNumCand"]=lstNumCand
        print("Mensajes")
        print(body)
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 body=body, headers=headers, tiempoespera=5000)
        print("Despues")
        if res_code==200:
            lstPuestos=response["Puestos"]
            lstCand=[]
            for p in lstPuestos:
                if p["id_cand"]!=0:
                   lstCand.append(p["id_cand"])
                else:
                    p["candidato"]="NO ASIGNADO"
            if len(lstCand)!=0:
                headers={}
                body={"lstCandidatos":lstCand}
                path='/candidatos/lista'
                response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                       body=body, headers=headers, tiempoespera=5000)              
                if res_code2==200:
                    lstDetCandidatos=response2["lstDetCandidatos"]
                    for p in lstPuestos:
                        for c in lstDetCandidatos:
                            if p["id_cand"]==c["id"]:
                                p["candidato"]=c["nombres"] + " "+ c["apellidos"]
                            p["imagen"]=c["imagen"]
                    print(response)
                    return response, 200
            else:
                print(response)
                return response, 200
        else:
            return response, res_code

class VistaEmpresaPuestosOfrecidos(Resource):
    def post(self, id_empresa):
        print("Gateway: Obtener Puestos Ofrecidos por una Empresa")
        patron=request.json.get("candidato")
        if patron!="":
            if patron=="NO ASIGNADO":
                lstNumCand=[0]
            else:
                headers=request.headers
                body={"patron": patron}
                responseX, res_codeX = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}/candidatos/like",
                                    body=body, headers=headers, tiempoespera=5000)
                if res_codeX==200:
                    lstNumCand=responseX["lstNumCandidatos"]
                else:
                    lstNumCand=[-1]
        else:
            lstNumCand=[-1]

        headers=request.headers
        body=request.json
        body["lstNumCand"]=lstNumCand
        print("Mensajes")
        print(body)
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 body=body, headers=headers, tiempoespera=5000)
        print("Despues")
        if res_code==200:
            lstPuestos=response["Puestos"]
            lstCand=[]
            for p in lstPuestos:
                if p["id_cand"]!=0:
                   lstCand.append(p["id_cand"])
                else:
                    p["candidato"]="NO ASIGNADO"
            if len(lstCand)!=0:
                headers={}
                body={"lstCandidatos":lstCand}
                path='/candidatos/lista'
                response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                       body=body, headers=headers, tiempoespera=5000)              
                if res_code2==200:
                    lstDetCandidatos=response2["lstDetCandidatos"]
                    for p in lstPuestos:
                        for c in lstDetCandidatos:
                            if p["id_cand"]==c["id"]:
                                p["candidato"]=c["nombres"] + " "+ c["apellidos"]
                    print(response)
                    return response, 200
            else:
                print(response)
                return response, 200
        else:
            return response, res_code

class VistaPuestosOfrecidosNoAsignados(Resource):
    def post(self):
        print("Gateway: Obtener Puestos Ofrecidos No Asignados")

        headers=request.headers
        body=request.json
        print("Mensajes")
        print(body)
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 body=body, headers=headers, tiempoespera=5000)
        print("Despues")
        if res_code==200:
            lstPuestos=response["Puestos"]
            for p in lstPuestos:
                p["candidato"]="NO ASIGNADO"
            print(response)
            return response, 200
        else:
            return response, res_code

class VistaPuestosOfrecidosAsignados(Resource):
    def post(self):
        print("Gateway: Obtener Puestos Ofrecidos Asignados")
        patron=request.json.get("candidato")
        if patron!="":
            if patron=="NO ASIGNADO":
                lstNumCand=[0]
            else:
                headers=request.headers
                body={"patron": patron}
                responseX, res_codeX = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}/candidatos/like",
                                    body=body, headers=headers, tiempoespera=5000)
                if res_codeX==200:
                    lstNumCand=responseX["lstNumCandidatos"]
                else:
                    lstNumCand=[-1]
        else:
            lstNumCand=[-1]

        headers=request.headers
        body=request.json
        body["lstNumCand"]=lstNumCand
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 body=body, headers=headers, tiempoespera=5000)
        if res_code==200:
            lstPuestos=response["Puestos"]
            lstCand=[]
            for p in lstPuestos:
                if p["id_cand"]!=0:
                   lstCand.append(p["id_cand"])
                else:
                    p["candidato"]="NO ASIGNADO"
            if len(lstCand)!=0:
                headers={}
                body={"lstCandidatos":lstCand}
                path='/candidatos/lista'
                response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                       body=body, headers=headers, tiempoespera=5000)              
                if res_code2==200:
                    lstDetCandidatos=response2["lstDetCandidatos"]
                    for p in lstPuestos:
                        for c in lstDetCandidatos:
                            if p["id_cand"]==c["id"]:
                                p["candidato"]=c["nombres"] + " "+ c["apellidos"]
                    print(response)
                    return response, 200
            else:
                print(response)
                return response, 200
        else:
            return response, res_code


class VistaPuestosOfrecidos(Resource):
    def post(self):
        print("Gateway: Obtener Puestos Ofrecidos")
        patron=request.json.get("candidato")
        if patron!="":
            if patron=="NO ASIGNADO":
                lstNumCand=[0]
            else:
                headers=request.headers
                body={"patron": patron}
                responseX, res_codeX = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}/candidatos/like",
                                    body=body, headers=headers, tiempoespera=5000)
                if res_codeX==200:
                    lstNumCand=responseX["lstNumCandidatos"]
                else:
                    lstNumCand=[-1]
        else:
            lstNumCand=[-1]

        headers=request.headers
        body=request.json
        body["lstNumCand"]=lstNumCand
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 body=body, headers=headers, tiempoespera=5000)
        if res_code==200:
            lstPuestos=response["Puestos"]
            lstCand=[]
            for p in lstPuestos:
                if p["id_cand"]!=0:
                   lstCand.append(p["id_cand"])
                else:
                    p["candidato"]="NO ASIGNADO"
            if len(lstCand)!=0:
                headers={}
                body={"lstCandidatos":lstCand}
                path='/candidatos/lista'
                response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                       body=body, headers=headers, tiempoespera=5000)              
                if res_code2==200:
                    lstDetCandidatos=response2["lstDetCandidatos"]
                    for p in lstPuestos:
                        for c in lstDetCandidatos:
                            if p["id_cand"]==c["id"]:
                                p["candidato"]=c["nombres"] + " "+ c["apellidos"]
                    print(response)
                    return response, 200
            else:
                print(response)
                return response, 200
        else:
            return response, res_code
        
class VistaProyectoDetalle(Resource):
    def get(self, id_proy):
        print("Gateway Proyecto Detalle")
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        if res_code==200:
            lstPerfiles=response["perfiles"]
            lstPerf=[]
            lstCand=[]
            for p in lstPerfiles:
                lstPerf.append(p["id_perfil"])
                if p["id_cand"]!=0:
                   lstCand.append(p["id_cand"])
                else:
                    p["candidato"]="NO ASIGNADO"
            
            headers={}
            body={"lstPerfiles":lstPerf}
            path='/perfiles/habilidades'
            response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_PERFILES']}{path}",
                                   body=body, headers=headers, tiempoespera=5000)
            if res_code2==200:
                lstDetPerfil=response2["lstDetPerfiles"]
                for p in lstPerfiles:
                    for pd in lstDetPerfil:
                        if p["id_perfil"]==pd["id"]:
                            p["lstHT"]=pd["lstHT"]
                            p["lstHB"]=pd["lstHB"]
                            p["lstHP"]=pd["lstHP"]
                            break

                headers={}
                body={"lstCandidatos":lstCand}
                path='/candidatos/lista'
                response3, res_code3 = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                   body=body, headers=headers, tiempoespera=5000)
                
                if res_code3==200:
                    lstDetCandidatos=response3["lstDetCandidatos"]
                    for p in lstPerfiles:
                        for c in lstDetCandidatos:
                            if p["id_cand"]==c["id"]:
                                p["candidato"]=c["nombres"] + " "+ c["apellidos"]
                    print(response)
                    return response, 200
                else:
                    print(response)
                    return response, 200
            else:
                print(response)
                return response, res_code
        else:
            print(response)
            return response, res_code
    
class VistaProyectos(Resource):
    def post(self, id_emp):
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, res_code

    def get(self, id_emp):
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, res_code


class VistaEmpresas(Resource):
    def post(self):
        print("Gateway Crear Empresa")
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        print(response)
        return response, res_code
    
    def get(self):
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, res_code

class VistaEmpresa(Resource):
    def get(self, id_empresa):        
        print("Gateway Ver Empresa: ", id_empresa)
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        print(response)
        return response, res_code

#################################################################################
#################################   FIN EMPRESAS   ##############################
#################################################################################


#################################################################################
#################################      PERFILES    ##############################
#################################################################################
class VistaListaHabils(Resource):
    def get(self):
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_PERFILES']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, res_code
    
class VistaPerfil(Resource):
    def get(self, id_perfil):
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_PERFILES']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, res_code

class VistaAsignaPerfilCandidato(Resource):
    def post(self, id_cand):
        print("Gateway: Asignar perfil a candidato")
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_PERFILES']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        print(response)
        return response, res_code

#################################################################################
#################################   FIN PERFILES   ##############################
#################################################################################

#################################################################################
#################################     EMPAREJAR    ##############################
#################################################################################

class VistaCumplenPerfilporLista(Resource):
    def post(self):
        print("Gateway Candidatos Cumplen Perfil por Lista")
        headers=request.headers
        body=request.json
        path='/validador/perfiles'
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_VALIDADOR']}{path}",
                                   body=body, headers=headers, tiempoespera=5000)
        print(response)
        return response, res_code

class VistaCumplenPerfil(Resource):
    def get(self, id_perfil):
        print("Gateway Candidatos Cumplen Perfil")
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_PERFILES']}/perfil/{id_perfil}",
                                 headers=headers, tiempoespera=5000)
        if res_code==200:
            print("Respuesta Perfiles Ok")
            lstHabils=response["Habilidades"]
            lstHab=[]
            for h in lstHabils:
                lstHab.append(h["id_habil"])
            print(lstHab)

            headers={}
            body={"lstHabils": lstHab}
            path='/validador/perfiles'
            response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_VALIDADOR']}{path}",
                                   body=body, headers=headers, tiempoespera=5000)
            print("=====================")
            print(response2)
            print("=====================")
            response3={"Mensaje":"Packed", "Respuesta": response2, "Otro":"Valor"}
            #response3={"Mensaje":"Packed", "Respuesta": {}, "Otro":"Valor"}
            return response3, res_code2
        else:
            print("Respuesta Perfiles Bad")
            return response, res_code

#################################################################################
#################################   FIN EMPAREJAR  ##############################
#################################################################################

#################################################################################
#################################     PRUEBAS     ###############################
#################################################################################

class VistaPruebas(Resource):
    def post(self):
        print("Gateway: creando nueva prueba")
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_PRUEBASTEC']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        print(response)
        return response, res_code

class VistaPruebasCalificacion(Resource):
    def post(self, id_examen):
        print("Gateway: Actualiza Calificacion de un Examen")
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_PRUEBASTEC']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        print(response)
        return response, res_code

class VistaPruebasCandidato(Resource):
    def get(self, id_cand):
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_PRUEBASTEC']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        if res_code==200:
            lstExamenes=response
            headers=request.headers
            path='/perfiles/lstHabilidades'
            response2, res_code2 = send_get_request(url=f"{current_app.config['HOST_PORT_PERFILES']}{path}",
                                   headers=headers, tiempoespera=5000)
            if res_code2==200:
                lstHabils=response2
                for e in lstExamenes:
                    for h in lstHabils:
                        if e['id_habil']==h['id']:
                            e['nom_habil']=h['nombre']
                            break;
        return response, res_code

class VistaPruebasParam(Resource):
    def post(self):
        print("Gateway: Consultar Pruebas Parametrizadas")
        num_pag=request.json.get("num_pag")
        maximo=request.json.get("max")
        patronCandidato=request.json.get("candidato")
        if patronCandidato!="":
            headers=request.headers
            body={"patron": patronCandidato}
            responseX, res_codeX = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}/candidatos/like",
                                body=body, headers=headers, tiempoespera=5000)
            if res_codeX==200:
                lstNumCand=responseX["lstNumCandidatos"]
            else:
                lstNumCand=[-1]
        else:
            lstNumCand=[-1]

        patronHabilidad=request.json.get("habilidad")
        if patronHabilidad!="":
            headers=request.headers
            body={"patron": patronHabilidad}
            responseX, res_codeX = send_post_request(url=f"{current_app.config['HOST_PORT_PERFILES']}/habilidades/like",
                                body=body, headers=headers, tiempoespera=5000)
            if res_codeX==200:
                lstNumHabil=responseX["lstNumHabilidades"]
            else:
                lstNumHabil=[-1]
        else:
            lstNumHabil=[-1]

        headers=request.headers
        body=request.json
        body["lstNumCand"]=lstNumCand
        body["lstNumHabil"]=lstNumHabil
        #print("Mensajes")
        #print(body)
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_PRUEBASTEC']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        if res_code==200:
            lstTests=response["Examenes"]
            lstCand=[]
            for t in lstTests:
                lstCand.append(t["id_cand"])
            if len(lstCand)!=0:
                headers={}
                body={"lstCandidatos":lstCand}
                path='/candidatos/lista'
                response2, res_code2 = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{path}",
                                       body=body, headers=headers, tiempoespera=5000)              
                if res_code2==200:
                    lstDetCandidatos=response2["lstDetCandidatos"]
                    for t in lstTests:
                        for c in lstDetCandidatos:
                            if t["id_cand"]==c["id"]:
                                t["candidato"]=c["nombres"] + " "+ c["apellidos"]
                                break;

            headers=request.headers
            path='/perfiles/lstHabilidades'
            response3, res_code3 = send_get_request(url=f"{current_app.config['HOST_PORT_PERFILES']}{path}",
                                   headers=headers, tiempoespera=5000)

            if res_code3==200:
                lstHabils=response3
                i=0
                for e in lstTests:
                    i=i+1
                    e['Num']=(num_pag-1)*maximo + i
                    for h in lstHabils:
                        if e['id_habil']==h['id']:
                            e['nom_habil']=h['nombre']
                            break;
            return response, res_code
        else:
            return response, res_code

#################################################################################
#################################    CANDIDATOS    ##############################
#################################################################################

class VistaCandidatosParcial(Resource):
    def post(self):
        print("Gateway: Obteniendo candidatos")
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        print(response)
        return response, res_code

class VistaCandidatos(Resource):
    def post(self):
        print("Gateway: Creando Candidato")
        headers=request.headers
        body=request.json
        response, res_code = send_post_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        print(response)
        return response, res_code



class VistaCandidato(Resource):
    def get(self, id_cand):
        print("Gateway: Consultar Candidato")
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        print("Vista en Estudio")
        print(response)
        return response, res_code

class VistaCandidatoUsuario(Resource):
    def get(self, id_usuario):
        print("Gateway: Consultar Candidato por id_usuario")
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        print("Vista en Estudio")
        print(response)
        return response, res_code


class VistaCandidatoDetalleUsuario(Resource):
    def get(self, id_usuario):
        print("Gateway: Consultar Detalle Candidato de un Usuario")
        headers=request.headers
        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_CANDIDATO']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        print(response)
        print(res_code)
        if res_code==200:
            print("Antes del JSON")
            candidatoJSON=response
            print(candidatoJSON)
            print("Respuesta Candidatos Ok")
            num_perfil=response["num_perfil"]
            headers=request.headers
            path='/perfil/'+str(num_perfil) 
            response2, res_code2 = send_get_request(url=f"{current_app.config['HOST_PORT_PERFILES']}{path}",
                                   headers=headers, tiempoespera=5000)
            if res_code2==200:
                lstHabils=response2["Habilidades"]
                lstHab=[]
                for h in lstHabils:
                    habilJSON={}
                    habilJSON["id_ph"]=h["id_hp"]
                    habilJSON["id_perfil"]=h["id_perfil"]
                    habilJSON["valoracion"]=h["valoracion"]
                    habilJSON["calificacion"]=h["calificacion"]
                    habilJSON["id_habil"]=h["id_habil"]
                    habilJSON["nombre"]=h["nombre"]
                    habilJSON["tipo"]=h["tipo_habil"]
                    lstHab.append(habilJSON)
                print(lstHab)
                candidatoJSON["lstHabils"]=lstHab
                return candidatoJSON, 200
            else:
                return response, res_code
        return response, res_code

#class VistaListaHabils(Resource):
#    def get(self):
#        headers=request.headers
#        response, res_code = send_get_request(url=f"{current_app.config['HOST_PORT_PERFILES']}{request.path}",
#                                 headers=headers, tiempoespera=5000)
#        return response, res_code

#################################################################################
#################################   FIN CANDIDATOS###############################
#################################################################################


class VistaPing(Resource):
    def get(self):
        print("pong")
        return {"Mensaje":"Pong"}, 200


def send_post_request(url, headers, body, tiempoespera):
    try:
        response = requests.post(url, json=body, headers=headers, timeout=tiempoespera)
        return response.json(), response.status_code
    except Exception as inst:
        print(type(inst))
        #print(inst)
        return {}, 500

def send_get_request(url, headers, tiempoespera):
    print(url)
    try:
        response = requests.get(url=url, headers=headers, timeout=tiempoespera)
        return response.json(), response.status_code
    except Exception as inst:
        print(type(inst))
        #print(inst)
        return {}, 500

def send_put_request(url, headers, body, tiempoespera):
    print(url)
    try:
        response = requests.put(url=url, json=body, headers=headers, timeout=tiempoespera)
        return response.json(), response.status_code
    except Exception as inst:
        print(type(inst))
        #print(inst)
        return {}, 500
    
def send_delete_request(url, headers, tiempoespera):
    print(url)
    try:
        response = requests.delete(url=url, headers=headers, timeout=tiempoespera)
        return response.json(), response.status_code
    except Exception as inst:
        print(type(inst))
        #print(inst)
        return {}, 500

api = Api(application)


api.add_resource(VistaPruebas, '/pruebas')
api.add_resource(VistaPruebasCandidato, '/pruebasCandidato/<int:id_cand>')
api.add_resource(VistaPruebasParam, '/pruebasParam')
api.add_resource(VistaPruebasCalificacion, '/pruebasCalificacion/<int:id_examen>')

api.add_resource(VistaSignIn, '/auth/signup')
api.add_resource(VistaLogIn, '/auth/login')
api.add_resource(VistaUsuario, '/usuario/<int:id_usuario>')
api.add_resource(VistaAuthorization, '/auth/me')
api.add_resource(VistaAuthPing, '/auth/ping')

api.add_resource(VistaEntrevistasCandidatos, '/entrevistasCandidato/<int:id_cand>')
api.add_resource(VistaEntrevistasEmpresas, '/entrevistasEmpresa/<int:id_empresa>')
api.add_resource(VistaLasEntrevistas, '/entrevistasPortal')
api.add_resource(VistaEntrevistas, '/empresas/proyectos/perfiles/entrevistas')
api.add_resource(VistaEntrevistasPuesto, '/empresas/proyectos/perfiles/entrevistas/<int:id_proyperfil>')
api.add_resource(VistaEntrevistasResultado, '/entrevistas/<int:id_entrevista>')

api.add_resource(VistaEvaluaciones, '/empresas/proyectos/perfiles/evaluaciones')
api.add_resource(VistaEvalsPuesto, '/empresas/proyectos/perfiles/evaluaciones/<int:id_proyperfil>')
api.add_resource(VistaAsignaCandidato, '/empresas/proyectos/perfiles/asignacion/<int:id_proyperfil>')
api.add_resource(VistaPerfilProyectoDet, '/empresas/proyectos/perfiles/<int:id_proyperfil>')
api.add_resource(VistaEmpresaPuestosOfrecidosNoAsignados, '/empresas/<int:id_empresa>/puestosNoAsig')
api.add_resource(VistaEmpresaPuestosOfrecidosAsignados, '/empresas/<int:id_empresa>/puestosAsig')
api.add_resource(VistaEmpresaPuestosOfrecidos, '/empresas/<int:id_empresa>/puestos')
api.add_resource(VistaPuestosOfrecidosNoAsignados, '/empresas/puestosNoAsig')
api.add_resource(VistaPuestosOfrecidosAsignados, '/empresas/puestosAsig')
api.add_resource(VistaPuestosOfrecidos, '/empresas/puestos')
api.add_resource(VistaEmpresaDetalleUsuario, '/empresaUsuarioDetalle/<int:id_usuario>')
api.add_resource(VistaProyectoDetalle, '/empresas/proyectos/<int:id_proy>/detallePerfiles')
api.add_resource(VistaPerfilesStr, '/empresas/proyectos/<int:id_proy>/perfilesStr')
api.add_resource(VistaPerfiles, '/empresas/proyectos/<int:id_proy>/perfiles')
api.add_resource(VistaProyecto, '/empresas/proyecto/<int:id_proy>')
api.add_resource(VistaProyectos, '/empresas/<int:id_emp>/proyectos')
api.add_resource(VistaEmpresaUsuario, '/miempresa/<int:id_usuario>')
api.add_resource(VistaEmpresas, '/empresas')
api.add_resource(VistaEmpresa, '/empresa/<int:id_empresa>')

api.add_resource(VistaPing, '/gateway/ping')
api.add_resource(VistaCumplenPerfil, '/cumplenPerfil/<int:id_perfil>')
api.add_resource(VistaCumplenPerfilporLista, '/cumplenPerfilporLista')
api.add_resource(VistaListaHabils, '/perfiles/lstHabilidades')
api.add_resource(VistaPerfil, '/perfil/<int:id_perfil>')
api.add_resource(VistaAsignaPerfilCandidato, '/perfil/asignaCandidato/<int:id_cand>')

api.add_resource(VistaCandidatosParcial, '/candidatos/parcial')
api.add_resource(VistaCandidatos, '/candidatos')
api.add_resource(VistaCandidato, '/candidato/<int:id_cand>')
api.add_resource(VistaCandidatoUsuario, '/micandidato/<int:id_usuario>')
api.add_resource(VistaCandidatoDetalleUsuario, '/candidatoUsuarioDetalle/<int:id_usuario>')

jwt = JWTManager(application)