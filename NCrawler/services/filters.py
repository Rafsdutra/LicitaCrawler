import spacy


def relevance(sentence):
    nlp = spacy.load('pt')
    main_doc = nlp(sentence)
    search_doc = nlp('arte midia marketing publicidade campanha divulgação')
    main_doc_no_stop_words = nlp(' '.join([str(t) for t in main_doc if not t.is_stop]))
    search_doc_no_stop_words = nlp(' '.join([str(t) for t in search_doc if not t.is_stop]))
    similarity = main_doc_no_stop_words.similarity(search_doc_no_stop_words)
    return similarity
