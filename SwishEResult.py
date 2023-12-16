import os
import subprocess
import re #rf

class SwishEResult:
    def __init__(self):
        self.search_words = ""
        self.number_of_hits = 0
        self.search_time = 0.0
        self.run_time = 0.0
        self.documents = []

    def parse_output(self, output):
        lines = output.split('\n')

        # Parsing search words
        search_words_line = [line for line in lines if '# Search words:' in line]
        if search_words_line:
            self.search_words = search_words_line[0].split(':')[1].strip()

        # Parsing number of hits
        hits_line = [line for line in lines if '# Number of hits:' in line]
        if hits_line:
            self.number_of_hits = int(hits_line[0].split(':')[1])

        # Parsing search time
        search_time_line = [line for line in lines if '# Search time:' in line]
        if search_time_line:
            searchTime = search_time_line[0].split(':')[1].split()[0]
            # Change , to . because of output from swish-e on different version
            if ',' in searchTime:
                searchTime = searchTime.replace(',', '.')

            self.search_time = float(searchTime)

        # Parsing run time
        run_time_line = [line for line in lines if '# Run time:' in line]
        if run_time_line:
            runTime = run_time_line[0].split(':')[1].split()[0]
            # Change , to . because of output from swish-e on different version
            if ',' in runTime:
                runTime = runTime.replace(',', '.')

            self.run_time = float(runTime)

        # Parsing document information
        document_lines = [line for line in lines if re.match(r"\d+ Rank-c/.+/\w+\.txt .+", line)]

        for doc_line in document_lines:
            match = re.match(r'(?P<rank>\d+) Rank-c/data/(?P<file_path>\w+\.txt) "(?P<content>.+)" (?P<skor>\d+)', doc_line)

            if match:
                document_info = {
                    'rank': int(match.group('rank')),
                    'file_path': match.group('file_path'),
                    'content': match.group('content'),
                    'skor': int(match.group('skor'))
                }
                self.documents.append(document_info)
            else:
                print(f"Failed to match line: {doc_line}")

    def __str__(self):
        result_str = f"# Search words: {self.search_words}\n"
        result_str += f"# Number of hits: {self.number_of_hits}\n"
        result_str += f"# Search time: {self.search_time} seconds\n"
        result_str += f"# Run time: {self.run_time} seconds\n"

        if self.documents:
            result_str += "\n# Top documents are:\n"
            for doc in self.documents:
                result_str += f"{doc['rank']} {doc['file_path']} {doc['content']}\n"

        return result_str
    

def get_swish_e_query(parameter, k):
    try:
        # Ganti spasi dengan ' or ' dalam parameter
        parameter = ' or '.join(parameter.split())

        # Sertakan parameter saat menjalankan Swish-e
        result = subprocess.run(['swish-e', '-w', parameter, '-m',k], stdout=subprocess.PIPE, text=True, check=True)
        output = result.stdout.strip()

        # Buat objek SwishEResult dan parse output Swish-e
        result_obj = SwishEResult()
        result_obj.parse_output(output)

        return result_obj
    except subprocess.CalledProcessError as e:
        print(f"Error running Swish-e: {e}")
        return None

