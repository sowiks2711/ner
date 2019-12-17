import numpy as np
def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return distance[row][col]

def generate_dict_doc_name(input_filename):
    results_grouped_by = dict()
    with open(input_filename, encoding='utf-8') as f:
        for line in f.readlines():
            clean_line = line.strip()
            split_line = clean_line.split(';')
            if len(split_line) != 2:
                continue
            name = split_line[0].lower()
            doc = split_line[1]
            if doc not in results_grouped_by:
                results_grouped_by[doc] = dict()
            if name not in results_grouped_by[doc]:
                results_grouped_by[doc][name] = 1
            else:
                results_grouped_by[doc][name] += 1
    return results_grouped_by


def generate_dict_corpus_name(input_filename):
    results_corpus = dict()
    with open(input_filename, encoding='utf-8') as f:
        for line in f.readlines():
            clean_line = line.strip()
            split_line = clean_line.split(';')
            if len(split_line) != 2:
                continue
            name = split_line[0].lower()
            if name not in results_corpus:
                results_corpus[name] = 1
            else:
                results_corpus[name] += 1
    return results_corpus


our_results_doc = generate_dict_doc_name('./our_result.csv')
their_results_doc = generate_dict_doc_name('./their_result.csv')
our_results_corpus = generate_dict_corpus_name('./our_result.csv')
their_results_corpus = generate_dict_corpus_name('./their_result.csv')

# ile otagowało rzeczy
print(f"Liczba znalezionych tagów w naszym rozwiązaniu -> {sum([our_results_corpus[x] for x in list(our_results_corpus.keys())])}")
print(f"Liczba znalezionych tagów w ich rozwiązaniu -> {sum([their_results_corpus[x] for x in list(their_results_corpus.keys())])}")

# ile znalezionych encji
print(f"Liczba znalezionych unikatowych encji w naszym rozwiązaniu -> {len(our_results_corpus)}")
print(f"Liczba znalezionych unikatowych encji w ich rozwiązaniu -> {len(their_results_corpus)}")

# ile znalezionych niepojedynczych encji
print(f"Liczba znalezionych unikatowych niepojedynczych encji w naszym rozwiązaniu -> {len([x for x in our_results_corpus if our_results_corpus[x]>2])}")
print(f"Liczba znalezionych unikatowych niepojedynczych encji w ich rozwiązaniu -> {len([x for x in their_results_corpus if their_results_corpus[x]>2])}")

# ile pokrywających się encji
similar_results_corpus = set(list(our_results_corpus.keys()) + list(their_results_corpus.keys()))
print(f"Liczba pokrywających się encji -> {len(their_results_corpus) + len(our_results_corpus) - len(similar_results_corpus)}")
# przykłady encji znalezionych przez 1 skrypt a nie przez drugi
our_unique_results = [x for x in list(our_results_corpus.keys())  if x not in list(their_results_corpus.keys())]
their_unique_results = [x for x in list(their_results_corpus.keys()) if x not in list(our_results_corpus.keys())]

#print(f"Nasze unikatowe encje: {",".join(our_unique_results[:5:30])}")
# przykłady dokumentów zawierających ich unikatowe encje (występujące tylko u nich)
example_docs = []
for doc in their_results_doc:
    their_entities = their_results_doc[doc]
    their_entities_keys = list(their_entities.keys())
    found_unique_result_set = set(their_entities_keys) & set(their_unique_results)
    if len(found_unique_result_set) != 0:
        example_docs.append((doc, found_unique_result_set))
print(f"example_docs => {example_docs[:30]}")
# ile pokrywających się dokumentów względem encji
print(f"liczba naszych dokumentów -> {len(our_results_doc)}")
print(f"liczba ich dokumentów -> {len(their_results_doc)}")

identical_docs = []
for doc in our_results_doc:
    if doc in their_results_doc:
        our_entities = our_results_doc[doc]
        their_entities = their_results_doc[doc]
        matched = len(our_entities) == len(their_entities)
        if matched:
            for person in our_entities:
                if person not in their_entities:
                    matched = False
                    break
        if matched:
            identical_docs.append(doc)
print(f"liczba identycznych dokumentów -> {len(identical_docs)}")
# kilka konkretnych przykładów nieścisłości (pierwsze 3 wypisz)

# ile pokrywających się dokumentów względem liczby encji
identical_docs = []
for doc in our_results_doc:
    if doc in their_results_doc:
        our_entities = our_results_doc[doc]
        their_entities = their_results_doc[doc]
        matched = (sum([our_entities[x] for x in our_entities])) == (sum([their_entities[x] for x in their_entities]))

        if matched:
            identical_docs.append(doc)
print(f"liczba identycznych dokumentów względem liczby encji-> {len(identical_docs)}")
# ile pokrywających się dokumentów względem kolmogorov(encji,1)
identical_docs = []
for doc in our_results_doc:
    if doc in their_results_doc:
        our_entities = our_results_doc[doc]
        their_entities = their_results_doc[doc]
        matched = True
        for our_entity in their_entities:
            found_levenstein = False
            for their_entity in our_entities:
                if levenshtein_ratio_and_distance(our_entity,their_entity) < 3:
                    #if( our_entity != their_entity):
                        #print(f"{our_entity} ;;; {their_entity}")
                    found_levenstein = True
                    
            
            if not found_levenstein:
                matched = False
                break
        if matched:
            identical_docs.append(doc)
    
print(f"liczba identycznych dokumentów względem liczby encji-> {len(identical_docs)}")