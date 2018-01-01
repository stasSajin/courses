# I'll be using S3 to complete this assignment
library(tidyverse)

# You will need to design a class called “LongitudinalData” that characterizes the structure of this longitudinal dataset. You will also need to design classes to represent the concept of a “subject”, a “visit”, and a “room”.
# 
# In addition you will need to implement the following functions
# 
# make_LD: a function that converts a data frame into a “LongitudinalData” object
# subject: a generic function for extracting subject-specific information
# visit: a generic function for extracting visit-specific information
# room: a generic function for extracting room-specific information
# For each generic/class combination you will need to implement a method, although not all combinations are necessary (see below). You will also need to write print and summary methods for some classes (again, see below).
# 
# To complete this Part, you can use either the S3 system, the S4 system, or the reference class system to implement the necessary functions. It is probably not wise to mix any of the systems together, but you should be able to compete the assignment using any of the three systems. The amount of work required should be the same when using any of the systems.

# converting df into a LongitudinalData object
make_LD <- function(df){
  structure(df, class = "LongitudinalData")
}

# set up a printing method for the LongitudinalObject
print.LongitudinalData <- function(df) {
  cat("Longitudinal dataset with", length(unique(df[['id']])), "subjects")
}

# method for finding subject specific info
subject <- function(df, subject_id) UseMethod("subject")
subject.LongitudinalData <- function(df, subject_id) {
  if(sum(df$id == subject_id) == 0)
    return(NULL)
  df <- df[df$id == subject_id]
  print(dim(df))
  structure(df, class = "Subject")
}


# printing method for subjects
print.Subject <- function(df) {
  cat("Subject ID:", df[["id"]])
  invisible(df)
}



library(readr)
library(magrittr)
library(tidyr)
source("oop_code.R")

data <- read_csv("data/MIE.csv")


x <- make_LD(data)
print(class(x))
print(x)
out <- subject(x, 10)
print(out)
out <- subject(x, 14)
print(out)
