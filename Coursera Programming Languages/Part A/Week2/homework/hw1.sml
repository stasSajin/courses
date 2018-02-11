(*Q1. is older takes two dates and evaluates to true or false
It evaluates to true if the first argument is a date that comes before the
second argument*)
fun is_older(dates:(int * int * int) * (int * int * int)) =
    if #1 (#1 dates) < #1 (#2 dates) then true
    else if #1 (#1 dates) = #1 (#2 dates) andalso
            #2 (#1 dates) < #2 (#2 dates)
    then true
    else if
        #1 (#1 dates) = #1 (#2 dates) andalso
        #2 (#1 dates) = #2 (#2 dates) andalso
        #3 (#1 dates) < #3 (#2 dates)
    then true
    else false

(* tests for the function *)
val is_older_test1 = is_older ((1,2,3),(2,3,4)) = true
val is_older_test2 = is_older ((2,2,3),(2,2,4)) = true
val is_older_test3 = is_older ((2,2,2),(2,3,1)) = true
val is_older_test4 = is_older ((2,2,2),(2,2,2)) = false
val is_older_test5 = is_older ((3,3,1),(2,3,2)) = false


(*Q2.  Write a function number_in_month that takes a list of dates and a month
(i.e., an int) and returns how many dates in the list are in the given month.*)
fun number_in_month(dates: (int*int*int) list, month: int) =
    let fun exists(date: (int*int*int)) =
        if #2 date = month then 1 else 0
    in

    if null dates
    then 0
    else exists(hd(dates)) + number_in_month(tl(dates), month)

    end

(*tests for the function*)
val number_in_month_test1 = number_in_month ([(2012,2,28),(2013,12,1)],2) = 1
val number_in_month_test2 = number_in_month ([(2012,2,28),(2013,12,1)],3) = 0
val number_in_month_test3 = number_in_month ([(2012,2,28)],2) = 1

(*Q3. Write a function number_in_months that takes a list of dates and a
list of months (i.e., an int list) and returns the number of dates in the list
of dates that are in any of the months in the list of months. Assume the list
of months has no number repeated. Hint: Use your answer to the previous problem
val number_in_months_test1 = number_in_months ([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[2,3,4]) = 3
val number_in_months_test2 = number_in_months ([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[5,5,5]) = 0
val number_in_months_test3 = number_in_months ([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[2]) = 1*)
