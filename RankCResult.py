import os
import subprocess
import re
from LookUp import get_info_file
import time

class RankCResult:
    def __init__(self):
        self.distinct_terms = 0
        self.words = []
        self.top_documents = []
        self.run_time = 0.0  # Menambahkan atribut run_time

    def parse_output(self, output, start_time):
        lines = output.split('\n')

        # Parsing distinct terms
        self.distinct_terms = int(lines[0].split()[1])

        # Mencari baris yang mengandung pola '#Word'
        word_lines = [line for line in lines if '#Word' in line]

        for word_line in word_lines:
            # Mencocokkan pola '#Word' menggunakan ekspresi reguler
            match = re.match(r"#Word \['(?P<word>\w+)'\], fw \(num of doc containing the word\) = (?P<fw>\d+\.\d+)", word_line)

            if match:
                word = match.group('word')
                fw = float(match.group('fw'))
                self.words.append({'word': word, 'fw': fw})

        # Mencari baris yang mengandung pola 'Document [...]' untuk mendapatkan informasi dokumen
        document_lines = [line for line in lines if re.match(r"Document \[\d+ \d+\.+txt\] or docno \d+ ranked = \d+\.\d+", line)]

        # Mencocokkan pola 'Document [...]' menggunakan ekspresi reguler untuk setiap baris
        for doc_line in document_lines:
            match = re.match(r"Document \[(?P<id>\d+) (?P<file>\d+\.+txt)\] or docno (?P<docno>\d+) ranked = (?P<ranked>\d+\.\d+)", doc_line)

            if match:
                info_file = get_info_file('data/' + match.group('file'))
                document_info = {
                    'document_id': int(match.group('id')),
                    'docno': match.group('docno'),
                    'file': match.group('file'),
                    'ranked': float(match.group('ranked')),
                    'title': info_file.title
                }
                self.top_documents.append(document_info)
            else:
                print(f"Failed to match line: {doc_line}")

        # Menghitung waktu eksekusi
        end_time = time.time()
        self.run_time = end_time - start_time

    def __str__(self):
        result_str = f"# Found {self.distinct_terms} distinct terms in {len(self.top_documents)} documents\n"
        if self.words:
            for word_info in self.words:
                result_str += f"# Word ['{word_info['word']}'], fw (num of doc containing the word) = {word_info['fw']}\n"
        else:
            result_str += f"# Word is not indexed or all query terms are stopword\n"
        if self.top_documents:
            result_str += "\n# Top 15th documents are:\n"
            for doc in self.top_documents:
                result_str += f"Document [{doc['document_id']} {doc['file']}] or docno {doc['docno']} ranked = {doc['ranked']}\n"
        result_str += f"# Time required: {self.run_time} seconds\n"
        return result_str

def get_rank_c_query(parameter, k):
    c_program_directory = os.path.join(os.path.dirname(__file__), 'Rank-c')
    c_program_name = './querydb'

    try:
        current_directory = os.getcwd()
        os.chdir(os.path.abspath(c_program_directory))

        start_time = time.time()

        result = subprocess.run([c_program_name, parameter, k], stdout=subprocess.PIPE, text=True, check=True)
        output = result.stdout.strip()

        result_obj = RankCResult()
        result_obj.parse_output(output, start_time)

        return result_obj
    except subprocess.CalledProcessError as e:
        print(f"Error running C program: {e}")
        return None
    finally:
        if 'current_directory' in locals():
            os.chdir(current_directory)
