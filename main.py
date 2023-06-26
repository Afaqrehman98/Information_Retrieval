import argparse
import os
import shlex

from document_processing import DocumentProcessor
from boolean_search import BooleanSearch


def main():
    parser = argparse.ArgumentParser(description='Process command.')

    parser.add_argument('-extract-collection', metavar='filename', help='Extract collection command')
    parser.add_argument('-model', metavar='value', help='Model option')
    parser.add_argument('-search-mode', metavar='value', help='Search mode option')
    parser.add_argument('-documents', metavar='value', help='Documents option')
    parser.add_argument('-stemming', metavar='value', help='Stemming option')
    parser.add_argument('-query', metavar='value', help='Query option')

    args = parser.parse_args()

    if args.extract_collection:
        filename = args.extract_collection
        print(f"Processing first -extract-collection {filename}")
        processor = DocumentProcessor()
        processor.extract_fables_from_text_file(filename)
    else:
        print("Invalid command. Please provide the right -extract-collection command. Which is presented in the "
              "directory")

    while True:
        search_query_command = input("Kindly enter the command to search for a document or enter 'exit' to quit: ")
        if search_query_command == 'exit':
            break

    if search_query_command.startswith("python main.py"):
        split_command = shlex.split(search_query_command)
        second_args = parser.parse_args(split_command[2:])
        model_for_search = second_args.model
        mode_of_search = second_args.search_mode
        folder_to_be_searched = second_args.documents
        stemming = second_args.stemming
        query_to_be_searched = second_args.query
        print(f"Processing search: {search_query_command}")
        document_processor = DocumentProcessor()
        if model_for_search == 'bool' and mode_of_search == 'linear' and folder_to_be_searched in ['original',
                                                                                                   'no_stopwords']:
            use_stopwords = True if folder_to_be_searched == 'no_stopwords' else False
            if stemming is None or not stemming:
                use_stemming = False
            else:
                use_stemming = True

            document_processor.linear_search_mode(query=query_to_be_searched, use_stopwords=use_stopwords,
                                                  use_stemming=use_stemming)
        elif model_for_search == 'bool' and mode_of_search == 'inverted' and folder_to_be_searched in ['original',
                                                                                                       'no_stopwords']:
            use_stopwords = True if folder_to_be_searched == 'no_stopwords' else False
            if stemming is None or not stemming:
                use_stemming = False
            else:
                use_stemming = True

            boolean_search = BooleanSearch
            invertedIndex = boolean_search.inverted_index(folder_to_be_searched)
            total_documents = len(os.listdir(folder_to_be_searched))
            boolean_search.search_documents(query=query_to_be_searched, inverted_index=invertedIndex,
                                            total_documents=total_documents)
        else:
            print("Invalid parameters. kindly check the document in the directory to make a correct command")

    else:
        print("Invalid command. kindly check the document in the directory to make a correct command")

    # This is the main function 
    # def boolean_retrieval_mode(self, query, use_stopwords=False):

    # sub_folder = 'collection_no_stopwords'
    #
    # inverted_index = inverted_index(sub_folder)
    # total_documents = len(os.listdir(sub_folder))
    #
    # query = input("Enter a Boolean query: ")
    #
    # result = search_documents(query, inverted_index, total_documents)
    #
    # print("Relevant Documents:")
    # for doc_id in result:
    #     print(doc_id)


if __name__ == '__main__':
    main()
