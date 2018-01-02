library(tidyverse)

# Question 1 What is average Sample.Value for “Bromine PM2.5 LC” in the state of Wisconsin in this dataset?
df <- read_csv('data/daily_SPEC_2014.csv.bz2')
df %>% 
  filter(
    `State Name` == 'Wisconsin' &
    `Parameter Name` == 'Bromine PM2.5 LC') %>% 
  summarise(mean_bromine = mean(`Arithmetic Mean`, na.rm = TRUE))

# Question 2 Calculate the average of each chemical constituent across all states, monitoring sites and all time points. Which constituent Parameter.Name has the highest average level?
df %>% 
  group_by(`Parameter Name`) %>% 
  summarise(mean_consituent = mean(`Arithmetic Mean`, na.rm = TRUE)) %>% 
  arrange(desc(mean_consituent)) %>% 
  head(10)
  

# Question 3 Which monitoring site has the highest average level of “Sulfate PM2.5 LC” across all time? Indicate the state code, county code, and site number.
df %>% 
  filter(`Parameter Name` == 'Sulfate PM2.5 LC') %>% 
  group_by(`State Code`, `County Code`, `Site Num`) %>% 
  summarise(max_sulfate = mean(`Arithmetic Mean`, na.rm = TRUE)) %>% 
  arrange(desc(max_sulfate)) %>% 
  head(10)


# Question 4 What is the absolute difference in the average levels of “EC PM2.5 LC TOR” between the states California and Arizona, across all time and all monitoring sites?
df %>% 
  filter(
    `State Name` %in% c('California', 'Arizona'),
    `Parameter Name` == "EC PM2.5 LC TOR") %>%
  group_by(`State Name`) %>% 
  summarise(mean = mean(`Arithmetic Mean`, na.rm = TRUE)) %>% 
  spread(`State Name`, mean) %>%
  mutate(abs_diff = abs(Arizona - California))


# Question 5 What is the median level of “OC PM2.5 LC TOR” in the western United States, across all time? Define western as any monitoring location that has a Longitude LESS THAN -100.
df %>% 
  filter(
    Longitude < -100,
    `Parameter Name` == "OC PM2.5 LC TOR") %>%
  summarise(median = median(`Arithmetic Mean`, na.rm = TRUE))


# Question 6 Use the readxl package to read the file aqs_sites.xlsx into R (you may need to install the package first). This file contains metadata about each of the monitoring sites in the EPA’s monitoring system. In particular, the "Land Use" and "Location Setting" variables contain information about what kinds of areas the monitors are located in (i.e. “residential” vs. “forest”).

#How many monitoring sites are labelled as both RESIDENTIAL for "Land Use" and SUBURBAN for "Location Setting"?

library(readxl)
sites <- read_excel('data/aqs_sites.xlsx')
sites %>% 
  filter(`Land Use` == 'RESIDENTIAL',
         `Location Setting` == 'SUBURBAN') %>% 
  nrow()

# Question 7 What is the median level of “EC PM2.5 LC TOR” amongst monitoring sites that are labelled as both “RESIDENTIAL” and “SUBURBAN” in the eastern U.S., where eastern is defined as Longitude greater than or equal to -100?
df %>% 
  left_join(sites, by = c("Latitude", "Longitude")) %>%
  filter(`Land Use` == 'RESIDENTIAL',
         `Location Setting` == 'SUBURBAN',
         Longitude >= -100,
         `Parameter Name` == "EC PM2.5 LC TOR") %>% 
  summarise(med = median(`Arithmetic Mean`, na.rm = TRUE))


# Question 8 Amongst monitoring sites that are labeled as COMMERCIAL for "Land Use", which month of the year has the highest average levels of "Sulfate PM2.5 LC"?
df %>% 
  left_join(sites, by = c("Latitude", "Longitude")) %>%
  filter(`Land Use` == 'COMMERCIAL',
         `Parameter Name` == "Sulfate PM2.5 LC") %>% 
  mutate(month = lubridate::month(`Date Local`, label = TRUE)) %>%
  group_by(month) %>% 
  summarise(avg = mean(`Arithmetic Mean`, na.rm = TRUE)) %>%
  arrange(desc(avg))
  

# Question 9 Take a look at the data for the monitoring site identified by State Code 6, County Code 65, and Site Number 8001 (this monitor is in California). At this monitor, for how many days is the sum of "Sulfate PM2.5 LC" and "Total Nitrate PM2.5 LC" greater than 10?

# For each of the chemical constituents, there will be some dates that have multiple `Arithmetic Mean` values at this monitoring site. When there are multiple values on a given date, take the average of the constituent values for that date.
df %>% 
  filter(`State Code` == '06',
         `County Code` == '065',
         `Site Num` == '8001',
         `Parameter Name` %in% c("Sulfate PM2.5 LC", "Total Nitrate PM2.5 LC")) %>% 
  group_by(`Date Local`, `Parameter Name`) %>% 
  summarise(avg = mean(`Arithmetic Mean`, na.rm = TRUE)) %>% 
  group_by(`Date Local`) %>%
  summarise(Total = sum(avg, na.rm = TRUE)) %>%
  filter(Total > 10)


# Question 10 Which monitoring site in the dataset has the highest correlation between "Sulfate PM2.5 LC" and "Total Nitrate PM2.5 LC" across all dates? Identify the monitoring site by it's State, County, and Site Number code.

# For each of the chemical constituents, there will be some dates that have multiple Sample.Value's at a monitoring site. When there are multiple values on a given date, take the average of the constituent values for that date.

df %>% 
  filter(`Parameter Name` %in% c("Sulfate PM2.5 LC", "Total Nitrate PM2.5 LC")) %>% 
  group_by(`State Code`, `County Code`, `Site Num`, `Parameter Name`, `Date Local`) %>% 
  summarise(avg = mean(`Arithmetic Mean`, na.rm = TRUE)) %>% 
  spread(`Parameter Name`, avg) %>% 
  group_by(`State Code`, `County Code`, `Site Num`) %>% 
  summarise(correl = cor(`Sulfate PM2.5 LC`, `Total Nitrate PM2.5 LC`)) %>%
  arrange(desc(correl))
