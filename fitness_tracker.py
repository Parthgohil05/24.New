import numpy as np
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Initialize empty DataFrames
workouts = pd.DataFrame(columns=['Date', 'Workout Type', 'Duration (min)', 'Calories Burned'])
nutrition = pd.DataFrame(columns=['Date', 'Food Item', 'Calories Consumed'])

# List of vegetarian food items
vegetarian_foods = {
    'Oatmeal': 150,
    'Vegetable Stir Fry': 250,
    'Fruit Salad': 200,
    'Vegetable Soup': 100,
    'Pasta Primavera': 400,
    'Grilled Cheese Sandwich': 300,
    'Vegetable Curry': 350,
    'Lentil Soup': 250,
    'Greek Salad': 200
}

# Function to log a workout
def log_workout(date, workout_type, duration, calories_burned):
    global workouts
    new_entry = pd.DataFrame([{
        'Date': date,
        'Workout Type': workout_type,
        'Duration (min)': duration,
        'Calories Burned': calories_burned
    }])
    workouts = pd.concat([workouts, new_entry], ignore_index=True)

# Function to log nutrition
def log_nutrition(date, food_item):
    if food_item not in vegetarian_foods:
        messagebox.showerror("Error", f"{food_item} is not a vegetarian option.")
        return
    global nutrition
    new_entry = pd.DataFrame([{
        'Date': date,
        'Food Item': food_item,
        'Calories Consumed': vegetarian_foods[food_item]
    }])
    nutrition = pd.concat([nutrition, new_entry], ignore_index=True)

# Function to calculate total calories burned
def total_calories_burned():
    return workouts['Calories Burned'].sum()

# Function to calculate total calories consumed
def total_calories_consumed():
    return nutrition['Calories Consumed'].sum()

