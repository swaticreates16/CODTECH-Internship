# Import required libraries
import pandas as pd
from reportlab.pdfgen import canvas

# This CSV file should contain student data with a column named "Marks"
data = pd.read_csv("data.csv")

# Calculate average, highest and lowest marks
average = data["Marks"].mean()
highest = data["Marks"].max()
lowest = data["Marks"].min()

# Create a new PDF document
pdf = canvas.Canvas("Student_Report.pdf")

# Set the title of the PDF
pdf.setTitle("Student Report Analysis")

# Write data into the PDF

pdf.drawString(50, 800, "STUDENT PERFORMANCE REPORT")
pdf.drawString(50, 780, f"Average marks: {average}")
pdf.drawString(50, 760, f"Highest marks: {highest}")
pdf.drawString(50, 740, f"Lowest marks: {lowest}")

# Save the PDF file
pdf.save()

# Final message in terminal
print("PDF Generated Successfully!")
