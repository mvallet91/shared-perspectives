# PyQt imports ####################################################################
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from testWindow2 import Ui_Dialog

# Data input imports ##############################################################
import pickle
import ast

# Process and calculation imports #################################################
from scipy import spatial
import operator
import random

# Image stuff #####################################################################
from PIL import Image
from PIL.ImageQt import ImageQt
import urllib.request
import numpy as np
import io

### Connect to database ############################################################

# config = dict(server=   'localhost', 
#               port=      1433,                  
#               database= 'name',
#               username= 'user',
#               password= 'password')

# connection_string = ('SERVER={server},{port};'   +
#                      'DATABASE={database};'      +
#                      'UID={username};'           +
#                      'PWD={password}')

# conn = pyodbc.connect(
#     r'DRIVER={ODBC Driver 13 for SQL Server};' +
#     connection_string.format(**config)
#     )

# cursor = conn.cursor()

### Get data from database (example) ###############################################

# just_movies = []
# cursor.execute("SELECT * FROM movies")
# movies = cursor.fetchall()
# for movie in movies:
#     if not 'season' in str(movie[1]).lower():
#         if not 'series' in str(movie[1]).lower():
#             if not 'collect' in str(movie[1]).lower():
#                 if not 'pack' in str(movie[1]).lower():
#                     if movie[3] != None:
#                         just_movies.append(movie[0])

### Get data from picke files, if database is not set up ############################

with open("data/just_movies.pickle", "rb") as input_file:
    just_movies = pickle.load(input_file)

with open("data/overviews.pickle", "rb") as input_file:
    overviews = pickle.load(input_file)

with open("data/movie2vec_perspectives.pickle", "rb") as input_file:
    movie2vec_perspectives = pickle.load(input_file)

with open("data/review_text.pickle", "rb") as input_file:
    inverted_reviews = pickle.load(input_file)

with open("data/poster_urls.pickle", "rb") as input_file:
    poster_urls = pickle.load(input_file)

###  Function to create display of similar movies ###################################
def generateDisplay(selected_movie):

	# List of discarded items, those that have already been shown in the process
	discarded = []

	discarded.append(selected_movie)

	display = []
	display_text = {}
	x = 0

	# Calculate similar SPTs to the SPTs of the EI
	for base in movie2vec_perspectives[selected_movie]:
	    v1 = base[2:102]
	    cosine = {}
	    for key in movie2vec_perspectives:
	        if key not in discarded:
	            for perspective in movie2vec_perspectives[key]:
	                v2 = perspective[2:102]
	                v1v2 = str(perspective[0])
	                cosine[v1v2] = 1 - spatial.distance.cosine(v1, v2)
	    sorted_cosine = sorted(cosine.items(), key=operator.itemgetter(1), reverse=True) 
	    topk_cosine = sorted_cosine[:6]

	    # Select m top similar SPTs for every SPT of EI, and check that the result items are not already in the display	    
	    for perspective in topk_cosine:
	        s = perspective[0]
	        movie = s[(s.index('|')+1):]
	        if movie not in display:
	        	if movie != selected_movie:
		            display.append(movie)
		            display_text[x] = inverted_reviews[perspective[0]]
		            x = x + 1
		            if len(display) % 3 == 0 and len(display) != 0:
		                break
	return(display, display_text)

def generatePerspectives(selected_movie):

	perspectives = {}
	for x in range(len(movie2vec_perspectives[selected_movie])):
		perspectives[x] = inverted_reviews[movie2vec_perspectives[selected_movie][x][0]]

	return(perspectives)

class TestProgram(Ui_Dialog):
	def __init__(self, dialog):
		#super(TestProgram, self).__init__(parent)
		Ui_Dialog.__init__(self)
		self.setupUi(dialog)
		self.my_dialog = dialog

### Read list of movies for the experiment #######################################
		with open('experiments/experiment_results.txt', 'r') as file:
		    movie_list = file.readline()
		    results = file.readlines()

### Get next movie from the list of experiment movies ############################
### Once done with the experiment, participants were free to write 'random' in ###
### the results file so they could just keep exploring random movies. ############

		if movie_list == 'random\n':
			current_movie = random.choice(just_movies)
		else:
			movie_list = ast.literal_eval(movie_list)
			current_movie = movie_list[len(results)]

		displays = generateDisplay(current_movie)
		display = displays[0]
		display_text = displays[1]

		perspectives = generatePerspectives(current_movie)
		movies = display

