Problem:

Simple Distributed File Indexer
Create a multi-process, command-line indexer application that finds the top 10 words across a collection of documents. 

1. Have a fixed number (N) of worker processes (say, N=3) that handle text indexing. Workers should be able to run on separate machines from each other.
2. When a worker process receives a text blob to process, it tokenizes it into words. Words are delimited by any character other than A‐Z or 0‐9.
3. A master collection, shared between all workers, keeps track of all unique words encountered and the number of times it was encountered. Each time a word is encountered, the count for that word is incremented (the word is added to the list if not present). Words should be matched in a case-insensitive manner and without any punctuation.
4. The application should output the top 10 words (and their counts) to standard out.

Approach:

Since the problem states distributing  the data across multiple machines (workers) and the data should be shared between multiple processes, Python’s multiprocessing module can be used to solve this problem.

Python multiprocessing supports spawning sub processes and offers both local and remote concurrency, effectively side-stepping the Global Interpreter Lock by using subprocesses instead of threads. So it can be used to create inter-process communication on networked systems. 

Note: ZeroMQ can be used instead of Python mulltiprocessing for similar inter-process messaging on a single machine with its IPC protocol, but it also has network-based protocols that allows you to send messages between processes running on different machines as well.
Also, ZeroMQ is robust and will be stable implementation compared to Python mulitprocessing module. ZeroMQ is used by large community.


Assumptions:

- Firewall in client machines allow the connection to server machine.
- The linux machines are used to execute this program (preferred). Windows machines can also be used. 
- Python version used here is 2.7.1 and above
- Text blobs collection is hardcoded in the program.
- Worker processes are set to 3 

Execution Instructions:

1. If both server and workers (clients) are on same machine.

	Step 1: Open Terminal and run the below command
		python mp_server.py 
	
		and it should display the following message

	“””
Starting Server at 50000 port number.....

Waiting for responses from workers...
	“””

	Step 2: Open another Terminal and run the below command
		python mp_worker.py 

		and you will receive if the scripts runs successfully (worker finishes job completely!)
		“””
		Client connecting to a server....

Job done.
		“””

	Step 3: Run the above command for two more times because there are 3 workers set in the program.

Step 4: Check first Terminal now and you should see the output message like below

“”””
Starting Server at 50000 port number.....

Waiting for responses from workers...

Word 		 Count
************************************************************
Fred 		 33
was 		 114
a 		 69
handsome 		 3
athletic 		 3
youngster 		 3
and 		 183
he 		 81
sat 		 3
his 		 114
“”””



2. If server and workers (clients) are running on different machines.

	Step 1: Login to first machine and open mp_server.py in editor and change IP_ADDRESS to the IP address of the machine on which this script will be running.

Step 2: Open Terminal and run the below command
		python mp_server.py 
	
		and it should display the following message

	“””
Starting Server at 50000 port number.....

Waiting for responses from workers...
	“””

	Step 3: Login to another machine and open mp_worker.py in editor and change IP_ADDRESS to the IP address of the first machine (Server).

 	Step 4: Open Terminal and run the below command
		python mp_worker.py 

		and you will receive if the scripts runs successfully (worker finishes job completely!)
		“””
		Client connecting to a server....

Job done.
		“””

	Step 3: Run the above command for two more times because there are 3 workers set in the program.

Step 4: Check Terminal in Server machine now and you should see the output message like below

“”””
Starting Server at 50000 port number.....

Waiting for responses from workers...

Word 		 Count
************************************************************
Fred 		 33
was 		 114
a 		 69
handsome 		 3
athletic 		 3
youngster 		 3
and 		 183
he 		 81
sat 		 3
his 		 114
“”””	
		
TODO:

- Implement logging
- Write unit test cases
- Implement Configuration Parser (http://docs.python.org/2/library/configparser.html)


Sample Output:

Server:

zeltmac03:file_indexer pshilavantar$ python mp_server.py 
Starting Server at 50000 port number.....

Waiting for responses from workers...

Word 		 Count
************************************************************
Fred 		 33
was 		 114
a 		 69
handsome 		 3
athletic 		 3
youngster 		 3
and 		 183
he 		 81
sat 		 3
his 		 114

Worker:

zeltmac03:file_indexer pshilavantar$ python mp_worker.py 
Client connecting to a server....

Job done.
zeltmac03:file_indexer pshilavantar$ python mp_worker.py 
Client connecting to a server....

Job done.
zeltmac03:file_indexer pshilavantar$ python mp_worker.py 
Client connecting to a server....

Job done.








