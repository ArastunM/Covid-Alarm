## Covid-aware Alarm Clock
Covid-aware alarm clock is a Python Web-based application created 
primarily using the Flask package. It servers the purpose of 
helping the user keep up to date with the rapidly changing 
world/events and promoting a better scheduled/planned daily routine.

The program achieves this goal by maintaining the user 
with constant notification updates (briefings) of news, 
weather and COVID-19 and providing a functionality to 
add/schedule alarms.


## Prerequisites
[Python version 3.8](https://www.python.org/downloads/release/python-380/) 
was used for development


## Installation
The project mainly uses python built-in packages, however; 
there are a few external packages that require additional installation

Use [pip](https://pip.pypa.io/en/stable/) to install the following:

```bash
pip install Flask
pip install requests
pip install pyttsx3
pip install uk_covid19
pip install playsound
```


## Getting Started
Before the project is run, it should be ensured 
that the necessary modules/files are within appropriate
directories

The modules/files can be downloaded from the [GitHub repository](https://github.com/ArastunM/Covid-Alarm.git)

The directory should look as below:

```
+-- README.md
+-- static
|   +-- images
|   |   +-- alarm_icon.png
|   +-- style.css
+-- templates
|   +-- index.html
+-- testing
|   +-- test_log_operate.py
|   +-- test_retrieve_data.py
|   +-- test_side_funcs.py
+-- main.py
+-- retrieve.py
+-- announcement.py
+-- side_funcs.py
+-- sys.log
+-- config.json
+-- LICENSE.txt
+-- short_notification.mp3
```

It is recommended for the config.json file to have the following 
default values, specifically for: 
- covid data_type
- log_file format 

```json
{
  "retrieve": {
    "news": {
      "key": "your_api_key",
      "path": "https://newsapi.org/v2/top-headlines?",
      "country": "gb"
    },
    "weather": {
      "key": "your_api_key",
      "path": "http://api.openweathermap.org/data/2.5/weather?",
      "city": "Exeter"
    },
    "covid": {
      "location": ["areaName=Exeter"],
      "data_type": {
        "areaName": "areaName",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate",
        "cumDeaths28DaysByDeathDateRate": "cumDeaths28DaysByDeathDateRate"
      }
    }
  },
  "log_file": {
    "file_name": "sys.log",
    "format": "%(name)s - %(levelname)s - [%(asctime)s] - %(message)s"
  },
  "image": "alarm_icon.png",
  "notify_sound": "short_notification.mp3"
}
```

The API requests for **weather** and **news** require the use of 
an API key. These keys should be generated from below sources
and included in the configuration file

|Parameter|Type|Description|Source|
|---------|----|-----------|------|
|your_api_key|string|critical|[news](https://newsapi.org/)|
|your_api_key|string|critical|[weather](https://openweathermap.org/)|

Afterwards the program can be run, by navigating to the project 
directory in the terminal and using below command:

```bash
python main.py
```


## Used Modules
The program consists of modules given below:
- **[main.py]** - 
central module for Covid-aware alarm clock
- **[retrieve.py]** - 
used to access and retrieve external data
- **[announcement.py]** - 
used to apply announcements when called
- **[side_funcs.py]** - 
used for clarity, consisting of necessary side functions
- **[log_operate.py]** - 
used to apply logging related functions


## Testing
Testing was automated to be run using [pytest](https://pypi.org/project/pytest/)

Assuming directories are set according to **Getting Started** section,
following commands should be used in terminal to run the testing:

```bash
pip install pytest
cd [project directory]
python -m pytest
```


## Details
- Author - Arastun Mammadli
- License - [MIT](LICENSE.txt)

**Access link to [GitHub repository](https://github.com/ArastunM/Covid-Alarm.git)**
