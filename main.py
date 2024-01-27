import json
import pickle

from Index.Indexer import Indexer
from Preprocess.Document_Tokenizer import Document_Tokenizer
from Preprocess.General_Tokenizer import General_Tokenizer
from Tf_Idf.Tf_Idf_Maker import Tf_Idf_Maker
from Tf_Idf.Tf_Idf_Ranker import Tf_Idf_Ranker

load_positional_indexes_info = True
save_positional_indexes_info = True
load_tf_idf_info = True
save_tf_idf_info = True
K = 10
deleted_most_frequent_count = 50


def load_positions_files():
    with open('Files/frequencies.pkl', 'rb') as reader:
        frequency_info = pickle.load(reader)
        reader.close()
    with open('Files/positions.pkl', 'rb') as reader:
        positions_info = pickle.load(reader)
        reader.close()
    with open('Files/positional_index.pkl', 'rb') as reader:
        positional_index_info = pickle.load(reader)
        reader.close()
    return frequency_info, positions_info, positional_index_info


def save_positions_files(frequency_info, positions_info, positional_index_info):
    with open('Files/frequencies.pkl', 'wb') as writer:
        pickle.dump(frequency_info, writer)
        writer.flush()
        writer.close()
    with open('Files/positions.pkl', 'wb') as writer:
        pickle.dump(positions_info, writer)
        writer.flush()
        writer.close()
    with open('Files/positional_index.pkl', 'wb') as writer:
        pickle.dump(positional_index_info, writer)
        writer.flush()
        writer.close()


def load_tf_idf_files():
    with open('Files/tf_idf.pkl', 'rb') as reader:
        tf_idf = pickle.load(reader)
        reader.close()
    with open('Files/idf.pkl', 'rb') as reader:
        idf = pickle.load(reader)
        reader.close()
    with open('Files/champions.pkl', 'rb') as reader:
        champions_list = pickle.load(reader)
        reader.close()
    return tf_idf, idf, champions_list


def save_tf_idf_files(tf_idf, idf, champions_list):
    with open('Files/tf_idf.pkl', 'wb') as writer:
        pickle.dump(tf_idf, writer)
        writer.flush()
        writer.close()
    with open('Files/idf.pkl', 'wb') as writer:
        pickle.dump(idf, writer)
        writer.flush()
        writer.close()
    with open('Files/champions.pkl', 'wb') as writer:
        pickle.dump(champions_list, writer)
        writer.flush()
        writer.close()


if __name__ == '__main__':
    query_tokenizer = General_Tokenizer()
    news = {}

    if load_positional_indexes_info:
        with open('IR_data_news_12k.json') as json_file:
            json_datas = json.load(json_file)
            json_file.close()
        json_data = None
        id = None
        for index in range(len(json_datas)):
            json_data = json_datas[str(index)]
            id = int(json_data['url'].split('/')[4])
            news[id] = json_data
        json_datas = None
        frequencies, positions, positional_index = load_positions_files()
        stop_words = dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True)[:deleted_most_frequent_count])

    else:
        document_tokenizer = Document_Tokenizer(50)

        with open('IR_data_news_12k.json') as json_file:
            json_datas = json.load(json_file)
            json_file.close()
        json_data = None
        title = None
        text = None
        url = None
        id = None
        for index in range(len(json_datas)):
            json_data = json_datas[str(index)]
            title = json_data['title']
            text = json_data['content']
            url = json_data['url']
            id = int(url.split('/')[4])
            print(json_data)
            news[id] = json_data
            document_tokenizer.start(text, id)
        json_datas = None

        positions, frequencies, stop_words = document_tokenizer.wait()
        print('Tokenizer finished its work and now indexer start its work')

        indexer = Indexer(positions, stop_words, frequencies)
        positional_index = indexer.start()
        print('Indexer finished its work and now tf_idf maker start its work')
        if save_positional_indexes_info:
            save_positions_files(frequencies, positions, positional_index)

    if load_tf_idf_info:
        tf_idf_result, words_idf, champions = load_tf_idf_files()
    else:
        documents_tf_idf = Tf_Idf_Maker(positional_index, positions)
        documents_tf_idf.start()
        tf_idf_result, words_idf, champions = documents_tf_idf.wait()
        print('tf_idf maker finished its work')
        if save_tf_idf_info:
            save_tf_idf_files(tf_idf_result, words_idf, champions)

    ranker = Tf_Idf_Ranker(tf_idf_result, words_idf, positions, champions)

    while True:
        print('Query : ')
        query = str(input())
        if query == '#EXIT':
            break
        query_tokens = query_tokenizer.process(query)
        ranker.search(query_tokens)
        results = ranker.wait()
        sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True)[:K])
        for news_id in sorted_results.keys():
            print(f'title : {news.get(news_id).get("title")}')
            print(f'link : {news.get(news_id).get("url")}')
            print()
        print()
    print('GOODBYE :)')
