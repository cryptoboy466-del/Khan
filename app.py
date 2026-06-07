import streamlit as st
import pandas as pd

# Application Configuration
st.set_page_config(page_title="EH Employee Overtime Sedra/Roshn", layout="centered")

# یہاں آپ کی نئی مین ہیڈنگ تبدیل کر دی گئی ہے
st.title("🕒 EH Employee Overtime Sedra/Roshn")
st.write("Enter your Employee Number to check your summary and overtime details.")

# The exact case-sensitive sheet name from your Excel file
EXCEL_FILE = "data.xlsx"
SHEET_NAME = "EH Staff"

try:
    # Read Excel sheet safely
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME, header=None)
    
    # Input Form for Employee Number
    with st.form(key="search_form"):
        emp_id_input = st.text_input("Enter your Employee Number:", placeholder="e.g., 220")
        submit_button = st.form_submit_button(label="Search")
        
    if submit_button:
        if emp_id_input.strip() == "":
            st.warning("Please enter a valid Employee Number.")
        else:
            search_val = emp_id_input.strip()

            # Defining column positions based on your Excel sheet layout
            # Python index starts at 0 (A=0, B=1, C=2, D=3, BR=69, BS=70)
            col_b = 1   # Employee No
            col_c = 2   # Name
            col_d = 3   # Position
            col_br = 69 # Absent / Total column
            col_bs = 70 # Overtime Total column

            # Search the employee row inside Column B (ignoring top header rows)
            matched_rows = df[df[col_b].astype(str).str.strip() == search_val]
            
            if not matched_rows.empty:
                st.success(f"Record found for Employee No. {search_val}")
                
                # Fetch row number 2 and row number 3 for descriptions
                desc_row_1 = df.iloc[1]
                desc_row_2 = df.iloc[2]
                emp_data_row = matched_rows.iloc[0]

                # Helper function to combine headers and remove ugly "nan" strings
                def make_clean_header(r1_val, r2_val, default_text):
                    part1 = str(r1_val).strip() if pd.notna(r1_val) and str(r1_val).strip().lower() != 'nan' else ""
                    part2 = str(r2_val).strip() if pd.notna(r2_val) and str(r2_val).strip().lower() != 'nan' else ""
                    
                    if part1 and part2:
                        return f"{part1} / {part2}"
                    elif part1:
                        return part1
                    elif part2:
                        return part2
                    else:
                        return default_text

                # Generate dynamic clean headers
                header_b = make_clean_header(desc_row_1[col_b], desc_row_2[col_b], "FILE #")
                header_c = make_clean_header(desc_row_1[col_c], desc_row_2[col_c], "EMPLOYEE NAME")
                header_d = make_clean_header(desc_row_1[col_d], desc_row_2[col_d], "POSITION")
                header_br = make_clean_header(desc_row_1[col_br], desc_row_2[col_br], "TOTAL ABSENT")
                header_bs = make_clean_header(desc_row_1[col_bs], desc_row_2[col_bs], "TOTAL OVERTIME")

                # Creating a custom clean dictionary for the screen
                summary_table = {
                    header_b: [emp_data_row[col_b]],
                    header_c: [emp_data_row[col_c]],
                    header_d: [emp_data_row[col_d]],
                    header_br: [emp_data_row[col_br]],
                    header_bs: [emp_data_row[col_bs]]
                }
                
                # Convert to DataFrame to print nicely
                final_df = pd.DataFrame(summary_table)
                
                # Display the clean filtered card data instantly
                st.dataframe(final_df, use_container_width=True, hide_index=True)
                
            else:
                st.error(f"Employee Number '{search_val}' not found in '{SHEET_NAME}' sheet. Please verify.")

except FileNotFoundError:
    st.error(f"Error: Excel file '{EXCEL_FILE}' not found in the directory.")
except ValueError as ve:
    st.error(f"Sheet Error: {ve}")
except Exception as e:
    st.error(f"An error occurred: {e}")