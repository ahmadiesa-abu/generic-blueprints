#!/bin/bash -e
# first lets disable rh-cloud repo
sudo rm -rf /etc/yum.repos.d/rh-cloud.repo

# add msssql repo
sudo curl -o /etc/yum.repos.d/mssql-server.repo https://packages.microsoft.com/config/rhel/8/mssql-server-2019.repo
sudo curl -o /etc/yum.repos.d/msprod.repo https://packages.microsoft.com/config/rhel/8/prod.repo

# register to rhel subscription
sudo LANG=C subscription-manager register --force --username="${rhel_sub_username}" --password="${rhel_sub_password}"
sudo LANG=C subscription-manager attach --auto

# install mssql
ctx logger info "Installing mssql-server package"
sudo yum install -y mssql-server

MSSQL_SA_PASSWORD="${mssql_password}"
MSSQL_PID='evaluation'
SQL_ENABLE_AGENT='y'
SQL_INSTALL_USER="${mssql_user}"
SQL_INSTALL_USER_PASSWORD="${mssql_password}"

echo Running mssql-conf setup...
sudo MSSQL_SA_PASSWORD=$MSSQL_SA_PASSWORD \
     MSSQL_PID=$MSSQL_PID \
     /opt/mssql/bin/mssql-conf -n setup accept-eula

ctx logger info "Installing mssql-tools, unixODBC-devel packages"
echo Installing mssql-tools and unixODBC developer...
sudo ACCEPT_EULA=Y yum install -y mssql-tools unixODBC-devel

# Add SQL Server tools to the path by default:
ctx logger info "Adding SQL Server tools to your path..."
echo PATH="$PATH:/opt/mssql-tools/bin" >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc

# Configure firewall to allow TCP port 1433:
ctx logger info "Configuring firewall to allow traffic on port 1433..."
sudo firewall-cmd --zone=public --add-port=1433/tcp --permanent
sudo firewall-cmd --reload

# Restart SQL Server after making configuration changes:
ctx logger info "Restarting SQL Server..."
sudo systemctl restart mssql-server

# Connect to server and get the version:
counter=1
errstatus=1
while [ $counter -le 5 ] && [ $errstatus = 1 ]
do
  ctx logger info "Waiting for SQL Server to start..."
  sleep 5s
  /opt/mssql-tools/bin/sqlcmd \
    -S localhost \
    -U SA \
    -P $MSSQL_SA_PASSWORD \
    -Q "SELECT @@VERSION" 2>/dev/null
  errstatus=$?
  ((counter++))
done

# Display error if connection failed:
if [ $errstatus = 1 ]
then
  ctx logger error "Cannot connect to SQL Server, installation aborted"
  exit $errstatus
fi

# Optional new user creation:
if [ ! -z $SQL_INSTALL_USER ] && [ ! -z $SQL_INSTALL_USER_PASSWORD ]
then
  ctx logger info "Creating user $SQL_INSTALL_USER"
  /opt/mssql-tools/bin/sqlcmd \
    -S localhost \
    -U SA \
    -P $MSSQL_SA_PASSWORD \
    -Q "CREATE LOGIN [$SQL_INSTALL_USER] WITH PASSWORD=N'$SQL_INSTALL_USER_PASSWORD', DEFAULT_DATABASE=[master], CHECK_EXPIRATION=ON, CHECK_POLICY=ON; ALTER SERVER ROLE [sysadmin] ADD MEMBER [$SQL_INSTALL_USER]"
fi

sudo LANG=C subscription-manager unregister

ctx logger info "Done!"
