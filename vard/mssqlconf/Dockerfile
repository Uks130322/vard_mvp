FROM mcr.microsoft.com/mssql/server

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=QeTuo123

#COPY vard/mssqlconf/setup.sql ./src/sql/setup.sql
#COPY vard/mssqlconf/entrypoint.sh ./src/sql/entrypoint.sh
#CMD ./ ./entrypoint.sh

#COPY vard/mssqlconf /src
##RUN chattr -a /src/entrypoint.sh
##RUN chmod +x /src/entrypoint.sh
##RUN ["chmod", "+x", "./entrypoint.sh"]
#ENTRYPOINT [ "/src/entrypoint.sh" ]
##RUN ["chmod", "+x", "/entrypoint.sh"]
#
##ENTRYPOINT [ "/entrypoint.sh" ]
#CMD /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P QeTuo123 -d master -i /docker-entrypoint-initdb.d/setup.sql
##CMD /opt/mssql-tools18/bin/sqlcmd -S testmssql:1433 -U sa -P QeTuo123 -C -Q "CREATE database [ddd];"
#CMD [ "/opt/mssql/bin/sqlservr" ]
COPY ./vard/mssqlconf /

ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]
CMD [ "/opt/mssql/bin/sqlservr" ]

#docker-compose build
#docker-compose up




