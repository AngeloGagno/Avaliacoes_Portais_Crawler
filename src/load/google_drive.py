import os
import sys 
from io import BytesIO
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import tempfile
from dotenv import load_dotenv

class Loader:
    def __init__(self,portal_name:str = 'airbnb'):
        _ = load_dotenv(override=True)
        # Procurar variaveis no .env e retornar erro caso alguma não seja encontrada
        self._envs = {"type": os.environ.get("TYPE"),
            "project_id": os.environ.get("PROJECT_ID"),
            "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
            "private_key": os.environ.get("PRIVATE_KEY"),
            "client_email": os.environ.get("CLIENT_EMAIL"),
            "client_id": os.environ.get("CLIENT_ID"),
            "auth_uri": os.environ.get("AUTH_URI"),
            "token_uri": os.environ.get("TOKEN_URI"),
            "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.environ.get("CLIENT_X509_CERT_URL"),
            "universe_domain": os.environ.get("UNIVERSE_DOMAIN"),
            "AIRBNB_FOLDER":os.environ.get("AIRBNB_FOLDER")
        }
        for var in self._envs:
            if self._envs[var] is None:
                print(f"A variável de ambiente {var} não está definida.")
                sys.exit(1)
        # Definir o escopo da API
        self.scopes = [
    'https://www.googleapis.com/auth/drive'
]
        # Conta de serviço que enviará os dados a pasta 
        self.service_account = self.service_account()
        self.portal_name = portal_name
        self._buffer = None

    def service_account(self) -> dict:
        return {"type": os.environ.get("TYPE"),
            "project_id": os.environ.get("PROJECT_ID"),
            "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
            "private_key": os.environ.get("PRIVATE_KEY"),
            "client_email": os.environ.get("CLIENT_EMAIL"),
            "client_id": os.environ.get("CLIENT_ID"),
            "auth_uri": os.environ.get("AUTH_URI"),
            "token_uri": os.environ.get("TOKEN_URI"),
            "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.environ.get("CLIENT_X509_CERT_URL"),
            "universe_domain": os.environ.get("UNIVERSE_DOMAIN")}
    
    def folder(self) -> str:
        if self.portal_name == 'airbnb':
            return str(os.environ.get('AIRBNB_FOLDER'))
        if self.portal_name == 'booking':
            return str(os.environ.get('BOOKING_FOLDER'))
        
        else:
            raise ValueError('Portal inserido está incorreto')

    def convert_to_delta(self, json_file):
        try:
            df = pd.DataFrame(json_file)
            self._buffer = BytesIO()
            try:
                df.to_parquet(self._buffer, engine='pyarrow',index=False)  # ou engine='fastparquet'
                self._buffer.seek(0)  # importante reposicionar o ponteiro!
                return self._buffer
            except Exception as e:
                print(f"Erro ao transformar o DataFrame em Parquet: {e}")
                self._buffer = None
                return None
        except Exception as e:
            print(f"Erro ao converter JSON para DataFrame: {e}")
            self._buffer = None
            return None

    def generate_filename(self):
        date = datetime.now().date().isoformat()
        return f'{self.portal_name}_{date}.parquet'
    
    def create_connection(self):
        #try:
            googleauth = GoogleAuth()
            googleauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(self.service_account, self.scopes)
            drive = GoogleDrive(googleauth)
            return drive
        
        #except:
        #    raise ConnectionError('Conexão Mal Sucedida. Revisar as credenciais')
    
        
    def create_file(self):
        #try:
            instance = self.create_connection()
            file = instance.CreateFile({'title':self.generate_filename(),'parents':[{'id':self.folder()}]})
            return file
        #except:
        #    raise FileNotFoundError('Pasta no drive não encontrada')
        

    def upload_parquet(self, parsed_data):
        buffer = self.convert_to_delta(json_file=parsed_data)
        if buffer is None:
            print("Erro: Buffer não criado.")
            return

        file = self.create_file()

        tmp_path = None  # Definimos fora para garantir acesso no finally
            # Criar e fechar arquivo temporário
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False, mode='wb') as tmp:
            tmp.write(buffer.getvalue())
            tmp_path = tmp.name  

        file.SetContentFile(tmp_path)
        file.Upload()

        

        