### Get image from URL for EI  ####################################################
		URL = poster_urls[current_movie]
		with urllib.request.urlopen(URL) as url:
		     f = io.BytesIO(url.read())
		img = Image.open(f)
		qimage = ImageQt(img)
		pixmap = QtGui.QPixmap.fromImage(qimage)
		pixmap_test = pixmap.scaledToWidth(145)

### Add EI poster to window #######################################################
		self.label_selected.setPixmap(pixmap_test)

### Add EI overview to window #####################################################
		overview = overviews[current_movie]
		self.overview.textCursor().insertHtml(str(overview))

### Get images from URL for all items in the display  ##############################
		movie_image = {}
		for x in range(len(movies)):
			URL = poster_urls[movies[x]]
			with urllib.request.urlopen(URL) as url:
			    f = io.BytesIO(url.read())
			img = Image.open(f)
			qimage = ImageQt(img)
			pixmap = QtGui.QPixmap.fromImage(qimage)
			pixmap_test = pixmap.scaledToWidth(145)
			movie_image[x] = pixmap_test

### Populate window #################################################################

		#self.label.setPixmap(pixmap_test)
		self.label.setPixmap(movie_image[0])
		self.label_2.setPixmap(movie_image[1])
		self.label_3.setPixmap(movie_image[2])
		self.label_4.setPixmap(movie_image[3])
		self.label_5.setPixmap(movie_image[4])
		self.label_6.setPixmap(movie_image[5])
		self.label_7.setPixmap(movie_image[6])
		self.label_8.setPixmap(movie_image[7])
		self.label_9.setPixmap(movie_image[8])

		self.textEdit_1.textCursor().insertHtml(str(perspectives[0]))
		self.textEdit_2.textCursor().insertHtml(str(perspectives[1]))
		self.textEdit_3.textCursor().insertHtml(str(perspectives[2]))

		self.textEdit_A.textCursor().insertHtml(str(display_text[0]))
		self.textEdit_A2.textCursor().insertHtml(str(display_text[1]))
		self.textEdit_A3.textCursor().insertHtml(str(display_text[2]))
		self.textEdit_A4.textCursor().insertHtml(str(display_text[3]))
		self.textEdit_A5.textCursor().insertHtml(str(display_text[4]))
		self.textEdit_A6.textCursor().insertHtml(str(display_text[5]))
		self.textEdit_A7.textCursor().insertHtml(str(display_text[6]))
		self.textEdit_A8.textCursor().insertHtml(str(display_text[7]))
		self.textEdit_A9.textCursor().insertHtml(str(display_text[8]))

		self.nextBttn.clicked.connect(self.clearAndShowNext)

		#self.seenMovie
		with open('experiments/experiment_results.txt', 'a') as file:
			file.write(current_movie+', ')

	def clearAndShowNext(self):

		P1 = self.textEdit_P1.toPlainText()
		P2 = self.textEdit_P2.toPlainText()
		P3 = self.textEdit_P3.toPlainText()
		
		B1 = str(self.checkBox_1.isChecked())
		B2 = str(self.checkBox_2.isChecked())
		B3 = str(self.checkBox_3.isChecked())
		B4 = str(self.checkBox_4.isChecked())
		B5 = str(self.checkBox_5.isChecked())
		B6 = str(self.checkBox_6.isChecked())
		B7 = str(self.checkBox_7.isChecked())
		B8 = str(self.checkBox_8.isChecked())
		B9 = str(self.checkBox_9.isChecked())

### Save results ####################################################################

		with open('experiments/experiment_results.txt', 'a') as file:
			file.write(self.seenMovie.currentText()+', '+self.comboBox.currentText()+', '+self.comboBox_2.currentText()+', '+self.comboBox_3.currentText()+
						"', '"+P1+"', '"+P2+"', '"+P3+"', "+B1+', '+B2+', '+B3+', '+B4+', '+B5+', '+B6+', '+B7+', '+B8+', '+B9+'\n')
		self.my_dialog.close()
		#child = TestProgram(dialog)
		#dialog.show()

if __name__ == '__main__':

	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QDialog()
	testProg = TestProgram(dialog)
	dialog.show()

	sys.exit(app.exec_())
