Multimedia & Web Databases Project - Phase 3:
------------------------------------------------------
Contents in the Folder:
Code
Outputs 
Report 
------------------------------------------------------
Software - Python 3.3+
OS - Linux Ubuntu 14.0.4
------------------------------------------------------
Have the following packages installed in your library before starting
1) sklearn.decomposition
2) numpy
3) lda
4) scipy
5) tensorly
6) math
7) sqlite3
8) csv
------------------------------------------------------
Code:
- Run 'createDB.py' only once for the entire implementation at the beginning
- This creates a database of the MovieLens+IMDB data (in csv files) in the form of tables
- 'dbInfo.py' contains functions of all operations performed to tables in the database to extract desired information whenever required
- 'utils.py' contains mathematical functions which are required for some tasks

- Task 1 (Movie Recommendations) & Task 2 (Probabilistic Relevance Feedback)
  - Run 'task1a_3.py' for movie recommendations using SVD or PCA  
  - Run 'task1b_3.py' for movie recommendations using LDA
  - Run 'task1c_3.py' for movie recommendations using Tensor decomposition
  - Run 'task1d_3.py' for movie recommendations using Personalized PageRank
  - Run 'task1e_3.py' for movie recommendations combining all the above methods
  The system asks user's feedback (Relevant and Irrelevant Movies) and gives modified movie recommendations in each sub-task for Task2 

- Task 3 (LSH & Nearest Neighbors) & Task 4 (NN-based Relevance Feedback)
  - Run 'task3_3.py' for implementing Task 3
  The system asks user's feedback (Relevant and Irrelevant Movies) and gives modified movie recommendations for Task4 

- Task 5 (Classification)
  - Run 'task5a_3.py' for implementing Task 5a
  - Run 'task5b_3.py' for implementing Task 5b
  - Run 'task5c_3.py' for implementing Task 5c
------------------------------------------------------
Outputs:
- Contains outputs for each task
------------------------------------------------------
Report:
- MWDB_Phase3.pdf
- Contains theoretical explanations for all the implementations done and also gives justification to the assumptions taken
------------------------------------------------------
