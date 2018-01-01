# The objective of Part 1 is to write a function that computes the factorial of an integer greater than or equal to 0. Recall that the factorial of a number n is n * (n-1) * (n - 2) * … * 1. The factorial of 0 is defined to be 1. Before taking on this part of the assignment, you may want to review the section on Functional Programming in this course (you can also read that section here).
# 
# For this Part you will need to write four different versions of the Factorial function:
#   
# 1. Factorial_loop: a version that computes the factorial of an integer using looping (such as a for loop)
# 2. Factorial_reduce: a version that computes the factorial using the reduce() function in the purrr package. Alternatively, you can use the Reduce() function in the base package.
# 3. Factorial_func: a version that uses recursion to compute the factorial.
# 4. Factorial_mem: a version that uses memoization to compute the factorial.
# After writing your four versions of the Factorial function, use the microbenchmark package to time the operation of these functions and provide a summary of their performance. In addition to timing your functions for specific inputs, make sure to show a range of inputs in order to demonstrate the timing of each function for larger inputs.
# 
# In order to submit this assignment, please prepare two files:
#   
# 1. factorial_code.R: an R script file that contains the code implementing your classes, methods, and generics for the longitudinal dataset.
# 
# 2. factorial_output.txt: a text file that contains the results of your comparison of the four different implementations.


# load dependencies
library(purrr)
library(testthat)
library(microbenchmark)

# Factorial Loop Implementation
factorial_loop <- function(x){
  stopifnot(x >= 0)
  result = 1
  if(x==0){
    return(result)
  }
  for(i in x:1){
    result = result * i 
  }
  result
}

# Factorial reduce implementation
factorial_reduce <- function(x){
  stopifnot(x >= 0)
  result = 1
  if(x==0){
    return(result)
  }
  reduce(x:1, `*`)
}

# Factorial functional implementation
factorial_recursion <- function(x){
  stopifnot(x >= 0)
  # base case
  if(x == 0){
    1
  } else {
    x * factorial_recursion(x - 1)
  }
}


# factorial mem function (doesn't make a lot of sense in this context, unless the reuslts are stored somewhere for later use)
fact_tbl <- c(rep(NA, 100))
factorial_mem <- function(x) {
  stopifnot(x >= 0)
  if (x == 0)
    return(1)
  if (!is.na(fact_tbl)[x])
    return(fact_tbl[x])
  fact_tbl[x] <<- x * factorial_mem(x - 1)
  fact_tbl[x]
}

######### TEST FACTORIAL FUNCTIONS ################
sink("factorial_output.txt")
# check that functions work properly by testing against the built in factorial function
test_factorial <- function(){
  x <- sample(0:100, 1)
  expect_equal(factorial(x),
               factorial_loop(x),
               factorial_recursion(x),
               factorial_mem(x))
  sprintf('hey, it passed for %s!', x)
}

test_multiple_func <- function(f, n){
  # tests a function repeatedly. f represents the function, n represents the number of times to test
  replicate(n, f)
  print('All tests passed')
}

test_multiple_func(test_factorial, 100)

print('get the performance of functions for different inputs')
######## Check the performance of each function ########
# reset lookup table
fact_tbl <- c(rep(NA, 100))
inputs <- seq(0, 50, 10)

results <- map(inputs, ~ microbenchmark(
  factorial_loop(.),
  factorial_reduce(.),
  factorial_recursion(.),
  factorial_mem(.)
))

names(results) <- as.character(inputs)
results

print('get the results for a range of benchmarks')
get_performance <- function(x) {
  fact_tbl <<- c(rep(NA, 100))
  microbenchmark(map_dbl(x, factorial_loop),
                 map_dbl(x, factorial_reduce),
                 map_dbl(x, factorial_recursion),
                 map_dbl(x, factorial_mem))
}

ranges <- list(`range 1:10` = 1:10,
               `range 1:50` = 1:25,
               `range 1:100` = 1:100)

results <- map(ranges, get_performance)
results

sink()

