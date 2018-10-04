#!/usr/bin/env python3

# -------
# imports
# -------

from math import sqrt
import pickle
from requests import get
from os import path
from numpy import sqrt, square, mean, subtract


def create_cache(filename):
    """
    filename is the name of the cache file to load
    returns a dictionary after loading the file or pulling the file from the public_html page
    """
    cache = {}
    filePath = "/u/fares/public_html/netflix-caches/" + filename

    if path.isfile(filePath):
        with open(filePath, "rb") as f:
            cache = pickle.load(f)
    else:
        webAddress = "http://www.cs.utexas.edu/users/fares/netflix-caches/" + \
            filename
        bytes = get(webAddress).content
        cache = pickle.loads(bytes)

    return cache

#---------------------------------------------------

#dict: (customer,movie): rating
ACTUAL_CUSTOMER_RATING = create_cache(
    "cache-actualCustomerRating.pickle")

#dict: (customer,movie):year of rating
YEAR_OF_RATING = create_cache("cache-yearCustomerRatedMovie.pickle")

#dict: (movie,year):avg rating
AVERAGE_MOVIE_RATING_PER_YEAR = create_cache(
    "cache-movieAverageByYear.pickle")
#average rating for movie
AVERAGE_MOVIE_RATING = {}
for x,y in AVERAGE_MOVIE_RATING_PER_YEAR:
	if x in AVERAGE_MOVIE_RATING:
		AVERAGE_MOVIE_RATING[x] = (AVERAGE_MOVIE_RATING[x] + AVERAGE_MOVIE_RATING_PER_YEAR[(x,y)])/2
	else:
		AVERAGE_MOVIE_RATING[x] = AVERAGE_MOVIE_RATING_PER_YEAR[(x,y)]

#dict: (customer,year):avg rating
CUSTOMER_AVERAGE_RATING_YEARLY = create_cache(
    "cache-customerAverageRatingByYear.pickle")
#avg customer rating
AVERAGE_CUSTOMER_RATING = {}
for x,y in CUSTOMER_AVERAGE_RATING_YEARLY:
	if x in AVERAGE_CUSTOMER_RATING:
		AVERAGE_CUSTOMER_RATING[x] = (AVERAGE_CUSTOMER_RATING[x] + CUSTOMER_AVERAGE_RATING_YEARLY[(x,y)])/2
	else:
		AVERAGE_CUSTOMER_RATING[x] = CUSTOMER_AVERAGE_RATING_YEARLY[(x,y)]

movie_year_cache = dict((x,y) for x,y in AVERAGE_MOVIE_RATING_PER_YEAR.keys())
from collections import defaultdict
actual_scores_cache = defaultdict(dict)
for x,y in ACTUAL_CUSTOMER_RATING:
	actual_scores_cache[y][x] = ACTUAL_CUSTOMER_RATING[(x,y)]
actual_scores_cache = dict(actual_scores_cache)

# ------------
# netflix_eval
# ------------

def netflix_eval(reader, writer) :
    predictions = []
    actual = []

    # iterate throught the file reader line by line
    for line in reader:

    # need to get rid of the '\n' by the end of the line
        line = line.strip()

        # check if the line ends with a ":", i.e., it's a movie title 
        if line[-1] == ':':

		# It's a movie
            current_movie = line.rstrip(':')
            pred = movie_year_cache[int(current_movie)]
            pred = (pred // 10) *10

            writer.write(line)
            writer.write('\n')
        else:
		# It's a customer
            current_customer = line
            #yr of rating
            yr = YEAR_OF_RATING[(int(current_customer),int(current_movie))]
            #current customer's average rating that year
            customer_avg_rating_this_year = CUSTOMER_AVERAGE_RATING_YEARLY[(int(current_customer),yr)]
            prediction = (AVERAGE_MOVIE_RATING[int(current_movie)] + customer_avg_rating_this_year)/2
            predictions.append(prediction)
            actual.append(actual_scores_cache[int(current_movie)][int(current_customer)])
            writer.write(str(round(prediction,1)))  
            writer.write('\n')	
    # calculate rmse for predications and actuals
    rmse = sqrt(mean(square(subtract(predictions, actual))))
    writer.write(str(rmse)[:4] + '\n')
