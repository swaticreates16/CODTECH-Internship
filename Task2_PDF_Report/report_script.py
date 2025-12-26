import pandas as pd
from reportlab.pdfgen import canvas

# Step 1: Load data from file
data = pd.read_csv("data.csv")

# Step 2: Calculate summary metrics
average = data["Marks"].mean()
highest = data["Marks"].max()
lowest = data["Marks"].min()

# Step 3: Create PDF file
pdf = canvas.Canvas("Student_Report.pdf")

pdf.setTitle("Student Report Analysis")

pdf.drawString(50, 800, "STUDENT PERFORMANCE REPORT")
pdf.drawString(50, 780, f"Average marks: {average}")
pdf.drawString(50, 760, f"Highest marks: {highest}")
pdf.drawString(50, 740, f"Lowest marks: {lowest}")

pdf.save()

print("PDF Generated Successfully!")
