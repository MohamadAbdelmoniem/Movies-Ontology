import rdflib
from rdflib import Namespace
import tkinter as tk
from tkinter import ttk, scrolledtext

# Load OWL file and setup RDF graph
g = rdflib.Graph()

# Define and bind your namespace
YOUR_NS = Namespace("http://www.semanticweb.org/dell/ontologies/2024/3/untitled-ontology-4#")
g.namespace_manager.bind('your_ns', YOUR_NS, override=False)

try:
    g.parse("Movies.ttl", format="turtle")
except Exception as e:
    print("Failed to parse OWL file:", e)

def query_films(include_actors=None, exclude_actors=None, include_directors=None, exclude_directors=None, include_genres=None, exclude_genres=None):
    # Prepare lists based on input or default to empty lists if None
    include_actors = [a.strip() for a in include_actors if a.strip()] if include_actors else []
    exclude_actors = [a.strip() for a in exclude_actors if a.strip()] if exclude_actors else []
    include_directors = [d.strip() for d in include_directors if d.strip()] if include_directors else []
    exclude_directors = [d.strip() for d in exclude_directors if d.strip()] if exclude_directors else []
    include_genres = [g.strip() for g in include_genres if g.strip()] if include_genres else []
    exclude_genres = [g.strip() for g in exclude_genres if g.strip()] if exclude_genres else []

    # Construct the SPARQL query
    query_parts = [
        "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
        "PREFIX your_ns: <http://www.semanticweb.org/dell/ontologies/2024/3/untitled-ontology-4#>",
        "SELECT DISTINCT ?filmTitle WHERE {",
        "    ?film rdf:type your_ns:Movie;",
        "          your_ns:hasTitle ?filmTitle."
    ]
    
    # Adding OPTIONAL clauses to bind properties only if needed
    optional_parts = []
    if include_actors or exclude_actors:
        optional_parts.append("?film your_ns:hasActor ?actor. ?actor your_ns:hasName ?actorName.")
    if include_directors or exclude_directors:
        optional_parts.append("?film your_ns:hasDirector ?director. ?director your_ns:hasName ?directorName.")
    if include_genres or exclude_genres:
        optional_parts.append("?film your_ns:hasGenre ?genre. ?genre your_ns:genreName ?genreName.")
    
    # Join optional parts into the query
    if optional_parts:
        query_parts.append("OPTIONAL {" + " ".join(optional_parts) + "}")

    # Building filters
    filters = []
    if include_actors:
        included_actors_list = ','.join(f'"{x}"' for x in include_actors)
        filters.append(f"?actorName IN ({included_actors_list})")
    if exclude_actors:
        excluded_actors_list = ','.join(f'"{x}"' for x in exclude_actors)
        filters.append(f"NOT EXISTS {{ ?film your_ns:hasActor ?exActor. ?exActor your_ns:hasName ?exActorName. FILTER (?exActorName IN ({excluded_actors_list})) }}")
    if include_directors:
        included_directors_list = ','.join(f'"{x}"' for x in include_directors)
        filters.append(f"?directorName IN ({included_directors_list})")
    if exclude_directors:
        excluded_directors_list = ','.join(f'"{x}"' for x in exclude_directors)
        filters.append(f"NOT EXISTS {{ ?film your_ns:hasDirector ?exDirector. ?exDirector your_ns:hasName ?exDirectorName. FILTER (?exDirectorName IN ({excluded_directors_list})) }}")
    if include_genres:
        included_genres_list = ','.join(f'"{x}"' for x in include_genres)
        filters.append(f"?genreName IN ({included_genres_list})")
    if exclude_genres:
        excluded_genres_list = ','.join(f'"{x}"' for x in exclude_genres)
        filters.append(f"NOT EXISTS {{ ?film your_ns:hasGenre ?exGenre. ?exGenre your_ns:genreName ?exGenreName. FILTER (?exGenreName IN ({excluded_genres_list})) }}")
    
    # Applying filters
    if filters:
        query_parts.append("FILTER (" + ' && '.join(filters) + ")")

    query_parts.append("}")
    query = "\n".join(query_parts)
    
    results = g.query(query)
    return [str(row[0]) for row in results]


# UI Function to filter movies
def filter_movies():
    included_actors = [actor.strip() for actor in entry_actor_include.get().split(',') if actor.strip()]
    excluded_actors = [actor.strip() for actor in entry_actor_exclude.get().split(',') if actor.strip()]
    included_directors = [director.strip() for director in entry_director_include.get().split(',') if director.strip()]
    excluded_directors = [director.strip() for director in entry_director_exclude.get().split(',') if director.strip()]
    included_genres = [genre.strip() for genre in entry_genre_include.get().split(',') if genre.strip()]
    excluded_genres = [genre.strip() for genre in entry_genre_exclude.get().split(',') if genre.strip()]

    # Query for filtered movies
    filtered_movies = query_films(included_actors, excluded_actors, included_directors, excluded_directors, included_genres, excluded_genres)

    # Update the text widget with results or a "no movies found" message
    txt_result.config(state=tk.NORMAL)
    txt_result.delete(1.0, tk.END)
    if filtered_movies:
        txt_result.insert(tk.INSERT, "\n".join(filtered_movies))
    else:
        txt_result.insert(tk.INSERT, "No movies found")
    txt_result.config(state=tk.DISABLED)

# Setting up the GUI
app = tk.Tk()
app.title("Film Finder")

label_actor_include = ttk.Label(app, text="Include Actors (comma-separated):")
label_actor_include.pack()
entry_actor_include = ttk.Entry(app, width=50)
entry_actor_include.pack()

label_actor_exclude = ttk.Label(app, text="Exclude Actors (comma-separated):")
label_actor_exclude.pack()
entry_actor_exclude = ttk.Entry(app, width=50)
entry_actor_exclude.pack()

label_director_include = ttk.Label(app, text="Include Directors (comma-separated):")
label_director_include.pack()
entry_director_include = ttk.Entry(app, width=50)
entry_director_include.pack()

label_director_exclude = ttk.Label(app, text="Exclude Directors (comma-separated):")
label_director_exclude.pack()
entry_director_exclude = ttk.Entry(app, width=50)
entry_director_exclude.pack()

label_genre_include = ttk.Label(app, text="Include Genres (comma-separated):")
label_genre_include.pack()
entry_genre_include = ttk.Entry(app, width=50)
entry_genre_include.pack()

label_genre_exclude = ttk.Label(app, text="Exclude Genres (comma-separated):")
label_genre_exclude.pack()
entry_genre_exclude = ttk.Entry(app, width=50)
entry_genre_exclude.pack()

btn_search = ttk.Button(app, text="Find Films", command=filter_movies)
btn_search.pack()

txt_result = scrolledtext.ScrolledText(app, width=60, height=10)
txt_result.pack()
txt_result.config(state=tk.DISABLED)

app.mainloop()
