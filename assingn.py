import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to load Excel file
def load_excel_file(file_path):
    try:
        df = pd.ExcelFile(file_path)
        print("Sheets available:", df.sheet_names)
        return df
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None

# Function to parse datasets
def parse_datasets(df):
    UserDetails = df.parse('UserDetails.csv')
    CookingSessions = df.parse('CookingSessions.csv')
    OrderDetails = df.parse('OrderDetails.csv')
    return UserDetails, CookingSessions, OrderDetails

# Function to handle missing values
def handle_missing_values(df):
    df['Rating'] = df['Rating'].fillna(0)
    return df

# Function to merge datasets
def merge_datasets(CookingSessions, OrderDetails):
    return pd.merge(CookingSessions, OrderDetails, on=['Session ID', 'User ID'], how='inner')

# Function to analyze relationships
def analyze_relationships(merged_data):
    relationships = merged_data.groupby(['Dish Name_x', 'Meal Type_x']).agg({
        'Order ID': 'count',
        'Amount (USD)': 'sum',
    }).reset_index()
    relationships.rename(columns={
        'Dish Name_x': 'Dish Name',
        'Meal Type_x': 'Meal Type',
        'Order ID': 'Total Orders',
        'Amount (USD)': 'Total Revenue'
    }, inplace=True)
    return relationships

# Function to find popular dishes
def find_popular_dishes(OrderDetails):
    popular_dishes = OrderDetails.groupby('Dish Name').agg({
        'Order ID': 'count',
        'Amount (USD)': 'sum'
    }).reset_index()
    popular_dishes.rename(columns={
        'Order ID': 'Total Orders',
        'Amount (USD)': 'Total Revenue'
    }, inplace=True)
    return popular_dishes

# Function to plot pie chart
def plot_pie_chart(popular_dishes):
    top_dishes = popular_dishes.head(5)
    plt.pie(top_dishes['Total Revenue'], labels=top_dishes['Dish Name'], explode=[0, 0, 0, 0, 0.1],
            shadow=True, colors=["yellow", "hotpink", "green", "cyan", "Lavender"],
            autopct="%0.2f%%", wedgeprops={'linewidth': 3, 'edgecolor': "k"}, startangle=90)
    plt.legend(title="Dish Name")
    plt.title("Top 5 Dishes by Revenue", fontsize=16, fontweight='bold', color='teal')
    plt.show()

# Function to plot bar chart
def plot_bar_chart(popular_dishes):
    top_dishes = popular_dishes.head(5)
    plt.figure(figsize=(8, 5))
    plt.bar(top_dishes['Dish Name'], top_dishes['Total Revenue'], width=0.5, color="purple", edgecolor="black", linewidth=1.5)
    plt.xlabel("Dish Name", color="green", fontsize=12)
    plt.ylabel("Total Revenue (USD)", color="red", fontsize=12)
    plt.title("Total Revenue by Dish", color="g", fontsize=14, fontweight="bold")
    plt.show()

def plot_cooking_sessions_orders():
    # Sample data for Cooking Sessions and Orders Relationship
    dish_names = ["Caesar Salad", "Grilled Chicken", "Oatmeal", "Pancakes", "Spaghetti", "Veggie Burger"]
    total_orders = [3, 4, 1, 2, 4, 2]
    total_revenue = [28.0, 51.0, 7.0, 16.5, 55.5, 22.0]
    
    plt.figure(figsize=(10, 6))
    plt.bar(dish_names, total_orders, color='hotpink', width=0.5, edgecolor="black", linewidth=1.5)
    plt.title('Cooking Sessions and Orders Relationship', fontsize=14)
    plt.xlabel('Dish Name', fontsize=12)
    plt.ylabel('Total Orders', fontsize=12)
    plt.show()

# Main loop
file_path = "C:\\Users\\lenovo\\Downloads\\Assignment.xlsx"
df = load_excel_file(file_path)
if df:
    UserDetails, CookingSessions, OrderDetails = parse_datasets(df)
    OrderDetails = handle_missing_values(OrderDetails)
    merged_data = merge_datasets(CookingSessions, OrderDetails)

    while True:
        print("\nChoose an option:")
        print("1. Analyze relationships between Cooking Sessions and Orders")
        print("2. Identify popular dishes")
        print("3. Plot pie chart for top dishes")
        print("4. Plot bar chart for total revenue")
        print("5. Plot bar chart for Cooking Sessions orders")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            relationships = analyze_relationships(merged_data)
            print(relationships)
            
        elif choice == '2':
            popular_dishes = find_popular_dishes(OrderDetails)
            print(popular_dishes.sort_values(by='Total Orders', ascending=False))
            
        elif choice == '3':
            popular_dishes = find_popular_dishes(OrderDetails)
            plot_pie_chart(popular_dishes)
            
        elif choice == '4':
            popular_dishes = find_popular_dishes(OrderDetails)
            plot_bar_chart(popular_dishes)

        elif choice == '5':
            plot_cooking_sessions_orders()
            
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
