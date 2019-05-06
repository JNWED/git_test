# UI Automation Env Setup At Linux

## Install Ubuntu
Follow the [HOWTO](http://ks.netease.com/blog?id=11585)
```shell
sudo sed -i s@cn.archive.ubuntu.com@mirrors.163.com@g /etc/apt/sources.list
sudo apt-get update
sudo apt-get install -y build-essential python python-pip net-tools
sudo apt-get install -y vim htop openssh-server apache2 git

```

## Install Node for Linux
```shell
#Install
cd ~/Downloads/
wget https://nodejs.org/dist/v8.11.3/node-v8.11.3-linux-x64.tar.xz
tar xf node-v8.11.3-linux-x64.tar.xz

#Setup
vim ~/.bashrc
#Add two lines to the file
export NODE_HOME=~/Downloads/node-v8.11.3-linux-x64
export PATH=${PATH}:${NODE_HOME}/bin
source ~/.bashrc
#check node version
node --version

#Use China local mirror
npm install -g cnpm --registry=https://registry.npm.taobao.org
#And then use cnpm to replace npm
#Such as: cnpm install -g appium
```
## Install Java
```shell
#Install
sudo apt-get update
sudo apt-get install default-jre
sudo apt-get install default-jdk

#setup
vim ~/.bashrc
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=${PATH}:${NODE_HOME}/bin:${JAVA_HOME}/bin
source ~/.bashrc
#check java version
java --version

```
## Install Android-SDK
```shell
sudo apt-get install android-sdk android-sdk-build-tools
vim ~/.bashrc
export ANDROID_HOME=/usr/lib/android-sdk
export PATH=${PATH}:${NODE_HOME}/bin:${JAVA_HOME}/bin:${ANDROID_HOME}/tools:${ANDROID_HOME}/platform-tools
source ~/.bashrc
adb devices

```

## Install Appium
```shell
cnpm install -g appium
cnpm install -g appium-doctor
appium-doctor
```


## Download latest code from gitlab
```shell
#first generate your public key and upload to gitlab server
ssh-keygen -t rsa -C "your email" -b 4096
cat ~/.ssh/id_rsa.pub
#paste the key at https://g.hz.netease.com (User/Setting/SSH-Key)

#git config
git config --global user.name "Your Name"
git config --global user.email "Your Email"

#checkout latst code
mkdir ~/work/
cd ~/work/
git clone ssh://git@g.hz.netease.com:22222/music_qa/client/automation.git

git checkout -b dev
git branch -a
#develop at dev branch 

```

## Setup Automation required package

```shell
#These requird packages can be found at automation/readme.md5 file

#Install PyH
cd ~/Downloads/
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pyh/PyH-0.1.1.tar.gz
tar xf PyH-0.1.1.tar.gz
cd PyH-0.1.1/
sudo python setup.py install

#Install Appium python client
pip install Appium-Python-Client

#Install other packages  
pip install pyyaml
pip install requests
pip install psutil
pip install xmlrunner

```

## Verify the total setup
```shell
#connected Android phone(enabeld usb debug option) 
adb devices
#and then added devicesID to config.yaml file

#Start Appium server
cd ~/work/automation
python run_server_appium.py

#Start http server to listen the test request
cd ~/work/automation
python run_server_http.py

#Submit test request
cd ~/work/automation
python  run_mode_autotest.py 

```

# UI Automation Env Setup At Mac
## Install some required tools for Mac

 ```shell

brew install libimobiledevice --HEAD  #先安装依赖
brew install ideviceinstaller
#first install npm
npm install -g ios-deploy

#check Env
idevice_id -l #connect iphone,and then use this command to find id
ideviceinfo # get more info about connected devices
```

## Install Node
```shell
brew install node
echo "registry=https://registry.npm.taobao.org/" > ~/.npmrc
```
## Install appium for Mac
```shell
npm install -g appium
npm install -g appium-doctor
pip install Appium-Python-Client
```

## Setup Automation required package for Mac

```shell
#These requird packages can be found at automation/readme.md5 file

#Install PyH
cd ~/Downloads/
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pyh/PyH-0.1.1.tar.gz
tar xf PyH-0.1.1.tar.gz
cd PyH-0.1.1/
sudo python setup.py install
#Install other packages
pip install pyyaml
pip install requests
pip install psutil
pip install xmlrunner

```

## setup Env for Mac
[Follow the offical document](https://github.com/appium/appium-xcuitest-driver) to setup

## Verify the total setup
```shell
#connected iphone and update config file
#Start Appium server
cd ~/work/automation
python run_server_appium.py

#Start http server to listen the test request
cd ~/work/automation
python run_server_http.py

#Submit test request
cd ~/work/automation
python  run_mode_autotest.py

```