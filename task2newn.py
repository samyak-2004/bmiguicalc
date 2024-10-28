import tkinter as tk
from tkinter import font, messagebox
import csv
import matplotlib.pyplot as plt
import pandas as pd

# Function to calculate BMI
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if weight <= 0 or height <= 0:
            result_bmi.set("Invalid Input")
            result_category.set("Enter positive values")
            return
        
        bmi = weight / (height ** 2)
        category = bmi_category(bmi)
        
        result_bmi.set(f"{bmi:.2f}")
        result_category.set(category)
        
        # Save results to CSV
        save_to_csv(weight, height, bmi, category)
        
    except ValueError:
        result_bmi.set("Invalid Input")
        result_category.set("Enter numeric values")

# Function to determine BMI category
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal weight"
    elif 25 <= bmi <= 29.9:
        return "Overweight"
    else:
        return "Obese"

# Function to save records to a CSV file
def save_to_csv(weight, height, bmi, category):
    with open('bmi_records.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([weight, height, f"{bmi:.2f}", category])
    messagebox.showinfo("Record Saved", "BMI record saved successfully.")

# Function to clear all fields
def clear_fields():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_bmi.set("")
    result_category.set("")

# Function to display past records as a chart
def display_chart():
    try:
        # Load data from CSV file
        data = pd.read_csv('bmi_records.csv', names=['Weight', 'Height', 'BMI', 'Category'])
        
        # Plotting BMI distribution
        plt.figure(figsize=(10, 6))
        category_counts = data['Category'].value_counts()
        category_counts.plot(kind='barh', color='skyblue')
        plt.title("BMI Categories of Past Records")
        plt.xlabel("Count")
        plt.ylabel("Category")
        plt.show()
        
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "No records found. Please calculate BMI first.")

# Setting up the GUI
app = tk.Tk()
app.title("BMI Calculator")
app.configure(bg="powder blue")

# Custom font
custom_font = font.Font(size=35, weight="bold")

# Instructions
instructions = [
    "1. Enter your weight in kilograms.",
    "2. Enter your height in meters.",
    "3. Click 'Calculate BMI' to see your results.",
    "4. Click 'Display Chart' to view past records."
]
for i, text in enumerate(instructions):
    tk.Label(app, text=text, bg="powder blue", fg="black", font=("Arial", 20, "italic")).grid(row=i, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Labels and Entries for weight and height
tk.Label(app, text="Weight (kg):", bg="powder blue", fg="black", font=custom_font).grid(row=4, column=0, padx=10, pady=10)
weight_entry = tk.Entry(app, font=custom_font)
weight_entry.grid(row=4, column=1, padx=10, pady=10)

tk.Label(app, text="Height (m):", bg="powder blue", fg="black", font=custom_font).grid(row=5, column=0, padx=10, pady=10)
height_entry = tk.Entry(app, font=custom_font)
height_entry.grid(row=5, column=1, padx=10, pady=10)

# Variables to hold BMI result and category
result_bmi = tk.StringVar()
result_category = tk.StringVar()

# Displaying BMI result
tk.Label(app, text="BMI:", bg="powder blue", fg="black", font=custom_font).grid(row=6, column=0, padx=10, pady=10)
bmi_result_label = tk.Entry(app, textvariable=result_bmi, font=custom_font, state="readonly")
bmi_result_label.grid(row=6, column=1, padx=10, pady=10)

# Displaying BMI category
tk.Label(app, text="Category:", bg="powder blue", fg="black", font=custom_font).grid(row=7, column=0, padx=10, pady=10)
category_result_label = tk.Entry(app, textvariable=result_category, font=custom_font, state="readonly")
category_result_label.grid(row=7, column=1, padx=10, pady=10)

# Buttons for calculating BMI, clearing fields, and displaying chart
calc_button = tk.Button(app, text="Calculate BMI", command=calculate_bmi, font=custom_font, bg="powder blue", fg="black")
calc_button.grid(row=8, column=0, padx=10, pady=10)

clear_button = tk.Button(app, text="Clear", command=clear_fields, font=custom_font, bg="powder blue", fg="black")
clear_button.grid(row=8, column=1, padx=10, pady=10)

chart_button = tk.Button(app, text="Display Chart", command=display_chart, font=custom_font, bg="powder blue", fg="black")
chart_button.grid(row=9, column=0, columnspan=2, padx=10, pady=20)

# Run the application
app.mainloop()
