import requests
from bs4 import BeautifulSoup
import re


url = 'https://indiankanoon.org/doc/237570/'
response = requests.get(url)


soup = BeautifulSoup(response.text, 'html.parser')


div_content = soup.find('div', class_='akn-akomaNtoso', id='div_1')


if div_content:
    span_content = div_content.find('span', class_='akn-act', attrs={'data-name': 'act'})

    
    if span_content:
        section_content = span_content.find('section', class_='akn-preamble')
        
        
       
            
            
        main_text = section_content.get_text(separator='\n', strip=True)
            
           
            
        print(main_text)
        
    else:
        print("Couldn't find the span with the 'akn-act' class.")
else:
    print("Couldn't find the div with id 'div_1'.")
