# Web-Search-Engine
Web Search Engine

# **Basic Python Web Search Engine**

This project is a simple web crawler and search engine that:  
- Crawls web pages starting from a seed URL  
- Indexes keywords and corresponding URLs  
- Ranks web pages using a simplified **PageRank** algorithm  
- Allows keyword searches with ranked results  

---

## **How to Use**

### **1. Requirements**
- Python 3.12  

### **2. Run Example**

1. **Crawl a website:**
   ```python
   index, graph = crawl_web("http://example.com")
   ```
   
2. **Search for a keyword:**
   ```python
   results = ranked_look_up(index, "keyword")
   print("Results:", results)
   ```

---

## **Main Functions**

- **`crawl_web(seed)`**: Crawls pages and builds an index of keywords and a link graph.  
- **`ranked_look_up(index, key, graph, compute_ranks)`**: Searches for pages with the keyword and returns ranked results.  

---

## **Troubleshooting**

- **SSL Error:** Disable verification:
  ```python
  import ssl
  context = ssl._create_unverified_context()
  ```

- **Empty Results:**  
  Check if the page has links (`<a href="">`) or uses JavaScript (use `requests-html` for dynamic pages).

---

## **Future Enhancements**   
- Improve keyword-based ranking with frequency analysis.  
