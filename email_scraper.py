def run_email_scraper():

    from bs4 import BeautifulSoup
    import requests  # used for aking the http request to the web pages
    import requests.exceptions  # handles connection errors like timout invalid url...
    import urllib.parse  # helps to break down the url into parts ike  domain path...
    from collections import (
        deque,
    )  # double ended queue for fast add/remove from both sides
    import re  # for regular expression, used here for finding emails in text

    user_url = str(input("[+] Enter Target URL To Scan: "))
    urls = deque([user_url])

    scraped_urls = set()  # keep track of urls already visited so we dont repeat
    emails = set()  # stores found email , no duplicates

    count = 0  # used for keeping the track of how mmany have been processed

    def new_func(response):  # EXTRACT FUNCTION
        return re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I
        )  # regex pattern

    # re.findall -finds all text that matches the pattern,
    # re.I - it makes all the regex case insensitive

    try:
        while len(urls):
            count += 1
            if count == 30:
                break
            url = (
                urls.popleft()
            )  # takes next url form the queue, popleft rm form the front
            scraped_urls.add(url)  # marks it as already visited

            parts = urllib.parse.urlsplit(url)
            # bcuz of some relative urls(just a piece ,missing the domain-Example: "https://example.com/about/index.html")
            # scheme - http / https ,netloc - domain/gmail.com
            # path -/about/index.html
            base_url = "{0.scheme}://{0.netloc}".format(
                parts
            )  # 0 refers to the first argument passed into .format() like =={0.scheme}.format(parts) -https .,,,,{0.netloc}".format(parts) - example.com

            path = (
                url[: url.rfind("/") + 1] if "/" in parts.path else url
            )  # Finds everything before the last '/'

            print("[%d] Processing %s" % (count, url))  # which page is worked on
            try:
                response = requests.get(url)  # downloads the html page
            except requests.exceptions.RequestException:
                continue
            new_emails = set(new_func(response))  # finds all emails in the page
            emails.update(new_emails)  # add that emial to the global list

            soup = BeautifulSoup(response.text, features="lxml")

            for anchor in soup.find_all("a"):
                link = anchor.attrs["href"] if "href" in anchor.attrs else ""
                if link.startswith("/"):
                    link = base_url + link
                elif not link.startswith("http"):
                    link = path + link
                if link not in urls and link not in scraped_urls:
                    urls.append(link)
    except KeyboardInterrupt:
        print("[-] Closing!")

    for mail in emails:
        print(mail)
