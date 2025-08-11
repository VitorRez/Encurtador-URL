$script_postgres = <<-SCRIPT
  apt-get update && \
  apt-get install -y postgresql postgresql-contrib && \

  # Configura o postgresql.conf para aceitar conexões externas
  sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf && \

  # Adiciona permissão no pg_hba.conf
  echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/*/main/pg_hba.conf && \

  # Reinicia o PostgreSQL
  systemctl restart postgresql && \

  # Cria usuário e banco apenas se ainda não existirem
  sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='euufsj'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE USER euufsj WITH PASSWORD 'euufsj';"

  sudo -u postgres psql -c "ALTER USER euufsj WITH SUPERUSER;"

  sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='urldb'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE DATABASE urldb OWNER euufsj;"
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "euUFSJDesenv"
    vb.memory = 2048
    vb.cpus = 2
  end

  # Redireciona porta 5432 da VM para o host
  config.vm.network "forwarded_port", guest: 5432, host: 5432
  config.vm.provision "shell", inline: $script_postgres
end
