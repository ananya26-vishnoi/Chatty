# Setup

## Virtual Environment


To ensure a clean and organized development environment, it is highly recommended to use a virtual environment when working with any project. You can create a virtual environment for your project by running the following command in your terminal:

```bash
python -m venv <name of virtual environment>
```

Once your virtual environment is created, you can activate it using the appropriate command for your operating system.

Windows:
```bash
.\<name of virtual environment>\Scripts\activate
```

Linux/Unix:
```bash
source <name of virtual environment>/bin/activate
```

By activating your virtual environment, you can ensure that any dependencies and packages you install will be isolated from your global environment, making it easier to manage and maintain your project.

## Installing Dependencies


      
To install all the necessary dependencies for your project, simply run the following command in your terminal:

```bash
pip install -r requirements.txt
```
This command will read the requirements.txt file and automatically install all the listed dependencies for you. Make sure your virtual environment is activated before running this command to ensure that the packages are installed in the correct environment. Once the installation is complete, you'll be ready to start working on your project!

## .env

<b> Important Note: </b>
Please make your own .env from demo.env file and add your own credentials.


# About the project:

1. This project uses Django Channels to implement Websockets.
2. Each socket has a unique ID which is used to identify and send messages to different users
3. Here is the video demonstration of the project: 
4. Frontend socket is handled by chat.js file in static/js folder
5. Backend socket is handled by consumers.py file in chat folder and routing is handled by routing.py file in chat folder
6. REST API is used to create chatHistory and chatList instead of sockets for better performance
7. This project uses Django Rest Framework to implement REST API
8. you will have to change BASE_URL in chat.js file to your own local url on which you are running the project