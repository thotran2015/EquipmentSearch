# import the 17 websites
import threading
import util

from scraping import dotmed, ebay, biosurplus, daigger, labcommerce, labx, google, equipnet, eurekaspot, \
    marshallscientific, medwow, newlifescientific, sibgene, used_line, sci_bay

import math
import time

USED_FUNCS = [equipnet.extract_results,
              labx.extract_results,
              ebay.extract_results,
              #dotmed.extract_results,
              google.extract_results,
              # biosurplus.extract_results,
              medwow.extract_results,
              #labcommerce.extract_results,
              marshallscientific.extract_results,
              #newlifescientific.extract_results,
              #eurekaspot.extract_results,
              sci_bay.extract_results,
              sibgene.extract_results,
              used_line.extract_results]
#
# TODO include coleparmer
# NEW_FUNCS=[daigger.extract_results, \
##ika.extract_results, \
# dotmed.extract_results, \
# ebay.extract_results, \
# google.extract_results, \
# labx.extract_results, \
# medwow.extract_results, \
# sibgene.extract_results
##coleparmer.extract_results
# ]

# NEW_FUNCS=[daigger.extract_results, \
# dotmed.extract_results, \
# ebay.extract_results, \
# google.extract_results, \
# labx.extract_results, \
# medwow.extract_results, \
# sibgene.extract_results
# ]
NEW_FUNCS = [daigger.extract_results, dotmed.extract_results]
USED_WEBSITES = {"equipnet", "labx", "ebay", "dotmed", "google", "biosurplus", "medwow", "labcommerce",
                 "marshallscientific", "newlifescientific", "eurekaspot", "sci_bay", "sibgene", "used_line"}
NEW_WEBSITES = {"daigger", "ika", "dotmed", "ebay", "google", "labx", "medwow", "ibgene", "coleparmer"}

WEBSITES = {"ebay": ebay.extract_results,
            "equipnet": equipnet.extract_results,
            "google": google.extract_results,
            "used line": used_line.extract_results,
            # "eurekaspot": eurekaspot.extract_results,
            # "labcommerce": labcommerce.extract_results,
            # "newlifescientific": newlifescientific.extract_results,
            # "biosurplus": biosurplus.extract_results,
            "sci_bay": sci_bay.extract_results,
            # "dotmed": dotmed.extract_results,
            "sibgene": sibgene.extract_results,
            # "labx": labx.extract_results,
            "medwow": medwow.extract_results,
            "marshallscientific": marshallscientific.extract_results,
            "daigger": daigger.extract_results
            }

MATCH_RATIO = .8

MAX_RESULTS = 10

MIN_RESULTS = 3


def search(website, search_term, condition):
    func = WEBSITES.get(website)
    results = []
    error_message = ""
    try:
        site_results = func(search_term, condition)
        for website_result in site_results:
            if util.is_close_match(search_term, website_result.title):
                results.append(website_result)
            if len(results) >= MAX_RESULTS:
                return error_message, results
    except Exception as e:
        error_message = f"Error scraping {website}: {e}"
        print(error_message)
    finally:
        return error_message, results


def search_a_website(website, search_term, results, lock, stop_event, condition='used') -> (bool, str):
    """
    searches a website until MAX_RESULTS close results are found
    @param website: string,
    @param search_term: string,
    @param results: list,
    @param lock: Threading.Lock,
    @param stop_event: threading event for exiting threads gracefully,
    @param condition: string ("new" or "used")
    returns website_number_valid (boolean), message (string), results (list of Results)
    """
    error_message = ""
    if condition == 'used' and website not in USED_WEBSITES:
        return False, "This site does not sell used equipment"
    if condition == 'new' and website not in NEW_WEBSITES:
        return False, "This site does not sell new equipment"

    func = WEBSITES.get(website)
    if func is None:
        return False, f"No scraping func for this site {website}"
    try:
        print("scraping ", website)
        website_results = func(search_term, condition)
        for website_result in website_results:
            # Check if stop event is set
            if stop_event.is_set():
                return True, error_message
            if util.is_close_match(search_term, website_result.title):
                # Acquire lock to safely update the results dictionary
                lock.acquire()
                results.append(website_result)
                lock.release()
            if len(results) >= MAX_RESULTS:
                stop_event.set()
                return True, error_message
    except Exception as e:
        error_message = f"Error scraping {website}: {e}"
        print(error_message)
    finally:
        return True, error_message


def main():
    lock = threading.Lock()
    stop_event = threading.Event()
    threads = []
    results = []
    start = time.time()
    keywords = "vacuum"
    condition = 'used'
    for website in USED_WEBSITES:
        thread = threading.Thread(target=search_a_website, args=(website, keywords, results, lock, stop_event, condition))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete or until stop condition is met
    for t in threads:
        t.join()  # Wait for this thread to terminate
        if len(results) >= MAX_RESULTS:
            break

    print("Time elapsed: ", time.time()-start)
    print("Results: ", results)


if __name__ == "__main__":
    main()
