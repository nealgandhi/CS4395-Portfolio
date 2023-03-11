from urllib import request
from urllib.request import Request
from bs4 import BeautifulSoup
import nltk
from nltk import sent_tokenize
from nltk.corpus import stopwords
import pickle
# function to loop through urls
def urlgen():
    list = []
    # news articles from Wildlife Conservation Society
    url = 'https://newsroom.wcs.org/'
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, features="html.parser")
    counter = 0
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if counter >= 15:
            break
        # filter only relevant links from url source
        if ('articleId' in link_str or link_str.startswith('https://')) and 'pbs' not in link_str \
                and 'medium' not in link_str and 'bbc' not in link_str and 'youtube' not in link_str \
                and 'library' not in link_str and 'twitter' not in link_str and link_str not in list:
            counter += 1
            list.append(link_str)
    return list
# function to scrape text off page and store in file
def webscrape(link):
    f_name = ''.join(link.split('.')[1:3])
    f_name = f_name.split('/')
    f_name = '_'.join(f_name)
    f_name = f_name + ".txt"
    try:
        with open(f_name, 'w+') as f:
            req = Request(
                url=link,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            html = request.urlopen(req).read().decode('utf8')
            soup = BeautifulSoup(html, features='html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            sents = sent_tokenize(text)
            for sent in sents:
                f.write(sent)
        preprocess(f_name, 25)
    except:
        print('')
# function to extract important terms from pages using term frequency or tf
def preprocess(file_name, num_terms):
    tf_dict = {}
    file_content = open(file_name).read()
    tokens = nltk.word_tokenize(file_content)
    tokens = [t.lower() for t in tokens if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]
    # get term frequencies
    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1
    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)
    # print 40 most frequent words in document
    sorted_terms = sorted(tf_dict.items(), reverse=True, key=lambda x: x[1])
    top_forty = sorted_terms[0:40]
    forty_list = [x[0] for x in top_forty]
    print(forty_list)
# start
url_list = urlgen()
for url in url_list:
    webscrape(url)
# knowledge base - consists of facts relating to key terms (source: https://www.wcs.org/)
kb = {'wildlife': ['The Wildlife Conservation Society mission is to save wildlife and wild places through science, '
                   'conservation action, and inspiring people to value nature'],
      'conservation': ['WCS has established long-term conservation presence in the last wild places across the '
                       'Americas, Africa, Asia, and Oceania.', 'We engage in a broad array of conservation science and '
                                                               'policy interventions to enable our conservation '
                                                               'solutions', 'We are dedicated to building leadership '
                                                                            'capacity for wildlife conservation on a '
                                                                            'global scale by providing support and '
                                                                            'mentoring to the best and the brightest '
                                                                            'young conservationists to become the '
                                                                            'conservation leaders of tomorrow.'],
      'climate change': ['We apply our science to discover how best to limit the impacts of climate change on '
                         'ecosystems, wildlife, and people, increasing resilience and providing insurance against a '
                         'rapidly changing world.', 'We are protecting large swaths of tropical and boreal forest that '
                                                    'sequester carbon through our work to protect intact forests and a '
                                                    'mechanism called REDD+.', 'We are helping to restore degraded '
                                                                               'forest lands in areas of high '
                                                                               'conservation significance and where '
                                                                               'this can bring benefits to local '
                                                                               'people.', 'We partner with local '
                                                                                          'communities and governments '
                                                                                          'to find science-based '
                                                                                          'solutions for adapting to '
                                                                                          'the immediate and projected '
                                                                                          'impacts of climate change.'],
      'biodiversity': ['Our Global Priority Species include: African Elephants, Asian Elephants, Bison, Bonobos, '
                       'Cheetahs, Chimpanzees, Coastal Dolphins, Condors, Coral, Flamingos, Turtles & Tortoises, '
                       'Gibbons, Gorillas, Jaguars, Lions, Vultures, Orangutans, Sharks, Snow Leopards, Tigers, '
                       'and Whales!'],
      'ecosystem': ['We are protecting regions that are biologically outstanding and where the long-term conservation '
                    'of species and ecological processes is viable.', 'We have 14 Priority regions including the '
                                                                      'Amazon Rainforest, North American Boreal '
                                                                      'Forests, Sudano-Sahel, and Melanesia to name a '
                                                                      'few!'],
      'planet': ['Our goal is to conserve the world\'s largest wild places in 14 priority regions, home to more than '
                 '50% of the planet\'s biodiversity.', 'Less than a quarter of the planet remains wild. Nature is '
                                                       'sending us a message. Are we listening? Can we find better, '
                                                       'smarter ways to protect our planet’s wildlife and wild '
                                                       'place—and ourselves? How can we be part of the solutions that '
                                                       'the world needs?'],
      'government': ['We assist governments and communities to protect the natural systems critical to saving wildlife '
                     'and wild places, securing valuable flows of ecosystems services and local livelihoods based on '
                     'principles of social and environmental sustainability.', 'We contribute our scientific, '
                                                                               'technical, and policy expertise to '
                                                                               'international discussions between '
                                                                               'governments and to influence '
                                                                               'international policies and commitments '
                                                                               'that will benefit wildlife and wild '
                                                                               'places.'],
      'community': ['We partner with indigenous and local people in achieving their vision for a more secure and '
                    'resilient future, where wildlife remains a visible and culturally valued part of the wild places '
                    'where they live.'],
      'health': ['We use our global health expertise to investigate and combat diseases that move between people, '
                 'domestic animals, and wildlife, and threaten the health of all.'],
      'science': ['WCS uses science to discover and understand the natural world. ', 'WCS scientists study what '
                                                                                     'wildlife species need to thrive. '
                                                                                     'With this knowledge we invest in '
                                                                                     'abating threats to wildlife '
                                                                                     'within their most important '
                                                                                     'strongholds and the corridors '
                                                                                     'that connect them.',
                  'Science helps us discover and understand the natural world.']}
# pickle knowledge base
with open('wcs.pkl', 'wb') as f:
    pickle.dump(kb, f)
# Manually Determined Top 10 Terms (in no particular order)
# wildlife
# conservation
# climate change
# biodiversity (animals, plants, endangered species)
# ecosystem
# planet
# government (international conservation affairs/news)
# community
# health
# science