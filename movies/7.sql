SELECT rating, title FROM movies INNER JOIN ratings ON (movies.id = ratings.movie_id) WHERE year = "2010" AND rating 
IS NOT 'NULL' ORDER BY rating DESC, title ASC;