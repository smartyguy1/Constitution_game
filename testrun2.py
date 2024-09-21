import requests
from bs4 import BeautifulSoup

def extract_section_text(section_number):
    
    url = 'https://indiankanoon.org/doc/237570/'
    response = requests.get(url)

    
    soup = BeautifulSoup(response.text, 'html.parser')

    
    div_content = soup.find('div', class_='akn-akomaNtoso', id='div_1')

    if div_content:
        
        span_act = div_content.find('span', class_='akn-act', attrs={'data-name': 'act'})

        if span_act:
            
            span_body = span_act.find('span', class_='akn-body')

            if span_body:
                
                section_id = f"section_{section_number}"
                section_content = span_body.find('section', class_='akn-section', id=section_id)

                if section_content:
                    
                    return section_content.get_text(separator='\n', strip=True)#has to be changed
                else:
                    return f"Section {section_number} not found." #This has to be false
                
            else:
                return "No 'akn-body' span found."
        else:
            return "No 'akn-act' span found."
    else:
        return "No 'akn-akomaNtoso' div found."



section_number = 39 #This is the article number
  # Replace with any number like 1, 2, 3, etc.
section_text = extract_section_text(section_number)
print(section_text)
