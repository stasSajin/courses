#' Read a csv file with automobile fatalities data
#'
#' \code{fars_read} Reads a specific csv datafile using the provided filename.
#'
#' @param filename The csv filename.
#'
#' @return The function will use the provided file_path to load the data
#'  contained in the csv in memory. If the file cannot be found, the function
#'  will provide an error message.
#' @export
#'
#' @examples
#' fars_read('data/accident_2013.csv.bz2')
#'
#' @importFrom readr read_csv
#' @importFrom dplyr tbl_df
fars_read <- function(filename) {
        if(!file.exists(filename))
                stop("file '", filename, "' does not exist")
        data <- suppressMessages({
                readr::read_csv(filename, progress = FALSE)
        })
        dplyr::tbl_df(data)
}



#' Create a filename for a specific year
#'
#' @param year a numeric value specifying the year
#'
#' @return A string representing a filename in the following format
#'  'accident_year.csv.bz2', where year will be replaced by the provided year
#' @export
#'
#' @examples
#' make_filename(1999)
make_filename <- function(year) {
        year <- as.integer(year)
        sprintf("accident_%d.csv.bz2", year)
}

#' Read multiple csv files for specific years
#'
#' \code{fars_read_years} accepts a vector of years. For each year, the functon invokes
#' \code{make_filename} that creates a file name based on a provided year and then reads
#' the contents of the csv using \code{fars_read}. The function will return a warning if
#' and invalid year is provided.
#'
#' @param years a vector of years, where each year must be a valid integer year
#'
#' @return A list of dataframes for each year
#' @export
#'
#' @examples
#' fars_read_years(c(2016, 2017))
fars_read_years <- function(years) {
        lapply(years, function(year) {
                file <- make_filename(year)
                tryCatch({
                        dat <- fars_read(file)
                        dplyr::mutate(dat, year = year) %>%
                                dplyr::select(MONTH, year)
                }, error = function(e) {
                        warning("invalid year: ", year)
                        return(NULL)
                })
        })
}




#' Total fatality statitics for each year and month
#'
#' \code{fars_summarize_years} will compute total fatality statistics for each
#' year and month. The function takes in a list of years for which statistics
#' are computed.
#'
#' @param years A vector of years
#'
#' @return A table of total accident counts broken by year and month.
#' @export
#'
#' @importFrom dplyr bind_rows group_by summarize
#' @importFrom tidyr spread
#' @examples
#' fars_summarize_years(c(2016, 2017))
fars_summarize_years <- function(years) {
        dat_list <- fars_read_years(years)
        dplyr::bind_rows(dat_list) %>%
                dplyr::group_by(year, MONTH) %>%
                dplyr::summarize(n = n()) %>%
                tidyr::spread(year, n)
}

#' Map accidents for a state
#'
#'
#' \code{fars_map_state} will plot the accidents for a provided state and year
#'
#' @param state.num State number
#' @param year The year for which the accidents should be mapped
#'
#' @return The return value will be a map of accidents for a state and year.
#' If one provides an invalid state, the function will provide an error indicating
#' and invalid State number. Also, if no accidents were found for a state and year
#' combination, then the function will return a message indicating that no accidents can
#' be plotted.
#' @export
#'
#' @importFrom dplyr filter
#' @importFrom maps map
#' @importFrom graphics points
#'
#' @examples
#' fars_map_state(3, 2017)
fars_map_state <- function(state.num, year) {
        filename <- make_filename(year)
        data <- fars_read(filename)
        state.num <- as.integer(state.num)

        if(!(state.num %in% unique(data$STATE)))
                stop("invalid STATE number: ", state.num)
        data.sub <- dplyr::filter(data, STATE == state.num)
        if(nrow(data.sub) == 0L) {
                message("no accidents to plot")
                return(invisible(NULL))
        }
        is.na(data.sub$LONGITUD) <- data.sub$LONGITUD > 900
        is.na(data.sub$LATITUDE) <- data.sub$LATITUDE > 90
        with(data.sub, {
                maps::map("state", ylim = range(LATITUDE, na.rm = TRUE),
                          xlim = range(LONGITUD, na.rm = TRUE))
                graphics::points(LONGITUD, LATITUDE, pch = 46)
        })
}
