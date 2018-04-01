use "hw1.sml"

(* tests for the function *)
val is_older_test1 = is_older ((1,2,3),(2,3,4)) = true
val is_older_test2 = is_older ((2,2,3),(2,2,4)) = true
val is_older_test3 = is_older ((2,2,2),(2,3,1)) = true
val is_older_test4 = is_older ((2,2,2),(2,2,2)) = false
val is_older_test5 = is_older ((3,3,1),(2,3,2)) = false

(* val number_in_month_test1 = number_in_month ([(2012,2,28),(2013,12,1)],2) = 1
val number_in_month_test2 = number_in_month ([(2012,2,28),(2013,12,1)],3) = 0
val number_in_month_test3 = number_in_month ([(2012,2,28)],2) = 1

val number_in_months_test1 = number_in_months ([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[2,3,4]) = 3
val number_in_months_test2 = number_in_months ([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[5,5,5]) = 0
val number_in_months_test3 = number_in_months ([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[2]) = 1

val dates_in_month_test1 = dates_in_month ([(2012,2,28),(2013,12,1)],2) = [(2012, 2, 28)]
val dates_in_month_test2 = dates_in_month ([(2012,3,28),(2013,12,1)],2) = []
val dates_in_month_test3 = dates_in_month ([],2) = []

val dates_in_months_test1 = dates_in_months ([(2012,2,28),(2013,12,1)],[2,12]) = [(2012,2,28),(2013,12,1)]
val dates_in_months_test2 = dates_in_months ([(2012,2,28),(2013,12,1)],[2,4]) = [(2012,2,28)]

val get_nth_test1 = get_nth(["a", "b", "c"], 2) = "b"
val get_nth_test2 = get_nth(["a", "b", "c"], 1) = "a"

val date_to_string_test1 = date_to_string((1,1, 2017)) = "January 1, 2017"
val date_to_string_test2 = date_to_string((2,12, 2017)) = "December 2, 2017"

val number_before_reaching_sum_test1 = number_before_reaching_sum(10, [1, 2, 3, 4, 5]) = 3
val number_before_reaching_sum_test2 = number_before_reaching_sum(20, [1, 20, 3, 4, 5]) = 1

val what_month_test1 = what_month(30) = 1
val what_month_test2 = what_month(365) = 12

val month_range_test1 = month_range(1, 30)
val month_range_test2 = month_range(60, 365)  *)
