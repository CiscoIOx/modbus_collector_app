Mqtt App for Cisco Developer workshop.

# Follow the steps defined in freeboard/README.md file and create once freeboard.io instance for your table.

# How to create and build the app:
- Git clone the mqtt_app repo.
    * RUN: git clone http://gitlab.cisco.com/iox/mqtt_app
    * cd mqtt_app
- Now if you want test the app locally please follow the steps defined below.
- To build the app in to docker container.
    * RUN: sudo docker build -t mqtt . # This basically read Dockerfile and create a docker image with name 'mqtt'
    * To view the image built, RUN: sudo docker images , you can see you image name populated
    * To test the app inside a docker container, please find the below steps.
- To package the docker container in to IOx undestadable,
    * RUN: sudo ioxclient docekr package <image_name> . # This will create package.tar file which can be installled on device

# Deploy and start the app in device.
- First create ioxclient profile for a given device.
    * RUN: ioxcient pr c
      For reference:
        root@ubuntu:/home/madawood/Documents/mqttApp/mqtt_app# ioxclient pr c
        Active Profile :  default
        Enter a name for this profile : <device-name?
        Your IOx platform's IP address[127.0.0.1] : <device_ip_address>
        Your IOx platform's port number[8443] : <CAF listening port>
        Authorized user name[root] : <device credentials>
        Password for root : <device credentials>
        Local repository path on IOx platform[/software/downloads]:
        URL Scheme (http/https) [https]:
        API Prefix[/iox/api/v2/hosting/]:
        Your IOx platform's SSH Port[2222]: <Port on which ssh server is running on device>
        Activating Profile  device-name
        Saving current configuration
    * RUN: ioxclient app li
        Should give response with list of apps installed or no apps installed
    * RUN: ioxclient app install <app_name> package.tar # WIll deploy the app on device
    * RUN: ioxclient app act <app_name> # Will activate the app
    * RUN: ioxclient app start <app_name> # Will satart the app
- Check you freeboard.io is populating the data in UI.

# To test the app locally, please follow the following steps defined.
-  Install python on your machine, preferred version = 2.7
-  Then install and run mosquitto broker on your local linux based machine.
    * Steps to install mosquitto on ubuntu based server:
        * RUN: sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
        * RUN: sudo apt-get update
        * RUN: sudo apt-get install mosquitto
        * For further details refer: http://wingsquare.com/blog/setting-up-mqtt-mosquitto-broker-in-ubuntu-linux/
- Once you successfully installed mosquitto, below are the steps to run it.
        RUN: sudo mosquitto -v -p 1883 #mosquitto will start and listen on 18833 port(this can be changed as per the requirements).
- Now we need to install the python bindings for mosquitto broker and also other dependencies.
        * RUN: sudo apt-get install python-pip
        * RUN: pip install -r requirement.txt
- Setup the freeboard.io instance for UI to get populate from our app data.
    * Steps to populate freeboard.io are mentioned in freeboard/README.md file
- Now we have environment created to run our app locally, so let's run it.
        Steps to run the app:
            First we need to start the publisher-simulator, RUN: python mqtt_pub.py --host localhost --port port --topics wx,geo,buttons
            Then start the app, RUN: python mqtt_app.py
                (your package_config.ini subscribe topics should match with the topics given to above publisher-simulator)
            After successful execution of the above commands, check your UI in freeboard.io.

