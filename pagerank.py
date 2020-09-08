import os, random, re, sys
DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit('Usage: python pagerank.py corpus')
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    else:
        ranks = iterate_pagerank(corpus, DAMPING)
        print('PageRank Results from Iteration')
        for page in sorted(ranks):
            print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()
    for filename in os.listdir(directory):
        if not filename.endswith('.html'):
            pass
        else:
            with open(os.path.join(directory, filename)) as (f):
                contents = f.read()
                links = re.findall('<a\\s+(?:[^>]*?)href=\\"([^\\"]*)\\"', contents)
                pages[filename] = set(links) - {filename}
    else:
        for filename in pages:
            pages[filename] = set((link for link in pages[filename] if link in pages))
        else:
            return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    page_probability = round((1 - damping_factor) / len(corpus), 3)
    try:
        link_probability = damping_factor / len(corpus[page]) + page_probability
    except:
        link_probability = page_probability

    model = {}
    model[page] = round(page_probability, 3)

    for link in corpus[page]:
        model[link] = round(link_probability, 3)
    else:
        return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_probability = round((1 - damping_factor), 2)
    pages = list(corpus.keys())

    weights = []
    for i in range(len(corpus)):
        weights.append(page_probability)

    sample = {}
    for p in pages:
        sample[p] = 0

    page = random.choices(pages, weights=weights, k=1)[0]
    sample[page] += 1

    for i in range(SAMPLES):
        model = transition_model(corpus, page, DAMPING)

        model.pop(page)
        for i in model:
            model[i] = round(model[i], 2)
        pages = list(model.keys())

        try:
            page = random.choices(pages, weights=list(model.values()), k=1)[0]
            sample[page] += 1
        except:
            pages = list(corpus.keys())

            weights = []
            for i in range(len(corpus)):
                weights.append(page_probability)

            page = random.choices(pages, weights=weights, k=1)[0]
            sample[page] += 1

    final_sample = {}

    for p in sample:
        final_sample[p] = sample[p]/10000

    return final_sample


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample = {}


    for p in list(corpus.keys()):
        sample[p] = 1/len(corpus)

    first = (1 - damping_factor)/len(corpus)

    while True:
        old_sample = sample.copy()
        for i in list(corpus.keys()):
            PR_NumLinks = 0
            for p in corpus.values():
                if i in p:
                    PR_i = sample[i]
                    NumLinks_i = len(p)
                    PR_NumLinks += PR_i/NumLinks_i

            sample[i] =  first + PR_NumLinks
            if sample[i] - old_sample[i] < .001:
                total = sum(sample.values())

                for page, value in sample.items():
                    sample[page] = value/total
                return sample

    return sample


if __name__ == '__main__':
    main()
