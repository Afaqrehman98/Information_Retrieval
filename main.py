import argparse
import shlex
import os
import time

from document_processing import DocumentProcessor


def main():
    # parser = argparse.ArgumentParser(description='Process command.')

    # parser.add_argument('-extract-collection', metavar='filename', help='Extract collection command')
    # parser.add_argument('-model', metavar='value', help='Model option')
    # parser.add_argument('-search-mode', metavar='value', help='Search mode option')
    # parser.add_argument('-documents', metavar='value', help='Documents option')
    # parser.add_argument('-query', metavar='value', help='Query option')

    # args = parser.parse_args()

    # if args.extract_collection:
    #     filename = args.extract_collection
    #     print(f"Processing first -extract-collection {filename}")
    #     processor = DocumentProcessor()
    #     processor.extract_fables_from_text_file(filename)
    # else:
    #     print("Invalid command. Please provide the right -extract-collection command. Which is presented in the "
    #           "directory")

    # while True:
    #     search_query_command = input("Kindly enter the command to search for a document or enter 'exit' to quit: ")
    #     if search_query_command == 'exit':
    #         break

    #     if search_query_command.startswith("python main.py"):
    #         split_command = shlex.split(search_query_command)
    #         second_args = parser.parse_args(split_command[2:])
    #         model_for_search = second_args.model
    #         mode_of_search = second_args.search_mode
    #         folder_to_be_searched = second_args.documents
    #         query_to_be_searched = second_args.query
    #         print(f"Processing search: {search_query_command}")
    #         document_processor = DocumentProcessor()
    #         if model_for_search == 'bool' and mode_of_search == 'linear' and folder_to_be_searched in ['original', 'no_stopwords']:
    #             use_stopwords = True if folder_to_be_searched == 'no_stopwords' else False
    #             document_processor.linear_search_mode(query=query_to_be_searched, use_stopwords=use_stopwords)
    #         else:
    #             print("Invalid parameters. kindly check the document in the directory to make a correct command")

    #     else:
    #         print("Invalid command. kindly check the document in the directory to make a correct command")





    def linear_search_mode(self, query, use_stopwords=False):
        # First we select the folder based on the parameters whether we want to search in collection_no_stopwords or
        # collection_original then get the directory to search for the query later we initialize an empty list to
        # append the items or content that matches then we do the linear search we iterate from every file and find
        # out the query in those files then print those fileNames which contains those query

        if use_stopwords:
            sub_folder = 'collection_no_stopwords'
        else:
            sub_folder = 'collection_original'
        search_directory = os.path.join(self.script_directory, sub_folder)

        files_that_matches_query = []

        for filename in os.listdir(search_directory):
            filepath = os.path.join(search_directory, filename)
            with open(filepath, 'r') as file:
                content = file.read()
                if boolean_query_search(query, content, use_stopwords):
                    files_that_matches_query.append(filename)

        if len(files_that_matches_query) == 0:
            print("No files found")
        else:
            for filename in files_that_matches_query:
                print(filename)


    # Methods For Boolean Retrival Method Starts Here
    
    # Create an inverted index to store the terms and their corresponding document IDs. 
    # Iterate over the text files in the "collection" folder, read the contents of each file, 
    # tokenize the text into terms, and build the inverted index.
    def inverted_index(folder_path):
        inverted_index = {}
        inverted_index["_all_documents"] = {}  # Add _all_documents entry
        
        for filename in os.listdir(folder_path):
            # print("filname",filename)
            file_path = os.path.join(folder_path, filename)
            # print("file_path",file_path)
            with open(file_path, 'r') as file:
                document = file.read()
                # print("document",document)
                terms = document.split()  # Split text into terms
                # print("term",terms)

                for term in terms:
                    if term not in inverted_index:
                        inverted_index[term] = {}
                    if filename not in inverted_index[term]:
                        inverted_index[term][filename] = 0
                    inverted_index[term][filename] += 1

                  # Add the document name to the _all_documents entry
                inverted_index["_all_documents"][filename] = len(terms)  # Store the document length

        return inverted_index
    
    

    # Implement functions to process Boolean queries and retrieve the relevant documents 
    # based on the inverted index
    # AND Logic
    def boolean_and(terms, inverted_index):
        if len(terms) == 0:
            return set()

        terms.remove("&")    
        terms = [term.lower() for term in terms]  # Convert terms to lowercase
    
        result = set(inverted_index.get(terms[0], {}).keys())

        for term in terms[1:]:
            result = result.intersection(inverted_index.get(term, {}).keys())

        return result
    
    # OR Logic
    def boolean_or(terms, inverted_index):
        if len(terms) == 0:
            return set()
        
        terms.remove("|")    
        terms = [term.lower() for term in terms]  # Convert terms to lowercase
        
        result = set()

        for term in terms:
            result = result.union(inverted_index.get(term, {}).keys()) 

        return result
    # NOT Logic
    def boolean_not(term, inverted_index, total_documents):
        if len(term) == 0:
            return set()
        
        term = term.lower()

        term_documents = set(inverted_index.get(term, {}).keys())
        all_documents = set(inverted_index["_all_documents"].keys())  # All document names

        result = all_documents - term_documents

        sorted_result = sorted(result, key=lambda x: int(x[:2]))  # Sort filenames based on first two digits

        return sorted_result

   
    def split_string_by_operators(string, operators):
        split_list = []
        current_word = ""

        for char in string:
            if char in operators:
                if current_word:
                    split_list.append(current_word)
                    current_word = ""
                split_list.append(char)
            else:
                current_word += char

        if current_word:
            split_list.append(current_word)

        return split_list

   # input Boolean queries and display the relevant documents.
    def search_documents(query, inverted_index, total_documents):
        
        start_time = time.time()
        
        operators = ["&","|","-"]
        terms = split_string_by_operators(query, operators)
        
        if '&' in terms:
            result = boolean_and(terms, inverted_index)
        elif '|' in terms:
            result = boolean_or(terms, inverted_index)
        elif '-' in terms:
            result = boolean_not(terms[1], inverted_index, total_documents)
        else:
            result = inverted_index.get(terms[0], set())
        
        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds and round to 2 decimal places

        results = [result]

        # Append the query processing time to the results list
        results.append(f"T=<{elapsed_time}>ms")

        return results

    # This is the main function 
    # def boolean_retrieval_mode(self, query, use_stopwords=False):

   
    sub_folder = 'collection_no_stopwords'

    inverted_index = inverted_index(sub_folder)
    total_documents = len(os.listdir(sub_folder))

    query = input("Enter a Boolean query: ")

    result = search_documents(query, inverted_index, total_documents)

    print("Relevant Documents:")
    for doc_id in result:
        print(doc_id)

if __name__ == '__main__':
    main()