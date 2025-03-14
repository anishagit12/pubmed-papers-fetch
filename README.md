A command-line tool to fetch research papers from PubMed and identify those with at least one author affiliated with a pharmaceutical or biotech company.
_________________________________________________________________________________________________________________________________________________________
Setup

1. Clone the repository: 
git clone ‘https://github.com/anishagit12/pubmed-papers-fetch’
cd get-papers-list
2. Install dependencies using Poetry: 
poetry install
_______________________________________________________________________________________________________________

Usage
Run the command using:
‘poetry run python src/get_papers_list/get_papers.py "[your query]" -f [filename].csv -d’
_______________________________________________________________________________________________________________

Example Usage
Fetch papers related to cancer immunotherapy and save the results to papers.csv:
poetry run python src/get_papers_list/get_papers.py "cancer and immunotherapy" -f cancerimmuno2.csv
Run in debug mode:
poetry run python src/get_papers_list/get_papers.py "cancer and immunotherapy" -f cancerimmuno2.csv -d
_______________________________________________________________________________________________________________
Project Structure
├── src/                   	# Source code directory
│   ├── get_papers_list/   	# Package containing the main functionality
│   │   ├── __init__.py    	# Makes it a Python package
│   │   ├── get_papers.py  	# Main script handling API requests and parsing
├── tests/                 	# Unit tests
│   ├── __init__.py        	# Makes it a test package
├── poetry.lock            	# Poetry lock file for dependencies
├── pyproject.toml         	# Poetry dependencies and project config
├── README.md              	# Documentation