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

(*Q3. Write a function number_in_months that takes a list of dates and a
list of months (i.e., an int list) and returns the number of dates in the list
of dates that are in any of the months in the list of months. Assume the list
of months has no number repeated. Hint: Use your answer to the previous problem*)

fun number_in_months(dates: (int*int*int) list, months: int list) =
    if null months
    then 0
    else number_in_month(dates, hd(months)) + number_in_months(dates, tl(months))

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

(*Q5 Write a function dates_in_months that takes a list of dates and a list of months (i.e., an int list)
and returns a list holding the dates from the argument list of dates that are in any of the months in
the list of months. Assume the list of months has no number repeated. Hint: Use your answer to the
previous problem and SML’s list-append operator (@). *)

fun dates_in_months (dates: (int*int*int) list, m: int list) =
  if null m then
    [ ]
  else dates_in_month(dates, hd m) @ dates_in_months (dates, tl m)

(*Q6 Write a function get_nth that takes a list of strings and an int n and returns the nth element of the
list where the head of the list is 1st. Do not worry about the case where the list has too few elements:
your function may apply hd or tl to the empty list in this case, which is okay. *)

fun get_nth (elements: string list, n: int) =
  if n = 1
  then hd elements
  else get_nth(tl elements, n-1)

(*Q7 Write a function date_to_string that takes a date and returns a string of the form January 20, 2013
(for example). Use the operator ^ for concatenating strings and the library function Int.toString
for converting an int to a string. For producing the month part, do not use a bunch of conditionals.
Instead, use a list holding 12 strings and your answer to the previous problem. For consistency, put a
comma following the day and use capitalized English month names: January, February, March, April,
May, June, July, August, September, October, November, December. *)
val string_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

fun date_to_string(date: int*int*int) =
    get_nth(string_months, #2 date) ^ " " ^ Int.toString(#1 date) ^ ", " ^ Int.toString(#3 date)

(*Q8 Write a function number_before_reaching_sum that takes an int called sum, which you can assume
is positive, and an int list, which you can assume contains all positive numbers, and returns an int.
You should return an int n such that the first n elements of the list add to less than sum, but the first
n + 1 elements of the list add to sum or more. Assume the entire list sums to more than the passed in
value; it is okay for an exception to occur if this is not the case *)

exception EmptyList
fun number_before_reaching_sum(sum: int, numbers: int list) =
    if null numbers then raise EmptyList
    else if sum - hd numbers <= 0 then 0
    else 1 + number_before_reaching_sum(sum - hd numbers, tl numbers)

(*Q9 Write a function what_month that takes a day of year (i.e., an int between 1 and 365) and returns
what month that day is in (1 for January, 2 for February, etc.). Use a list holding 12 integers and your
answer to the previous problem. *)

fun what_month(day) =
  let
    val day_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  in
    number_before_reaching_sum(day, day_months) + 1
  end

(*Q10 Write a function month_range that takes two days of the year day1 and day2 and returns an int list
[m1,m2,...,mn] where m1 is the month of day1, m2 is the month of day1+1, ..., and mn is the month
of day day2. Note the result will have length day2 - day1 + 1 or length 0 if day1>day2. *)

fun month_range(day1: int, day2: int) =
  if day1 > day2 then []
  else what_month(day1)::month_range(day1+1, day2)

(*Q11 Write a function oldest that takes a list of dates and evaluates to an (int*int*int) option. It
evaluates to NONE if the list has no dates and SOME d if the date d is the oldest date in the list. *)
fun oldest(dates: (int*int*int) list)=
  if null dates then NONE
  else
    let
      val current_oldest = oldest(tl dates)
    in
      if isSome current_oldest andalso is_older(valOf current_oldest, hd dates)
    then
      current_oldest
    else
      SOME(hd dates)
    end

(*Q12 Challenge Problem: Write functions number_in_months_challenge and dates_in_months_challenge
that are like your solutions to problems 3 and 5 except having a month in the second argument multiple
times has no more effect than having it once. (Hint: Remove duplicates, then use previous work.) *)

fun remove_duplicates(xs: int list)=
  let
      fun check_list(xs: int list, item: int) =
          if null xs
            then false
          else if hd xs = item
            then true
          else check_list(tl xs, item)
      fun check_list_of_lists(xs: int list) =
        if null xs
          then []
        else if check_list(tl xs, hd xs)
          then check_list_of_lists(tl xs)
        else hd xs::check_list_of_lists(tl xs)
   in
        check_list_of_lists(xs)
  end

fun number_in_months_challenge (dates : (int*int*int) list, months : int list) =
  if null dates orelse null months then
    0
  else
    number_in_months(dates, remove_duplicates(months))

fun dates_in_months_challenge (dates : (int*int*int) list, months : int list) =
  if null dates orelse null months then
    [ ]
  else
    dates_in_months(dates, remove_duplicates(months))


(*Q13 Challenge Problem: Write a function reasonable_date that takes a date and determines if it
describes a real date in the common era. A “real date” has a positive year (year 0 did not exist), a
month between 1 and 12, and a day appropriate for the month. Solutions should properly handle leap
years. Leap years are years that are either divisible by 400 or divisible by 4 but not divisible by 100.
(Do not worry about days possibly lost in the conversion to the Gregorian calendar in the Late 1500s.) *)
