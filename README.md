# Chatbot_IIITDM

## Folder Content
* ML - It contail ML model, trainging code, and testing trained model code
* app - It contain frontent Angular app.
* server_django - It contain backend code in Django python which uses trained model.

## ML

This folder contain -
* *intents.json* - This file contain the intents and patterns(questions) with respect to intents. This file contain data to train out model. 
* *main.py* - This file contain the code for training model. Traing model will be saved as *model.tflearn.data*, *model.tflearn.index* and *model.tflearn.meta* .
Also save the data in *data.pickle* file.
* appTest.py - This file can be used to use the trained model.

This folder also contain jupyter files main.ipynb and app.ipynb.

## server_django
This folder contain the backend File written in Django. Remember everytime you run the model (also after changing in *intents.json* file then run main.py) copy the gerated pickle and model files to this (server_django) folder.
### Important files - 
* *server_django/chat/ml.py* - This file contain the code that will used by chahtbot to give appropriate response.
* *formLink.json* - this file contain most of the important form link available on institute's website.

## app/chatbot-app

This folder contain codes of frontend Angular app.

## Run the Project
### Create virtual environment
```
# Creating a virtual environment inside the project directory
python3 -m venv <virtualEnvName>

# activation
source <virtualEnvName>/bin/activate
```

use any name for your environment, replace `<virtualEnvName>` (like `chatbot_env`)

### Install project dependencies
```
pip install -r requirements.txt
```

### Traing model
Go to ML folder and run

```
python main.py
```

After Taining of model, copy genrated files (all modedel.tflean filed, data.pickle) to server_django folder.

### Running Django server
```
python manage.py runserver
```
