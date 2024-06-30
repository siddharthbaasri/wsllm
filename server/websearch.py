from llm import Groq_llm
import chromadb
from google_search import getSearchJSON
import concurrent.futures
from helpers import headers
import requests
from bs4 import BeautifulSoup
import re
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter



class Websearch:
    def __init__(self):
        self.llm = Groq_llm()
        self.chroma_client = chromadb.Client() 

    def search(self, query_string):
        links = getSearchJSON(query_string)
        search_contexts = self.get_search_contexts(links, query_string)
        return self.llm.getFinalAnswer(query_string, search_contexts)


    def get_search_contexts(self, links, prompt):
        formatted_results = ""

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(self.downloadFile, links[i]): i for i in range(0, len(links))}
            index = 1
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if len(result['content']) < 150:
                    continue
                searchResult = self.vectorizeText(result['content'], prompt)
                for doc in searchResult['documents'][0]:
                    formatted_results += f"[{index}] {result['url']}\n{doc}\n\n"
                index += 1

        return formatted_results
    
    def downloadFile(self, link):
        link['content'] = ""
        try:
            response = requests.get(link['url'], headers = headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser") # Parse the HTML   
                link['content'] = re.sub(r'\s+', ' ', soup.get_text().replace('\n', ' '))
        except:
            pass
        return link
    
    def vectorizeText(self, text, userPrompt):
        text = text[:5000]
        splitTexts = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200).split_text(text)
        name = str(uuid.uuid4())
        collection = self.chroma_client.create_collection(name = name)
        collection.add (
            documents=splitTexts,
            ids=[str(i) for i in range(len(splitTexts))]
        )
        results = collection.query(
            query_texts=[userPrompt], 
            n_results=5
        )
        self.chroma_client.delete_collection(name)
        return results

    
    