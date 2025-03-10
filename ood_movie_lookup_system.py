"""
Problem Statement:
Design a movie scheduling system that allows users to look up movies by date. 

Requirements:
1. Find a movie for a specific date
2. If no movie is available on the requested date, find the closest date with a movie

DS:
- SortdDict
- Binary Search on sorted array
"""


from sortedcontainers import SortedDict
from datetime import date
from typing import Optional, List

class Movie:
    def __init__(self, title, show_dates=None):
        self.title = title
        self.show_dates = show_dates or []
    

class MovieScheduler:
    def __init__(self):
        """Initialize a movie scheduler with a SortedDict where dates are keys and movie lists are values."""
        self.date_to_movies = SortedDict()  # date -> [movies on that date]
    
    def add_movie(self, movie):
        """Add a movie with its show dates."""
        for show_date in movie.show_dates:
            if show_date not in self.date_to_movies:
                self.date_to_movies[show_date] = []
            self.date_to_movies[show_date].append(movie)

    def get_available_dates(self) -> List[date]:
        """Return a list of all available dates."""
        return list(self.date_to_movies.keys())
    
    def get_movie_for_date(self, query_date) -> Optional[Movie]:
        """
        Return a movie released on the given date.
        If no movie was released on that date, return a movie from the closest date.
        """
        # If no movies exist
        if not self.date_to_movies:
            return None
        
        # If we have an exact match, return it
        if query_date in self.date_to_movies:
            today_movies = self.date_to_movies[query_date]
            return today_movies[0]
        
        # Use SortedDict's built-in methods to find closest dates
        # Since query_date is not in the SortedDict
        # the bisect_left and bisect_right will return the same index
        index = self.date_to_movies.bisect_left(query_date)
        
        # If query_date is before all dates, return the first movie
        if index == 0:
            first_date = self.date_to_movies.keys()[0]
            return self.date_to_movies[first_date][0]
            
        # If query_date is after all dates, return the last movie
        if index == len(self.date_to_movies):
            last_date = self.date_to_movies.keys()[-1]
            return self.date_to_movies[last_date][0]
        
        # Get the dates before and after query_date
        before_date = self.date_to_movies.keys()[index-1]
        after_date = self.date_to_movies.keys()[index]
        
        # Compare the distances to the closest dates
        if abs(query_date - before_date) <= abs(after_date - query_date):
            return self.date_to_movies[before_date][0]
        else:
            return self.date_to_movies[after_date][0]