# Function to generate summary
def generate_summary(period='weekly'):
    end_date = datetime.now()
    if period == 'weekly':
        start_date = end_date - pd.Timedelta(weeks=1)
    elif period == 'monthly':
        start_date = end_date - pd.Timedelta(days=30)
    
    recent_workouts = workouts[workouts['Date'] >= start_date.strftime('%Y-%m-%d')]
    recent_nutrition = nutrition[nutrition['Date'] >= start_date.strftime('%Y-%m-%d')]
    
    summary = {
        'Total Calories Burned': recent_workouts['Calories Burned'].sum(),
        'Total Calories Consumed': recent_nutrition['Calories Consumed'].sum(),
        'Workouts': recent_workouts,
        'Nutrition': recent_nutrition
    }
    return summary

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Personal Fitness Tracker")
    root.geometry("800x600")
    root.configure(bg='#f0f0f0')

    # Title Label
    title_label = tk.Label(root, text="Personal Fitness Tracker", font=("Arial", 24), bg='#f0f0f0')
    title_label.pack(pady=20)

    # Workout Frame
    workout_frame = tk.LabelFrame(root, text="Log Workout", padx=10, pady=10, bg='#d9e4dd', font=("Arial", 14))
    workout_frame.pack(padx=20, pady=10, fill="x")

    tk.Label(workout_frame, text="Date (YYYY-MM-DD):", bg='#d9e4dd').grid(row=0, column=0, padx=5, pady=5)
    tk.Label(workout_frame, text="Workout Type:", bg='#d9e4dd').grid(row=0, column=1, padx=5, pady=5)
    tk.Label(workout_frame, text="Duration (min):", bg='#d9e4dd').grid(row=0, column=2, padx=5, pady=5)
    tk.Label(workout_frame, text="Calories Burned:", bg='#d9e4dd').grid(row=0, column=3, padx=5, pady=5)

    workout_date_entry = tk.Entry(workout_frame)
    workout_type_entry = tk.Entry(workout_frame)
    workout_duration_entry = tk.Entry(workout_frame)
    workout_calories_entry = tk.Entry(workout_frame)

    workout_date_entry.grid(row=1, column=0, padx=5, pady=5)
    workout_type_entry.grid(row=1, column=1, padx=5, pady=5)
    workout_duration_entry.grid(row=1, column=2, padx=5, pady=5)
    workout_calories_entry.grid(row=1, column=3, padx=5, pady=5)

    def add_workout():
        date = workout_date_entry.get()
        workout_type = workout_type_entry.get()
        duration = int(workout_duration_entry.get())
        calories = int(workout_calories_entry.get())
        log_workout(date, workout_type, duration, calories)
        messagebox.showinfo("Success", "Workout logged successfully!")
        workout_date_entry.delete(0, tk.END)
        workout_type_entry.delete(0, tk.END)
        workout_duration_entry.delete(0, tk.END)
        workout_calories_entry.delete(0, tk.END)

    add_workout_button = tk.Button(workout_frame, text="Add Workout", command=add_workout, bg='#a4c3b2')
    add_workout_button.grid(row=1, column=4, padx=5, pady=5)

    # Nutrition Frame
    nutrition_frame = tk.LabelFrame(root, text="Log Nutrition", padx=10, pady=10, bg='#d9e4dd', font=("Arial", 14))
    nutrition_frame.pack(padx=20, pady=10, fill="x")

    tk.Label(nutrition_frame, text="Date (YYYY-MM-DD):", bg='#d9e4dd').grid(row=0, column=0, padx=5, pady=5)
    tk.Label(nutrition_frame, text="Food Item:", bg='#d9e4dd').grid(row=0, column=1, padx=5, pady=5)

    nutrition_date_entry = tk.Entry(nutrition_frame)
    food_item_entry = tk.Entry(nutrition_frame)

    nutrition_date_entry.grid(row=1, column=0, padx=5, pady=5)
    food_item_entry.grid(row=1, column=1, padx=5, pady=5)

    def add_nutrition():
        date = nutrition_date_entry.get()
        food_item = food_item_entry.get()
        log_nutrition(date, food_item)
        messagebox.showinfo("Success", "Nutrition logged successfully!")
        nutrition_date_entry.delete(0, tk.END)
        food_item_entry.delete(0, tk.END)

    add_nutrition_button = tk.Button(nutrition_frame, text="Add Nutrition", command=add_nutrition, bg='#a4c3b2')
    add_nutrition_button.grid(row=1, column=2, padx=5, pady=5)

    # Summary Frame
    summary_frame = tk.LabelFrame(root, text="Summary", padx=10, pady=10, bg='#d9e4dd', font=("Arial", 14))
    summary_frame.pack(padx=20, pady=10, fill="x")

    def show_summary():
        for item in workout_tree.get_children():
            workout_tree.delete(item)
        for item in nutrition_tree.get_children():
            nutrition_tree.delete(item)
        
        period = period_var.get()
        summary = generate_summary(period)

        summary_label.config(text=(
            f"Total Calories Burned: {summary['Total Calories Burned']}\n"
            f"Total Calories Consumed: {summary['Total Calories Consumed']}\n"
        ))

        for index, row in summary['Workouts'].iterrows():
            workout_tree.insert("", tk.END, values=row.tolist())
        
        for index, row in summary['Nutrition'].iterrows():
            nutrition_tree.insert("", tk.END, values=row.tolist())

    period_var = tk.StringVar(value='weekly')
    tk.Radiobutton(summary_frame, text="Weekly", variable=period_var, value='weekly', bg='#d9e4dd').grid(row=0, column=0, padx=5, pady=5)
    tk.Radiobutton(summary_frame, text="Monthly", variable=period_var, value='monthly', bg='#d9e4dd').grid(row=0, column=1, padx=5, pady=5)

    summary_button = tk.Button(summary_frame, text="Show Summary", command=show_summary, bg='#a4c3b2')
    summary_button.grid(row=0, column=2, padx=5, pady=5)

    summary_label = tk.Label(summary_frame, text="", bg='#d9e4dd', justify=tk.LEFT, font=("Arial", 12))
    summary_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    # Workout Treeview
    workout_tree = ttk.Treeview(summary_frame, columns=('Date', 'Workout Type', 'Duration (min)', 'Calories Burned'), show='headings')
    workout_tree.heading('Date', text='Date')
    workout_tree.heading('Workout Type', text='Workout Type')
    workout_tree.heading('Duration (min)', text='Duration (min)')
    workout_tree.heading('Calories Burned', text='Calories Burned')
    workout_tree.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

    # Nutrition Treeview
    nutrition_tree = ttk.Treeview(summary_frame, columns=('Date', 'Food Item', 'Calories Consumed'), show='headings')
    nutrition_tree.heading('Date', text='Date')
    nutrition_tree.heading('Food Item', text='Food Item')
    nutrition_tree.heading('Calories Consumed', text='Calories Consumed')
    nutrition_tree.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    root.mainloop()

create_gui()
