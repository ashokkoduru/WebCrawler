The Class of the indexer.py is Indexer

It can run directly by calling 

python indexer.py

I have a written a function called in tasks_hw3 in which we can call the required methods from the Indexer class
The call should be of the format 

You can change the required values in the above method and run the ‘indexer.py' file

The Indexer Class has following methods

ind = Indexer()

1. build_parsed_corpus
This method takes the downloaded html files from the folder called corpus. If the folder is not present it creates the corpus folder and asks the user to put the raw html files in that. It parses each file from the folder corpus and puts the clean data file in to the folder called parsed_corpus

2. create_tf_table
It takes three parameters
	1. n - it specifies the which gram index should be built
	2. plot - Boolean value whether the plot should be shown (optional)
	3. file save = Boolean which tell whether the file should be saved or not(optional)

It should be called in the following way

ind.create_tf_table(1)

3. create_df_table
It takes n as parameter which decides which gram should be built for the document frequency table

It should be called the following way

ind.create_df_table(2)



 




