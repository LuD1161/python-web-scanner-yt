import requests
import time
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue

def worker(input_queue):
    cookies = {
        '_ga_GR4KJ51T5B': 'GS1.1.1651692257.1.0.1651693215.0',
        '_ga': 'GA1.1.327657774.1651692257',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': '_ga_GR4KJ51T5B=GS1.1.1651692257.1.0.1651693215.0; _ga=GA1.1.327657774.1651692257',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    while True:
        url = input_queue.get()
        if url is None:
            break

        print(f"🚀 URL : {url}\n")
        try:
            response = requests.get(url, cookies=cookies, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            headers = response.headers
            print(f"title : {soup.title.string}\n")
        except Exception as e:
            print(f"Exception in getting header : {e}")


def main():
    number_of_workers = 10
    with open("top-100.csv", "r") as f:
        data = f.read()
    urls = data.split("\n")

    input_queue = Queue()
    workers = []

    # Create workers.
    for i in range(number_of_workers):
        p = Process(target=worker, args=(input_queue, ))
        workers.append(p)
        p.start()

    # Distribute work.
    for url in urls:
        url = "https://"+url.split(",")[1]    # ["1", "netflix.com"]
        input_queue.put(url)

    # Ask the workers to quit.
    for w in workers:
        input_queue.put(None)

    # Wait for workers to quit.
    for w in workers:
        w.join()

    print('Done')


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
