from TwitterAPI import TwitterAPI
import time
from flask import Flask
import os
from flask import Flask, render_template, request, redirect, session, send_from_directory

import unicodedata
import string
import mechanize
import random
import requests
import wikipedia
import StringIO

app = Flask(__name__,static_url_path='')

with open('lat-long.damei','r') as f :
	latlong = [ x.split(';') for x in f.read().split('\n')][:-1]

with open('rand.txt','r') as f :
	d_latlong = [ x.split(';') for x in f.read().split('\n')][:-1]

print len(latlong)


if os.getenv("VCAP_APP_PORT"):
	port = int(os.getenv("VCAP_APP_PORT"))
else:
	port = 8080

def refine(string) :
	newString = ''
	string.replace("\s","")
	for char in string :
		try :
			newString += str(char)
		except :
			pass
	return newString


def mech(content) :
		browser = mechanize.Browser()
		browser.set_handle_robots(False)
		browser.addheaders = [('User-Agent','Firefox')]
		browser.open('http://um-python.mybluemix.net/')
		browser.select_form(nr=0)
		browser.form['content'] = content
		browser.submit()
		html = browser.response().read().split('<h2>Output</h2>')[1]		
		return html

def wiki(keyword) :	
	print wikipedia.search(keyword,suggestion=True)
	result = wikipedia.search(keyword,suggestion=True)[0]
	wikiPage = wikipedia.page(result)
	content = refine(wikiPage.content)[:1000]	
	return mech(content)

def maps(keyword) :	
	CONSUMER_KEY = 'rvQKnkf1sBMFBawgRxwL7Ndxx'
	CONSUMER_SECRET = 'A1DI4M2pSMnXoEZLIjYI5OCxF3yoXXpZ7lcsj9bHgMRkfIagrn'
	OAUTH_TOKEN = '1190893374-ZzE3xyn4tz2RXrDsLEoeiaSUHs8nTK1yhuv3uPa'
	OAUTH_TOKEN_SECRET = 'EiE3Akjs1KpokGx3av7opROQOKAhcKpjMKs3obmdiiq4r'

	api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

	#random.shuffle(d_latlong)
	#print d_latlong[1]
	Tweets = [ ]
	temp = latlong
	for item in d_latlong[:1000] :
		temp.append(d_latlong[random.randrange(0,len(d_latlong))])
	for item in temp:
		try :
			Tweets.append(['', float(item[-2][1:-1]) , float(item[-3][1:-1]) ,random.randrange(10,50) ])
		except :
			pass
	return Tweets

@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('css', path)

@app.route('/fonts/<path:path>')
def send_font(path):
	return send_from_directory('fonts', path)

@app.route('/static/<path:path>')
def send_static_file(path):
	return send_from_directory('static', path)

@app.route('/')
def hi_world():
	return '''
	<!DOCTYPE html>
<html lang="en" class="no-js">
	<head>
				<meta charset="UTF-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 
		<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
		<title> swagShakti</title>
		<meta name="description" content="Natural Language Form with custom text input and drop-down lists" />
		<meta name="keywords" content="Natural Language UI, sentence form, text input, contenteditable, html5, css3, jquery" />
		<meta name="author" content="Codrops" />
		<link rel="shortcut icon" href="../favicon.ico"> 
		<link rel="stylesheet" type="text/css" href="css/default.css" />
		<link rel="stylesheet" type="text/css" href="css/component.css" />
		<script src="js/modernizr.custom.js"></script>
		<script src="js/jquery.js"></script>
		<script>
				$("#pastRecords").click(function(){
					window.location.replace("/results?q="+$('#page-content-wrapper').value);

				});
		</script>
	</head>
	<body class="nl-blurred">
		<div class="container demo-1">
			<!-- Top Navigation -->
			<div class="codrops-top clearfix">
				
			</div>
			<header>
				<h1> Welcome <span> </span></h1>	
			</header>
			<div class="main clearfix">
				<form id="nl-form" class="nl-form" method="get" action="/results">
					I would like to see how the world is responding to
					<input type="text" name="q" id="query" value="" placeholder="any product/thing" data-subline="For example: <em>iphone6</em> or <em>IBM</em>"/>
					and what they think about it.
					<div class="nl-submit-wrap">
						<button class="nl-submit" id="submit" >Let Bluemix do the rest</button>
					</div>
					<div class="nl-overlay"></div>
				</form>
			</div>
		</div><!-- /container -->
		<script src="js/nlform.js"></script>
		<script>
			var nlform = new NLForm( document.getElementById( 'nl-form' ) );
		</script>
	</body>
</html>
	'''

