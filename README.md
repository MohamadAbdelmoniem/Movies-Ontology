# Film Finder

## Description

Film Finder is a Python application that leverages semantic web technologies to enable users to search for films based on specified criteria, such as included or excluded actors, directors, and genres. Utilizing RDF data and SPARQL queries, this application provides a sophisticated way to navigate through movie datasets, making it easier to find films that match user preferences.

## Features

- **Flexible Search Criteria:** Allows users to include or exclude actors, directors, and genres in their film searches.
- **Semantic Web Integration:** Utilizes RDF (Resource Description Framework) and SPARQL to interact with semantic web data.
- **User-friendly Interface:** Features a simple and intuitive GUI built with Tkinter for ease of use.

## Installation

To run Film Finder, ensure you have Python and the necessary dependencies installed:

### Prerequisites

- Python 3.7 or higher
- rdflib
- tkinter (typically included with Python)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MohamadAbdelmoniem/Movies-Ontology.git
   cd Movies-Ontology
   ```

2. **Install RDFlib:**

   Install RDFlib using pip. If pip is not installed, [follow these instructions](https://pip.pypa.io/en/stable/installation/).

   ```bash
   pip install rdflib
   ```

3. **Run the Application:**

   Start the application using Python.

   ```bash
   python film_finder.py
   ```

## Usage

After starting Film Finder, the application window will present multiple text fields for input:

- **Include Actors / Exclude Actors:** Names of actors to include or exclude, separated by commas.
- **Include Directors / Exclude Directors:** Names of directors to include or exclude, separated by commas.
- **Include Genres / Exclude Genres:** Genres to include or exclude, separated by commas.

Input your search criteria and click the "Find Films" button to display results in the text area below the button.
