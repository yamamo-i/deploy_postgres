# -*- mode: ruby -*-

Vagrant.configure(2) do |config|
  config.vm.box = "centos_7"
  config.vm.hostname = "postgres-server"

  config.vm.provider "postgres_server" do |vb|
    # Display the VirtualBox GUI when booting the machine
    vb.gui = false
  
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
  end

  config.vm.network "forwarded_port", guest: 5432, host: 5432
  config.vm.network "forwarded_port", guest: 80, host: 8080

end