@app.route('/results',methods=['GET'])
def hello_world():	
	if request.method == 'GET' :		
		html = '''
			<!DOCTYPE html>
			<html>
			  <head>
				<title>swagShakti</title>
				<meta charset="utf-8"/>
				<meta http-equiv="X-UA-Compatible" content="IE=edge"/>
				<meta name="viewport" content="width=device-width, initial-scale=1"/>
				<link rel="shortcut icon" href="http://um-python.mybluemix.net/static/images/favicon.ico" type="image/x-icon"/>
				<link rel="icon" href="static/images/favicon.ico" type="image/x-icon"/>
				<link rel="stylesheet" href="http://um-python.mybluemix.net/static/css/watson-bootstrap-dark.css"/>
				<link rel="stylesheet" href="http://um-python.mybluemix.net/static/css/browser-compatibility.css"/>
				<link rel="stylesheet" href="http://um-python.mybluemix.net/static/css/watson-code.css"/>
				<link rel="stylesheet" href="http://um-python.mybluemix.net/static/css/style.css"/>
			    <meta charset="utf-8">
			    <title>Heatmaps</title>
			    <style>
			      html, body, #map-canvas {
			        height: 100%;
			        margin: 0px;
			        padding: 0px
			      }
			      #panel {
			        position: absolute;
			        top: 5px;
			        left: 50%;
			        margin-left: -180px;
			        z-index: 5;
			        background-color: #fff;
			        padding: 5px;
			        border: 1px solid #999;
			      }
			    </style>
			    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&signed_in=false&libraries=visualization"></script>
			    <script>
			// Adding 500 Data Points
			var map, pointarray, heatmap;
			var taxiData = [
  	new google.maps.LatLng(37.782551, -122.445368),
			'''
		for item in maps(request.args.get('q')) :			
			for counter in range(random.randrange(1,7))  :				
				lat = item[2]#) + random.randrange(2,2) )
				lon = item[1]#) + random.randrange(-2,2) )
				html += '''new google.maps.LatLng('''+str(lat)+''','''+str(lon)+'''),
				'''
				
		html += '''
		];

function initialize() {
  var mapOptions = {
    zoom: 3,
    center: new google.maps.LatLng(37.774546, -122.433523),
    mapTypeId: google.maps.MapTypeId.SATELLITE
  };

  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

  var pointArray = new google.maps.MVCArray(taxiData);

  heatmap = new google.maps.visualization.HeatmapLayer({
    data: pointArray
  });

  heatmap.setMap(map);
}

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}

function changeGradient() {
  var gradient = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(0, 0, 223, 1)',
    'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 159, 1)',
    'rgba(0, 0, 127, 1)',
    'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',
    'rgba(191, 0, 31, 1)',
    'rgba(255, 0, 0, 1)'
  ]
  heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 20);
}

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}

google.maps.event.addDomListener(window, 'load', initialize);

    </script>
  </head>

  <body>
    <div id="panel">
      <button onclick="toggleHeatmap()">Toggle Heatmap</button>
      <button onclick="changeGradient()">Change gradient</button>
      <button onclick="changeRadius()">Change radius</button>
      <button onclick="changeOpacity()">Change opacity</button>
      <button onclick="#">Green indicates spring</button>
      <button onclick="#">Red indicates danger</button>
    </div>
    <div id="map-canvas"></div>
    '''
		html += wiki(request.args.get('q'))
		html +=	'''
  </body>
</html>
		'''
		return html
	else :		
		return '''
		<html>
			<b> Enter a get variable 
			</b>
		</html>'''


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)
