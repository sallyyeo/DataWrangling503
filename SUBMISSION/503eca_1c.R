rm(list=ls())
require(RMySQL)
require(ggplot2)
require(scales)

# Connect to database
con = dbConnect(MySQL(), dbname='anl503eca')
vttclean = suppressWarnings(expr=dbReadTable(conn=con, name="vttclean"))
dbDisconnect(conn=con)

# Filter out non-student entries
student_only <- vttclean[vttclean$RegName != "INSTRUCTOR" & vttclean$RegName != "UNKNOWN",]

# Calculate total airtime for each student using sum
total_airtime_per_student <- aggregate(milliseconds ~ RegName, data = student_only, sum)

# Renaming columns
names(total_airtime_per_student) <- c("Student", "TotalMilliseconds")


# Creating the barchart with improved label positioning
ggplot(total_airtime_per_student, aes(x = reorder(Student, -TotalMilliseconds), y = TotalMilliseconds)) +
  geom_bar(stat = "identity", fill = "navy") +
  geom_text(aes(label = scales::comma(TotalMilliseconds)), # Comma as thousand separator
            position = position_nudge(y = 0.5),  # Nudge labels to the right of the bar
            hjust = -0.1,  # Adjust horizontal position to ensure labels are outside the bars
            size = 3.5,  # Text size
            color = "black") + # Text color
  theme_minimal() +
  labs(title = "Total Airtime per Student",
       x = "Student",
       y = "Total Airtime (milliseconds)") +
  scale_y_continuous(labels = label_number(big.mark = ",")) + # Scale and put comma as thousand separator
  coord_flip()  # Flipping the coordinates for better readability

