# comspacity
Using Spacy to return the complexity of a document.
## Installation
Open a terminal and copy or clone the repository. Move into the directory comspacity with cd comspacity. It is required that docker and docker compose are installed and running in your machine in advance. Run docker-compose up as a command in your terminal. Open a web browser and go to either http://127.0.0.1:8501 or http://localhost:8501.
## Usage
1. Choose a language
2. Choose if you want the complexity-score of the whole document or if you want the complexity-score of each sentence.
3. Enter a snippet and press ⌘+Enter to see the complexity-score.
### Example
!["home screen"]("https://user-images.githubusercontent.com/41857601/189454260-b056ac09-448c-4d65-bd7c-a48e8d17fbc1.png")
If you enter this text:
Natural language processing (NLP) is a theorymotivated range of computational techniques for the automatic analysis and representation of human language. NLP research has evolved from the era of punch cards and batch processing (in which the analysis of a sentence could take up to 7 minutes) to the era of Google and the likes of it (in which millions of webpages can be processed in less than a second). This review paper draws on recent developments in NLP research to look at the past, pres- ent, and future of NLP technology in a new light. Borrowing the paradigm of ‘jumping curves’ from the field of business management and marketing prediction, this survey article reinterprets the evolution of NLP research as the intersection of three overlapping curves-namely Syntactics, Semantics, and Pragmatics Curves- which will eventually lead NLP research to evolve into natural language understanding.
!["Entered the snippet"]("https://user-images.githubusercontent.com/41857601/189453936-bfc79847-19ae-45f2-8788-e2fedcf6b2f0.png")
!["Same snippet if you choose to see the complexity of the sentences"]("https://user-images.githubusercontent.com/41857601/189454445-2fa08ce3-c94a-46a4-95c2-af27f9da5352.png")