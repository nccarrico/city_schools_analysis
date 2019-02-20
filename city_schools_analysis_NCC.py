# # PyCity Schools Analysis - N. C. Carrico
# 
# * All top 5 performing schools were charter schools while all 5 bottom performing schools were district schools
# 
# * The students at the top 5 schools performed better at both math and reading despite the lower spending per student at the top 5 schools; per student spending ranged from 578-638 dollars for the top 5 schools and 637-655 dollars for the bottom 5
# 
# * There were no visible trends of overall improvement or decline in math or reading scores for students from grade 9 to 12 at the different schools  
# 
# * Overall passing rate in math and reading was lower in schools that had higher spending per student
# 
# * Larger schools had lower performance in both math and reading compared to small and medium sized schools
# 
# * Charter schools performed better in both math and reading compared to district schools
# ---

# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete = school_data_complete.rename(columns={'school_name': 'School Name'})
school_data_complete.head()


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting


# calculate values
num_schools = len(school_data_complete['School Name'].unique())
num_students = school_data_complete.shape[0]
total_budget = school_data_complete['budget'].unique().sum()
avg_math_score = school_data_complete['math_score'].mean()
avg_reading_score = school_data_complete['reading_score'].mean()
comb_score = (school_data_complete['math_score'] + school_data_complete['reading_score']) / 2
passing_rate = comb_score.mean()
stu_pass_math = school_data_complete[school_data_complete['math_score'] >= 70 ]
pct_pass_math = len(stu_pass_math) / num_students * 100 
stu_pass_read = school_data_complete[school_data_complete['reading_score'] >= 70 ]
pct_pass_read = len(stu_pass_read) / num_students * 100 

# create dataframe for above results
district_summ_df = pd.DataFrame({
    "Total Schools": [num_schools], 
    "Total Students": [num_students],
    "Total Budget": [total_budget],
    "Average Math Score": [avg_math_score], 
    "Average Reading Score": [avg_reading_score],
    "% Passing Math": [pct_pass_math],
    "% Passing Reading": [pct_pass_read],
    "% Overall Passing": [passing_rate]
})
district_summ_df


# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)
#   
# * Create a dataframe to hold the above results


# create new df grouped by school name and type
school_df = school_data_complete.groupby(['School Name', 'type']).mean()
school_df = school_df.reset_index('type')

# calculate values 
school_df['Per Student Budget'] = school_df['budget'] / school_df['size']
pass_math_by_school = stu_pass_math.groupby('School Name')['math_score'].count()
pass_read_by_school = stu_pass_read.groupby('School Name')['reading_score'].count()
pct_math_by_school = pass_math_by_school / school_df['size'] * 100
pct_read_by_school = pass_read_by_school / school_df['size'] * 100

school_df['% Passing Math'] = pct_math_by_school
school_df['% Passing Reading'] = pct_read_by_school
school_df['Overall Passing Rate'] = (pct_math_by_school + pct_read_by_school) / 2

# rename columns for school_df
school_df = school_df.rename(columns={
    'type': 'School Type',
    'size': 'Total Students',
    'budget': 'Total Budget', 
    'math_score': 'Average Math Score', 
    'reading_score': 'Average Reading Score',
})

# change data type for total students
school_df['Total Students'] = school_df['Total Students'].astype(int)

# choose only columns that we need to display
school_df = school_df[['School Type', 'Total Students', 'Total Budget', 'Per Student Budget', 'Average Math Score', 'Average Reading Score', '% Passing Math', '% Passing Reading', 'Overall Passing Rate']]

school_df.head()


# ## Top Performing Schools (By Passing Rate)

# * Sort and display the top five schools in overall passing rate

sorted_descending = school_df.sort_values(by=['Overall Passing Rate'], ascending=False)
sorted_descending.head()


# ## Bottom Performing Schools (By Passing Rate)

# * Sort and display the five worst-performing schools

sorted_ascending = school_df.sort_values(by=['Overall Passing Rate'], ascending=True)
sorted_ascending.head()


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting


# create df for each grade
ninth_grade_df = school_data_complete[school_data_complete['grade'] == '9th']
tenth_grade_df = school_data_complete[school_data_complete['grade'] == '10th']
eleventh_grade_df = school_data_complete[school_data_complete['grade'] == '11th']
twelfth_grade_df = school_data_complete[school_data_complete['grade'] == '12th']

# group each grade by school name and get average values
ninth_by_school = ninth_grade_df.groupby('School Name').mean()
tenth_by_school = tenth_grade_df.groupby('School Name').mean()
eleventh_by_school = eleventh_grade_df.groupby('School Name').mean()
twelfth_by_school = twelfth_grade_df.groupby('School Name').mean()

# get math average values only
ninth_math = ninth_by_school['math_score']
tenth_math = tenth_by_school['math_score']
eleventh_math = eleventh_by_school['math_score']
twelfth_math = twelfth_by_school['math_score']

# create df for math values
grades_math_df = pd.DataFrame({
    '9th grade': ninth_math,
    '10th grade': tenth_math,
    '11th grade': eleventh_math,
    '12th grade': twelfth_math
})
grades_math_df


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores


# get reading average values only
ninth_reading = ninth_by_school['reading_score']
tenth_reading = tenth_by_school['reading_score']
eleventh_reading = eleventh_by_school['reading_score']
twelfth_reading = twelfth_by_school['reading_score']

# create df for math values
grades_math_df = pd.DataFrame({
    '9th grade': ninth_reading,
    '10th grade': tenth_reading,
    '11th grade': eleventh_reading,
    '12th grade': twelfth_reading
})
grades_math_df


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# Spending bins
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]

# split the df into bins
school_df['Spending Range'] = pd.cut(school_df['Per Student Budget'], spending_bins, labels=group_names)
spending_df = school_df.groupby("Spending Range")

spending_df = spending_df.mean()
spending_df = spending_df[['Average Math Score', 'Average Reading Score', '% Passing Math', '% Passing Reading', 'Overall Passing Rate']]
spending_df


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# School size bins
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

# split the df into bins
school_df['Size Category'] = pd.cut(school_df['Total Students'], size_bins, labels=group_names)
size_df = school_df.groupby('Size Category').mean()
size_df = size_df[['Average Math Score', 'Average Reading Score', '% Passing Math', '% Passing Reading', 'Overall Passing Rate']]
size_df


# ## Scores by School Type

# * Perform the same operations as above, based on school type.

schools_types = ['District', 'Charter']

by_type = school_df.groupby('School Type').mean()
by_type = by_type[['Average Math Score', 'Average Reading Score', '% Passing Math', '% Passing Reading', 'Overall Passing Rate']]
by_type
