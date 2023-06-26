def load_ground_truth(ground_truth_file):
    ground_truth = {}
    with open(ground_truth_file, 'r') as gt_file:
        lines = gt_file.readlines()
        for line in lines:
            term, doc_ids = line.strip().split(' - ')
            doc_ids = [int(doc_id) for doc_id in doc_ids.split(',')]
            ground_truth[term] = doc_ids
    return ground_truth


class PrecisionRecallCalculator:
    def __init__(self, ground_truth_file):
        self.ground_truth = load_ground_truth(ground_truth_file)

    def calculate_precision_recall(self, query, retrieved_docs):
        relevant_docs = set(self.ground_truth.get(query, []))
        retrieved_docs_set = set(retrieved_docs)

        if len(retrieved_docs_set) == 0:
            precision = 0
        else:
            precision = len(retrieved_docs_set.intersection(relevant_docs)) / len(retrieved_docs_set)

        if len(relevant_docs) == 0:
            recall = 0
        else:
            recall = len(retrieved_docs_set.intersection(relevant_docs)) / len(relevant_docs)

        return precision, recall
