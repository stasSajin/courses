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
of months has no number repeated. Hint: Use your answer to the previous problem*)

fun number_in_months(dates: (int*int*int) list, months: int list) =
    if null months
    then 0
    else number_in_month(dates, hd(months)) + number_in_months(dates, tl(months))

val number_in_months_test1 = number_in_months ([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[2,3,4]) = 3
val number_in_months_test2 = number_in_months ([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[5,5,5]) = 0
val number_in_months_test3 = number_in_months ([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[2]) = 1

(*Q4 Write a function dates_in_month that takes a list of dates and a month (i.e., an int) and returns a
list holding the dates from the argument list of dates that are in the month. The returned list should
contain dates in the order they were originally given.*)
fun dates_in_month (dates: (int*int*int) list, m: int) =
  if null dates then
    [ ]
  else if #2 (hd dates) = m then
    hd dates :: dates_in_month(tl dates, m)
  else
    dates_in_month(tl dates, m)

val dates_in_month_test1 = dates_in_month ([(2012,2,28),(2013,12,1)],2) = [(2012, 2, 28)]
val dates_in_month_test2 = dates_in_month ([(2012,3,28),(2013,12,1)],2) = []
val dates_in_month_test3 = dates_in_month ([],2) = []

(*Q5 Write a function dates_in_months that takes a list of dates and a list of months (i.e., an int list)
and returns a list holding the dates from the argument list of dates that are in any of the months in
the list of months. Assume the list of months has no number repeated. Hint: Use your answer to the
previous problem and SML’s list-append operator (@). *)

fun dates_in_months (dates: (int*int*int) list, m: int list) =
  if null m then
    [ ]
  else dates_in_month(dates, hd m) @ dates_in_months (dates, tl m)

val dates_in_months_test1 = dates_in_months ([(2012,2,28),(2013,12,1)],[2,12]) = [(2012,2,28),(2013,12,1)]
val dates_in_months_test2 = dates_in_months ([(2012,2,28),(2013,12,1)],[2,4]) = [(2012,2,28)]


(*Q6 Write a function get_nth that takes a list of strings and an int n and returns the nth element of the
list where the head of the list is 1st. Do not worry about the case where the list has too few elements:
your function may apply hd or tl to the empty list in this case, which is okay. *)

fun get_nth (elements: string list, n: int) =
  if n = 1
  then hd elements
  else get_nth(tl elements, n-1)


val get_nth_test1 = get_nth(["a", "b", "c"], 2) = "b"
val get_nth_test2 = get_nth(["a", "b", "c"], 1) = "a"

(*Q7 Write a function date_to_string that takes a date and returns a string of the form January 20, 2013
(for example). Use the operator ^ for concatenating strings and the library function Int.toString
for converting an int to a string. For producing the month part, do not use a bunch of conditionals.
Instead, use a list holding 12 strings and your answer to the previous problem. For consistency, put a
comma following the day and use capitalized English month names: January, February, March, April,
May, June, July, August, September, October, November, December. *)
val string_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

fun date_to_string(date: int*int*int) =
    (* let
      val day = #1 date
      val month = get_nth(string_months, #2 date)
      val year = #3 date
    in
      month ^ " " ^ Int.toString(day) ^ ", " Int.toString(month) *)
    Int.toString(1)
