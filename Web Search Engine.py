# Function to get the next URL link from a page's content
def get_next_target(page):
    start_link = page.find('<a href=')  # Find the position of the hyperlink
    if start_link == -1:  # No link found
        return None, 0  # Return None and position 0
    start_quote = page.find('"', start_link)  # Find the start of the URL in quotes
    end_quote = page.find('"', start_quote + 1)  # Find the end of the URL
    url = page[start_quote + 1:end_quote]  # Extract the URL between quotes
    return url, end_quote  # Return the URL and position of the end quote

# Function to fetch the content of a web page given its URL
def get_page(url):
    try:
        import urllib.request  # Import library for HTTP requests
        page = urllib.request.urlopen(url).read()  # Read page content
        return page.decode("utf-8")  # Decode to string
    except:  # Handle errors such as 404 or no connection
        return ""

# Function to merge two lists, adding elements from `q` into `p` if they are not already present
def union(p, q):
    for e in q:
        if e not in p:
            p.append(e)

# Function to add a keyword and associated URL to the search index
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)  # Append the URL if keyword already exists
    else:
        index[keyword] = [url]  # Create new entry if keyword doesn't exist

# Function to add all words on a page to the index
def add_page_to_index(index, url, content):
    words = content.split()  # Split content into individual words
    for word in words:
        add_to_index(index, word, url)  # Add each word with the URL to the index

# Function to extract all links from a page's content
def get_all_links(page):
    links = []  # Initialize an empty list for links
    while True:
        url, endpos = get_next_target(page)  # Get the next URL
        if url:  # If a URL is found
            links.append(url)  # Add it to the list
            page = page[endpos:]  # Move past this link in the page
        else:  # No more links found
            break
    return links  # Return the list of links

# Function to remove HTML tags from content and clean the text
def clean_html(content):
    cleaned_content = ""  # Initialize cleaned content string
    htmls = content.split('>')  # Split by '>' to separate HTML tags and text
    for i in htmls:
        if '<' in i:  # If there's a tag within the text
            cleaned_content += i.split('<')[0]  # Add only the text before the '<'
        else:
            cleaned_content += i  # Add the full text if no '<' is found
    return cleaned_content

# Function to crawl the web starting from a seed URL and build an index and a graph of pages
def crawl_web(seed):
    to_crawl = [seed]  # List of URLs to crawl
    crawled = []  # List of already crawled URLs
    index = {}  # Dictionary to store keywords and associated URLs
    graph = {}  # Dictionary to store the relationship between pages (links)

    while to_crawl:
        page = to_crawl.pop()  # Remove the last URL from to_crawl list
        if page not in crawled:  # Only crawl if the page hasn't been crawled
            content = get_page(page)  # Fetch page content
            cleaned_content = clean_html(content)  # Clean content from HTML tags
            add_page_to_index(index, page, cleaned_content)  # Add content to index
            outlinks = get_all_links(content)  # Extract links from the page
            graph[page] = outlinks  # Store links in the graph
            union(to_crawl, outlinks)  # Add new links to the crawl list
            crawled.append(page)  # Mark the page as crawled

    return index, graph  # Return the index and graph

# Function to compute page ranks using a simplified PageRank algorithm
def compute_ranks(graph):
    d = 0.8  # Damping factor (probability of following a link)
    N = len(graph)  # Number of pages in the graph
    numloops = 10  # Number of iterations to refine ranks
    ranks = {}  # Dictionary to store ranks of pages

    for page in graph:  # Initialize rank of each page to 1/N
        ranks[page] = 1 / N

    for i in range(numloops):  # Perform rank computation
        newranks = {}  # Dictionary for new ranks
        for page in graph:
            newrank = (1 - d) / N  # Base rank (for pages with no in-links)
            for element in graph:  # Sum contributions from in-links
                if page in graph[element]:
                    newrank += d * (ranks[element] / len(graph[element]))  # Weighted contribution
            newranks[page] = newrank  # Store the new rank
        ranks = newranks  # Update ranks

    return ranks  # Return the final ranks

# Function to perform a ranked lookup of pages for a keyword
def ranked_look_up(index, key, graph):
    result_dict = {}  # Dictionary to store pages and their ranks
    results = []  # List of pages sorted by rank
    all_ranks = compute_ranks(graph)  # Compute ranks of pages

    if key in index:  # If the keyword exists in the index
        for page in index[key]:
            key_rank = all_ranks[page]  # Get the rank of the page
            if page not in result_dict:
                result_dict[page] = key_rank  # Add page and rank to the dictionary

    # Sort pages by their rank in descending order
    sorted_results = sorted(result_dict.items(), key=lambda item: item[1], reverse=True)

    for page, key_rank in sorted_results:
        results.append(page)  # Append sorted pages to the results

    return results  # Return the sorted pages

# Function to look up pages for a keyword with optional ranking
def look_up(index, key, graph=None, computing_procedure=None):
    if graph is None and computing_procedure is None:  # Simple lookup without ranking
        if key in index:
            return index[key]  # Return the URLs for the keyword
        else:
            return None
    elif graph is not None and computing_procedure is not None:  # Lookup with ranking
        all_ranks = computing_procedure(graph)  # Compute ranks
        result_dict = {}
        results = []
        if key in index:
            for page in index[key]:
                key_rank = all_ranks[page]  # Get rank of the page
                if page not in result_dict:
                    result_dict[page] = key_rank

        sorted_results = sorted(result_dict.items(), key=lambda item: item[1], reverse=True)

        for page, key_rank in sorted_results:
            results.append(page)

        return results  # Return ranked results
    else:
        print("INVALID INPUT COMBINATION: Please check the inputs.")  # Invalid combination


#test case
index1, graph1 = crawl_web("http://searchengineplaces.com.tr")

print(index1)

print(graph1)
