#importing the required libraries
import requests
import pandas as pd
import argparse
from datetime import datetime
import xml.etree.ElementTree as ET

#function to fetch papers from PubMed Entrez API
def fetch_paper_ids(query, max_results=10):
    url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "xml"
    }
    response = requests.get(url, params=params)
    return response.text

#fetch details of the paper with PubMed ID as pmid
def fetch_paper_details(pmid):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params={
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }
    response = requests.get(url, params=params)
    return response.text

#parse the paper details
def parse_paper_details(xml_response):
    
    root = ET.fromstring(xml_response)
    papers = []

    #iterates through all articles to extract specific info
    for article in root.findall(".//PubmedArticle"):
        paper = {}

        #extract ID
        pmid = article.find(".//PMID").text if article.find(".//PMID") is not None else "N/A"
        paper["PubMedID"] = pmid

        #extract title    
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
        paper["Title"] = title

        #extract publication date
        pub_date = article.find(".//PubDate")
        if pub_date is not None:
            pub_year = pub_date.find("Year").text if pub_date.find("Year") is not None else "N/A"
            pub_month = pub_date.find("Month").text if pub_date.find("Month") is not None else "N/A"
            paper["Publication Date"] = f"{pub_year}-{pub_month}-01"
        else:
            paper["Publication Date"] = "N/A"
        
        #extract industry-affiliation
        non_academic_authors = []
        company_affiliations = []
        for author in article.findall(".//Author"):
            last_name = author.find("LastName").text if author.find("LastName") is not None else "N/A"
            fore_name = author.find("ForeName").text if author.find("ForeName") is not None else "N/A"
            affiliation = author.find("AffiliationInfo/Affiliation").text if author.find("AffiliationInfo/Affiliation") is not None else "N/A"

            if "pharma" in affiliation.lower() or "biotech" in affiliation.lower():
                company_affiliations.append(affiliation)
            else:
                non_academic_authors.append(f"{fore_name} {last_name}")
        
        paper["Non-academic authors"] = ", ".join(non_academic_authors)
        paper["Company Affiliations"] = ", ".join(company_affiliations)

        #extract corresponding author's email
        corresponding_email = article.find(".//CorrespondingAuthor/Email")
        paper["Corresponding Author Email"] = corresponding_email.text if corresponding_email is not None else "N/A"
        
        papers.append(paper)
    
    return papers

#save result to csv file
def save_to_csv(data, filename="papers.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

#parsing command-line args
def parse_args():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Query to search papers on PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the results.", default="papers.csv")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information.")
    return parser.parse_args()

#main function
def main():
    args = parse_args()

    if args.debug:
       print(f"Searching for papers with query: {args.query}")

    xml_response = fetch_paper_ids(args.query)

    root = ET.fromstring(xml_response)
    paper_ids = [id_elem.text for id_elem in root.findall(".//IdList/Id")]

    papers_data = []

    for pmid in paper_ids:
        if args.debug:
            print(f"Fetching details for PubMed ID: {pmid}")
        paper_details = fetch_paper_details(pmid)
        parsed_papers = parse_paper_details(paper_details)
        papers_data.extend(parsed_papers)

    save_to_csv(papers_data, args.file)
    print(f"Results saved to {args.file}")

#running the script
if __name__ == "__main__":
    main()