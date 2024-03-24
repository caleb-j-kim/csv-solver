Instructions:
 This Constraint Satisfaction Problem Solver (CSP Solver) reads in both a var and a con file before 
prompting the user to determine whether they want to use backtracking exclusively or if they 
want to use backtracking and forward checking to find the solution to the CSP solver.

 Inside of the var file there will be a certain amount of sets that are labeled as unique letters and 
inside of each set will be a varying amount of numbers. 

 The con file will contain a set of constraints or rules that each set must follow in order to find 
the correct solution. 

 When the program has found the solution, it outputs each set and the remaining value(s) that 
each set concludes with while following the given constraints.

Sample Input and Output:
Sample var file:
ex1.var

Sample con file:
ex1.con

Backtracking Analysis:
Backtracking is used in this program because it guarantees that the CSV Solver will find a solution unless 
it truly does not exist. It is based off of a depth-first search and uses this logic to search through the 
problem space to find values that fit with each constraint. This search algorithm can also be seamlessly 
combined with minimum remaining value and least constraining value heuristics to optimize the 
decision making that the backtracking algorithm performs. 
However, this algorithm can be inefficient for large-scale CSPs due to its depth-first nature which could 
lead to a large number of unnecessary recursive calls and back tracks.

Forward Checking Analysis:
As mentioned previously, the backtracking algorithm can be somewhat inefficient if it is given a large 
amount of data as it shares the weakness that depth-first search algorithms have. The inclusion of 
forward checking along with backtracking allows for greater efficiency as the backtracking will have a 
smarter search strategy when searching through the problem space. Forward checking detects 
constraint violations as soon as they occur by checking the impact of each variable assignment on 
domains of unassigned variables and prunes the domains of unassigned variables before the 
backtracking algorithm comes into contact with them, shortening the overall search space and leading 
to fewer recursive calls / a faster solution calculation time.
