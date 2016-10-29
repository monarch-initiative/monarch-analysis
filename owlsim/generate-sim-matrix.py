import json
import argparse
from monarch import monarch

parser = argparse.ArgumentParser(description='description')
parser.add_argument('--input', '-i', type=str, required=True,
                    help='Location of input file')
parser.add_argument('--similarity', '-sim', type=str, required=True,
                    help='Location of output file')
parser.add_argument('--distance', '-dist', type=str, required=True,
                    help='Location of output file')
parser.add_argument('--temp', '-t', type=str, required=False,
                    help='Location of temp file')
parser.add_argument('--cache', '-c', type=str, required=False,
                    help='Location of cache file')
args = parser.parse_args()

input_file = open(args.input, 'r')
similarity_file = open(args.similarity, 'w')
distance_file = open(args.distance, 'w')
if args.temp:
    temp_file = open(args.temp, 'w')
    temp_file.close()

sample_ids = []

for line in input_file:
    sample_ids.append(line.rstrip('\n'))

if args.cache:
    cached_matrix = open(args.cache, 'r')
    similarity_matrix = json.load(cached_matrix)
    distance_matrix = [[100-k if k != 0 else 0 for k in similarity_matrix[i]] for i in range(len(similarity_matrix))]
else:
    similarity_matrix = [[0 for k in range(len(sample_ids))] for i in range(len(sample_ids))]
    distance_matrix = [[0 for k in range(len(sample_ids))] for i in range(len(sample_ids))]


for index, value in enumerate(sample_ids):
    for index_query, value_query in enumerate(sample_ids):
        if similarity_matrix[index][index_query] is 0 \
                and distance_matrix[index][index_query] is not 100:
            score = monarch.get_score_from_compare(value, value_query)
            try:
                similarity_score = int(score)
                distance_score = 100 - similarity_score
            except ConnectionError:
                similarity_score = 0
                distance_score = 0

            similarity_matrix[index][index_query] = similarity_score
            similarity_matrix[index_query][index] = similarity_score
            distance_matrix[index][index_query] = distance_score
            distance_matrix[index_query][index] = distance_score

    # Dump matrix to temp file every now and then
    if index % 100 == 0:
        if args.temp:
            temp_file = open(args.temp, 'w')
            temp_file.write(json.dumps(similarity_matrix))
            temp_file.close()


similarity_file.write(json.dumps(similarity_matrix))
distance_file.write(json.dumps(distance_matrix))

