# dataset-translator
The console app that translate huggingface dataset with translate api or llm


## Usage
```bash
$ transdata --engine [ENGINE] {ENGINE OPTIONS} [HF DATASET PATH] --jq [TARGET to TRANSLATE]
```


## RoadMap

- [x] `2024-07-24` start 
- [x] `2024-07-25` support DeepL API (free)
- [x] `2024-07-28` support LLM translate(use my lite-llm-client)
- [ ] add interface for translate engine(deepl, llm, etc)
- [ ] support DeepL API (pro)
- [ ] support Google Translate
- [ ] implement CLI
- [ ] replace datasets