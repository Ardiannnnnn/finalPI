This indexing is done with 3 tools, namely using `Rank-c` (which is indexing using the c language), `swish-e`, and `Solr`.

## Requirements
make sure `flask` (for website search engine simulation), `swish-e`, `solr` and `c compiler` are installed and functioning normally. (recommended using Linux, especially ubuntu)

## Running Flask
to run flask to display a search engine simulation, you can use the following command :
```
python app.py
```
After that, you can just open [http://localhost:5000](http://localhost:5000) by default

## Run the following command to compile and watch for changes for the Tailwind CSS file:
```
npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch
```

# Setup Rank-c
Indexing with Rank-c can be easily done by utilizing the Makefile that has been created in the Rank-c folder, navigate to the `Rank-c` folder in terminal with `cd Rank-c` and then run:
```
make index
``` 
it will create a new program file with the name `indexdb`, it is used for indexing and 
```
make query
``` 
it will create a new program file with the name `querydb`, it is used for searching.

## Run indexdb
to run `indexdb`, You can do it easily by run : 
```
./indexdb
```
make sure you are inside the folder where indexdb is located.
it will ask you for Data directory path, you can just type `data/` because here the data directory that we use by default is in `Rank-c/data/

`After indexing rank-c, you can use rank-c as a search method in flask.``

It will create some index file in `index-db/` folder.

## Run querydb
`querydb` can be run after you have indexed using `indexdb`, you can do it easily by run : 
```
./querydb "makan" 5
```
it indicates that we here want to search for the word "`makan ayam`" and want to display the top `5` results.

Output Example : 
```
#Found 2280 distict terms in 49 documents

#Word ['makan'], fw (num of doc containing the word) = 15.000000
#Word ['ayam'] is not indexed

#Top 5th documents are:
Document [0 28.txt] or docno 0 ranked = 2.600412
Document [18 12.txt] or docno 18 ranked = 2.011954
Document [32 21.txt] or docno 32 ranked = 1.594435
Document [6 35.txt] or docno 6 ranked = 1.594435
Document [34 2.txt] or docno 34 ranked = 1.594435
#Time required: 0.000000 mseconds
```

# Setup Swish-e
Make sure swish-e is installed and can be run on the system.

## Install Ubuntu
in ubuntu, you can easily run : 
```
apt-get install swish-e
```

## Index with Swish-e
Navigate to the directory where swish.conf is located and run it: 
```
swish-e -c swish.conf
```

`After indexing swish-e, you can use swish-e as a search method in flask.`

## Search with Swish-e
terminal search in swish-e can be done by :
```
swish-e -w 'makan'
```
`makan` here is the word to look for 
