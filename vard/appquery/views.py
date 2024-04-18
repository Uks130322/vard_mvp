from rest_framework import viewsets
from vardapp.models import ClientDB, Chart, ClientData
from rest_framework.response import Response
from .serializers import ClientDBSerializer, ClientDataSerializer
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy_utils import create_database, drop_database, database_exists
from sqlalchemy import exc


class ClientDBViewSet(viewsets.ModelViewSet):
    queryset = ClientDB.objects.all()
    serializer_class = ClientDBSerializer

    def get_host(self, url, host, port):
        if host == 'localhost' or host == '127.0.0.1':
            result = host
        elif port == '' or port is None or not port:
            result = f'{url}:3306'
        else:
            result = f'{url}:{port}'
        return result

    def get_str_connect_sqlalchemy(self, user_name, password, url, host, port, data_base_name):
        password_new = password.replace('@', '%40')
        password_new = re.escape(password_new)
        host_new = self.get_host(url, host, port)
        str_connect = f"mysql://{user_name}:{password_new}@{host_new}/{data_base_name}"
        return str_connect

    def get_engine(self, user_name, password, url, host, port, data_base_name):
        str_connect_new = self.get_str_connect(user_name, password, url, host, port, data_base_name)
        engine = create_engine(f"{str_connect_new}", echo=False)
        return engine

    def create_data_base(self, user_name, password, url, host, port, data_base_name):
        str_connect_new = self.get_str_connect(user_name, password, url, host, port, data_base_name)
        if not database_exists(f"{str_connect_new}"):
            create_database(f"{str_connect_new}")
            return f'{data_base_name} создана'
        else:
            return f'{data_base_name} уже существует'

    def drop_data_base(self, user_name, password, url, host, port, data_base_name):
        str_connect_new = self.get_str_connect(user_name, password, url, host, port, data_base_name)
        if database_exists(f"{str_connect_new}"):
            drop_database(f"{str_connect_new}")
            return f'{data_base_name} удалена'
        else:
            return f'{data_base_name} не найдена'

    def get_query(self, user_name, password, url, host, port, data_base_name, str_query, user_id):
        engine = self.get_engine(user_name, password, url, host, port, data_base_name)
        Session = sessionmaker(autoflush=False, bind=engine)
        with Session(autoflush=False, bind=engine) as db:
            rows = db.execute(text(str_query)).fetchall()
            user = [{'user_id': user_id}]
            result = user + [r._asdict() for r in rows]
        return result

    def perform_create(self, serializer):
        # serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.validated_data
        str_datas_for_connection = self.get_str_connect_sqlalchemy(
            datas['user_name'],
            datas['password'],
            datas['url'],
            datas['host'],
            datas['port'],
            datas['data_base_name']
        )
        return serializer.save(
            user=self.request.user,
            str_datas_for_connection=str_datas_for_connection
        )

    def get_queryset(self):
        queryset = ClientDB.objects.filter(user_id=self.request.user)
        return queryset


class ClientDataViewSet(viewsets.ModelViewSet):
    queryset = ClientData.objects.all()
    serializer_class = ClientDataSerializer

    def list(self, request, *args, **kwargs):
        L = []
        old_response_data = super(ClientDataViewSet, self).list(request, *args, **kwargs)
        client_data = ClientData.objects.all()
        for i, j in zip(client_data, old_response_data.data):
            obj = Chart.objects.get(id=i.chart.id)
            str_query = obj.str_query
            str_datas_for_connection = ClientDB.objects.get(id=obj.clientdb_id.id).str_datas_for_connection
            try:
                engine = create_engine(f"{str_datas_for_connection}", echo=False)
                Session = sessionmaker(autoflush=False, bind=engine)
                with Session(autoflush=False, bind=engine) as db:
                    rows = db.execute(text(str_query)).fetchall()
                    result = [r._asdict() for r in rows]
                    if not ClientData.objects.filter(id=i.chart.id):
                        ClientData.objects.filter(id=i.chart.id).update(data=result)
            except exc.SQLAlchemyError as e:
                #error = str(e.__dict__['orig'])
                print('error', e)
            j['data'] = result
            L.append(j)
        new_response_data = L
        return Response(new_response_data)
