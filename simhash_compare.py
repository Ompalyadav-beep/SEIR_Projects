import sys
import requests
from bs4 import BeautifulSoup

def convertUrlToText(url):
    webPage = requests.get(url)
    webPage.raise_for_status()
    soup = BeautifulSoup(webPage.text, "html.parser")
    if soup.body:
        return soup.body.get_text(separator=" ", strip=True)
    else:
        return "No body content found"

def countWord(webPage):
    stopWords={"a","an","the","and","for","with","that","this","you","had"}
    webPage=webPage.lower()
    webPage=webPage.split()
    freqCounter={}
    for word in webPage:
        if word not in stopWords:
            if word in freqCounter :
                freqCounter[word]+=1
            else:
                freqCounter[word]=1
    return freqCounter

def polynomial_hash(word):
    p = 53
    m = 2**64
    hash_value = 0
    power = 1
    for ch in word:
        hash_value = (hash_value + ord(ch) * power) % m
        power = (power * p) % m
    return hash_value

def compute_simhash(freq_dict):
    fingerprint = [0] * 64
    for word, freq in freq_dict.items():
        hashValue = polynomial_hash(word)
        for i in range(64):
            if hashValue & (1 << i):
                fingerprint[i] += freq
            else:
                fingerprint[i] -= freq
    simhash = 0
    for i in range(64):
        if fingerprint[i] > 0:
            simhash |= (1 << i)
    return simhash

def hamming_distance(simhash1,simhash2):
    dis=0
    xor=simhash1^simhash2
    for i in range(64):
        if xor&(1<<i):
            dis+=1
        else:
            None
    return 64 - dis

def main():
    if len(sys.argv) != 3:
        print("Two urls must be entered.")
        sys.exit(1)

    url1 = sys.argv[1]
    url2 = sys.argv[2]

    webPage1=convertUrlToText(url1)
    webPage2=convertUrlToText(url2)
    if webPage1 and webPage2:
        freqDict1=countWord(webPage1)
        freqDict2=countWord(webPage2)

        simhash1 = compute_simhash(freqDict1)
        simhash2 = compute_simhash(freqDict2)

        distance = hamming_distance(simhash1, simhash2)
        common_bits = 64 - distance

        print("wordcounts1: ",freqDict1)
        print("wordcounts2: ",freqDict2)
        print("simhash1",simhash1)
        print("simhash2",simhash2)
        print("hamming distance: ",distance)
        print("Common Bits:", common_bits)
    else:
        print("error to get content")
if __name__ == "__main__":
    main()