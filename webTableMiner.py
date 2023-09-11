import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import pyfiglet
from termcolor import colored
import sys


def scrape_tables(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")
        return [pd.read_html(str(table))[0] for table in tables]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []


def save_dataframe_to_file(dataframe, filename, file_format):
    if file_format == "csv":
        dataframe.to_csv(filename + ".csv", index=False)
        print(f"Data saved to {filename}.csv")
    elif file_format == "excel":
        dataframe.to_excel(filename + ".xlsx", index=False, engine="openpyxl")
        print(f"Data saved to {filename}.xlsx")
    else:
        print("Unsupported file format. Please use 'csv' or 'excel'.")


def select_tables_to_save(table_count, tables):
    print("Tables found on the webpage:")
    for i, table in enumerate(tables, start=1):
        print(f"Table {i}")
        print(f"Column Names:")
        for column_name in table.columns:
            print(f"  - {column_name}")

    while True:
        print(
            f"Enter table numbers to save (1-{table_count}), 'all' to save all tables, or 'exit' to exit, separated by spaces (e.g., '1 2 3' or 'all'):"
        )
        user_input = input().strip()

        if user_input.lower() == "all":
            table_numbers = list(range(1, table_count + 1))
            break
        elif user_input.lower() == "exit":
            table_numbers = []
            break
        else:
            table_numbers = [int(x) for x in user_input.split() if x.isdigit()]
            if all(1 <= num <= table_count for num in table_numbers) and table_numbers:
                break
            else:
                print("Invalid input. Please try again.")
    return table_numbers


def select_columns_interactively(dataframe, table_num):
    selected_columns = []

    print(f"Available columns for Table {table_num}:")
    columns = list(dataframe.columns)
    for i, column in enumerate(columns):
        print(f"{i + 1}. {column}")

    for column in columns:
        while True:
            print(
                f"Do you want to include the column '{column}' for Table {table_num}?"
            )
            print("1. Yes")
            print("2. No")
            print("Type 'exit' to quit.")
            include = input("Enter your choice (1/2/exit): ").strip().lower()

            if include == "1":
                selected_columns.append(column)
                break
            elif include == "2":
                break
            elif include == "exit":
                print("Exiting from the program!")
                sys.exit()
            else:
                print(
                    "Invalid input. Please choose '1' for Yes, '2' for No, or 'exit' to quit."
                )

    return selected_columns
  
def add_user_defined_columns(table_num):
    user_columns = {}

    while True:
        column_name = input(
            f"Enter the name of the new column for Table {table_num} (or 'done' to finish adding columns): "
        ).strip()

        if column_name.lower() == "done":
            break
        else:
            default_value = input(
                f"Enter the default value for column '{column_name}' for Table {table_num}: "
            ).strip()
            user_columns[column_name] = default_value

        while True:
            add_more = (
                input("Do you want to add more columns for this table? (1/2/exit): ")
                .strip()
                .lower()
            )
            if add_more == "1":
                break
            elif add_more == "2":
                return user_columns
            elif add_more == "exit":
                print("Exiting the program.")
                sys.exit()
            else:
                print("Invalid input. Please enter '1' for 'yes', '2' for 'no', or 'exit'.")
    return user_columns

def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        elif user_input == "exit":
            return None
        else:
            print("Invalid input. Please try again or enter 'exit' to exit.")


def get_valid_url():
    while True:
        url = input(
            "Enter the URL of the website with tables (or 'exit' to quit): "
        ).strip()
        if url.lower() == "exit":
            return None
        elif url:
            return url
        else:
            print("Please enter a valid URL or 'exit' to quit.")

if __name__ == "__main__":
    while True:
        banner = pyfiglet.figlet_format("WebTable\n          Miner")
        colored_banner = colored(banner, color="cyan")
        print(colored_banner)

        url = get_valid_url()

        if url:
            tables = scrape_tables(url)
            if not tables:
                print("No tables found on the webpage.")
            else:
                print(f"Found {len(tables)} table(s) on the webpage.")

                table_count = len(tables)
                table_numbers = select_tables_to_save(table_count, tables)

                if not table_numbers:
                    print("No tables selected to save.")
                else:
                    while True:
                        user_filename = input("Enter the base file name (e.g., data) or 'exit' to quit: ").strip()
                        if user_filename.lower() == 'exit':
                            print("Exiting the program.")
                            sys.exit()
                        elif user_filename:
                              
                            while True:
                              if len(table_numbers) == 1:
                                save_option='1'
                              else:
                                print("Choose how to save the data:")
                                print("1. Save all tables in a single file.")
                                print("2. Save each table in separate files.")
                                print("Type 'exit' to quit.")
                                save_option = input("Enter your choice (1/2/exit): ")

                              if save_option == '1':
                                  while True:
                                      print("Choose the file format:")
                                      print("1. CSV")
                                      print("2. Excel")
                                      print("Type 'exit' to quit.")
                                      format_option = input("Enter your choice (1/2/exit): ")

                                      if format_option == '1':
                                          file_format = 'csv'
                                          break
                                      elif format_option == '2':
                                          file_format = 'excel'
                                          break
                                      elif format_option.lower() == 'exit':
                                          print("Exiting the program.")
                                          sys.exit()
                                      else:
                                          print("Invalid format choice. Please choose '1' for CSV, '2' for Excel, or 'exit' to quit.")
                                  if file_format in ('csv', 'excel'):
                                      combined_data = []
                                      for table_num in table_numbers:
                                          selected_columns = select_columns_interactively(tables[table_num - 1], table_num)
                                          print("Do you want to add some additional columns on the table with default values:")
                                          print("1. Yes")
                                          print("2. No")
                                          print("Type 'exit' to quit.")
                                          user_columns = {}
                                          while True:
                                              is_user_want_additional_columns = input("Enter your choice (1/2/exit): ")
                                              if is_user_want_additional_columns == '1':
                                                  user_columns = add_user_defined_columns(table_num)
                                                  break
                                              elif is_user_want_additional_columns == '2':
                                                  break
                                              elif is_user_want_additional_columns == 'exit':
                                                  sys.exit()
                                              else:
                                                  print('Invalid Choice')

                                          table = tables[table_num - 1].copy()
                                          if selected_columns:
                                              table = table[selected_columns]
                                          for column, default_value in user_columns.items():
                                              table[column] = default_value

                                          combined_data.append(table)
                                      combined_data = pd.concat(combined_data, ignore_index=True)
                                      save_dataframe_to_file(combined_data, user_filename, file_format)
                                      break
                                  else:
                                      print("Invalid file format choice.")
                                      continue

                              elif save_option == '2':
                                  while True:
                                      print("Choose the file format:")
                                      print("1. CSV")
                                      print("2. Excel")
                                      print("Type 'exit' to quit.")
                                      format_option = input("Enter your choice (1/2/exit): ")

                                      if format_option == '1':
                                          file_format = 'csv'
                                          break
                                      elif format_option == '2':
                                          file_format = 'excel'
                                          break
                                      elif format_option.lower() == 'exit':
                                          print("Exiting the program.")
                                          sys.exit()
                                      else:
                                          print("Invalid format choice. Please choose '1' for CSV, '2' for Excel, or 'exit' to quit.")
                                  if file_format in ('csv', 'excel'):
                                      for table_num in table_numbers:
                                          selected_columns = select_columns_interactively(tables[table_num - 1], table_num)
                                          print("Do you want to add some additional columns on the table with default values:")
                                          print("1. Yes")
                                          print("2. No")
                                          print("Type 'exit' to quit.")
                                          user_columns = {}
                                          while True:
                                              is_user_want_additional_columns = input("Enter your choice (1/2/exit): ")
                                              if is_user_want_additional_columns == '1':
                                                  user_columns = add_user_defined_columns(table_num)
                                                  break
                                              elif is_user_want_additional_columns == '2':
                                                  break
                                              elif is_user_want_additional_columns == 'exit':
                                                  sys.exit()
                                              else:
                                                  print('Invalid Choice')

                                          table = tables[table_num - 1].copy()
                                          if selected_columns:
                                              table = table[selected_columns]
                                          for column, default_value in user_columns.items():
                                              table[column] = default_value

                                          save_dataframe_to_file(table, f"{user_filename}_Table{table_num}", file_format)
                                      print("Exiting the program.")
                                      sys.exit()
                                  else:
                                      print("Invalid file format choice.")
                                      continue

                              elif save_option.lower() == 'exit':
                                  print("Exiting the program.")
                                  sys.exit()
                              else:
                                  print("Invalid save option. Please choose '1' or '2'.")
                                  continue
                        else:
                            print("Please enter a valid base file name or 'exit' to quit.")
