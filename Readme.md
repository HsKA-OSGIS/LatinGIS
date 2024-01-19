
# ![App Screenshot](https://lh3.googleusercontent.com/drive-viewer/AEYmBYSAC6Pz8NQpUg7-1ro83hoCihYHJ8BAfxwDh90ZoMwtnIjGuTf5-YnW1NU8Fihx3YFuLF6NsWDNREZnigLqg3xlTLrY=w210-h991) LatinGIS

LatinGIS is a group of three students of HKA University in Karlsruhe (Germany) that are creating a project of "15-Minute City" for the faculty of Geomatics in the subject Open Source GIS in Master of Geomatics.

The goal of this project is get resources of facilities in the city of Karlsruhe and show them in a map. User will be able to select a point and check what facilities are closer to that point. The distance between the point and the facilities is given by the choosen mode of transport (by walk or bike) and the time that you want to spend (5, 10 or 15 minutes).

The final data recollected is given visualized in the map and in a list. That data can be exported as csv file.
## Authors

- [@dpulidogeology](https://github.com/dpulidogeology)  as Fronted developer,Geospatial Data
- [@NestorVillanueva](https://github.com/NestorVillanueva) as Geospatial developer
- [@TheIvansito](https://github.com/TheIvansito) as Backend developer,Geospatial Developer
+ [@mlechner](https://github.com/mlechner) as Teacher


## Features

#### Frontend
+ Web page with map
+ Geovisual data from server of Transparenz Karlsruhe Portal
+ Download data from map
#### Backend
- WPS server
- Unique WPS tools
- Python files for internal operations


## Installation

Basic guide for Installation. For more info and detailed installation, please read Readme from Backend, Frontend and libraries inside of them.

#### Frontend
```bash
  git clone
  npm i
  npm run dev
```
Excecuted on [localhost:3000](localhost:3000)

#### Backend
```bash

  sudo apt install python3-virtualenv
  virtualenv -p python3 pywps_flask_env
  . bin/activate
  cd pywps-flask
  pip3 install -r requirements.txt
  python3 demo.py -a
```
Excecuted on [localhost:5000](localhost:5000)
## FAQ

#### Can I clone this repository?

Yes

#### I need a virtual machine or special SO to run this?

No. You can run this wherever you want.

#### I need to give files to Backend to work with my data?

If you are in online mode, you need to change the URL in settings from Backend.
If you are in offline mode, you can replace data with yours in data folder. This has to be conected online after this.

#### What type of data do you use?

We use data from json files that are stored online.



## Libraries from Github

 - [Nuxt](https://nuxt.com/)
 - [VueJS](https://vuejs.org/)
 - [OpenLayers](https://openlayers.org/)
 - [TailWind css](https://tailwindcss.com/)
 - [PyWPS - Flask](https://github.com/geopython/pywps-flask)


## License

[MIT](https://choosealicense.com/licenses/mit/)

Copyright (c) 2023 LatinGIS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
## Feedback

If you have any feedback, please reach out to us at siiv1011@h-ka.de

