# comspacity
Using Spacy to return the complexity of a document.
## Installation
Open a terminal and copy or clone the repository.\
`$ cd comspacity`\
It is required that docker and docker compose are installed and running in your machine in advance.\
`$ docker-compose up`\
Open a web browser and go to either `http://127.0.0.1:8501` or `http://localhost:8501`.
## Usage
1. Choose a language
2. Choose if you want the complexity-score of the whole document or if you want the complexity-score of each sentence.
3. Enter a snippet and press ⌘+Enter to see the complexity-score.
### Example
When you open the site you will be greated by this:
<img width="725" alt="Bildschirmfoto 2022-09-09 um 14 15 06" src="https://user-images.githubusercontent.com/41857601/189454833-35290d0f-5a70-4586-9947-b46feb0ad5be.png">

**If you enter this text:**
>*Natural language processing (NLP) is a theory-motivated range of computational techniques for the automatic analysis and representation of human language. NLP research has evolved from the era of punch cards and batch processing (in which the analysis of a sentence could take up to 7 minutes) to the era of Google and the likes of it (in which millions of webpages can be processed in less than a second). This review paper draws on recent developments in NLP research to look at the past, present, and future of NLP technology in a new light. Borrowing the paradigm of ‘jumping curves’ from the field of business management and marketing prediction, this survey article reinterprets the evolution of NLP research as the intersection of three overlapping curves - namely Syntactics, Semantics, and Pragmatics Curves - which will eventually lead NLP research to evolve into natural language understanding.*
<img width="738" alt="Bildschirmfoto 2022-09-09 um 14 13 21" src="https://user-images.githubusercontent.com/41857601/189454746-4a5c5f7e-eb9e-4940-bc99-b1d40e6a67e7.png">

If you now change to analyse the complexity of each sentence. You will see the most complex sentence at the top. \
<img width="739" alt="Bildschirmfoto 2022-09-09 um 14 14 36" src="https://user-images.githubusercontent.com/41857601/189454854-9c76934e-82cc-480d-9c11-7636be53e83c.png">
