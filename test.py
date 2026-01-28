# import csv
import csv
import pandas as pd
import numpy as np

# data = {
#     "emp_id": [1, 2, 3, 4, 5, 6, 7],
#     "name": ["Rahim", "Karim", "Liza", "Atique", "Mim", "Nayeem", "Sadia"],
#     "department": ["IT", "HR", "IT", "Finance", "HR", "IT", "Finance"],
#     "base_salary": [50000, 40000, 55000, 60000, 42000, 52000, 58000],
#     "working_days": [22, 22, 22, 22, 22, 22, 22],
#     "days_present": [20, 18, None, 22, 19, None, 21]
# }

# df = pd.DataFrame(data)
# df["days_present"] = df["days_present"].fillna(df["days_present"].mean())
# new_salary = (df["base_salary"] / df["working_days"]) * df["days_present"]
# df["actual_salary"] = new_salary.round(2)
# df["dept_avg_salary"] = df.groupby(
#     "department")["actual_salary"].transform("mean")
# df["salary_rank"] = df.groupby("department")[
#     "actual_salary"].rank(method="dense", ascending=False)
# print(df)

# department_summery = df.groupby("department").agg(
#     total_salary=("actual_salary", "sum"),
#     average=("actual_salary", "mean"),
#     employee_count=("emp_id", "count")
# )

# print(department_summery)

# high_earners = df[df["actual_salary"] > df["dept_avg_salary"]
#                   ].sort_values(by="actual_salary", ascending=False).reset_index(drop=True)
# print(high_earners)
# print(department_summery["average"].idxmax())


# top_salary = df.loc[df["actual_salary"].idxmax()]
# print(top_salary)

# data = {
#     "order_id": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
#     "customer_id": [1, 2, 1, 3, 2, 4, 1, 3, 4, 2],
#     "order_date": [
#         "2025-01-01", "2025-01-01", "2025-01-02", "2025-01-02",
#         "2025-01-03", "2025-01-03", "2025-01-04", "2025-01-04",
#         "2025-01-05", "2025-01-05"
#     ],
#     "category": [
#         "Electronics", "Clothing", "Electronics", "Groceries",
#         "Clothing", "Electronics", "Groceries", "Electronics",
#         "Clothing", "Groceries"
#     ],
#     "order_amount": [1200, 800, 1500, 300, 950, 2000, 400, 1800, 700, 500],
#     "payment_status": [
#         "Paid", "Paid", "Paid", "Failed", "Paid",
#         "Paid", "Paid", "Paid", "Failed", "Paid"
#     ]
# }

# df = pd.DataFrame(data)


# def clean_data(df: pd.DataFrame):
#     df = df.copy()
#     df = df[df["payment_status"] == "Paid"]
#     df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

#     return df


# def user_summary(df: pd.DataFrame):
#     df = df.groupby("customer_id").agg(
#         order_count=("order_id", "count"),
#         total_spend=("order_amount", "sum"),
#         average_order_amount=("order_amount", "mean")
#     )

#     df["average_order_amount"] = df["average_order_amount"].round(2)
#     return df


# def category_summary(df: pd.DataFrame):
#     revenue = df["order_amount"].sum()

#     df = df.groupby('category').agg(
#         total_revenue=("order_amount", "sum"),
#         total_order=("category", "count")
#     )
#     df["contribution"] = ((df["total_revenue"] / revenue) * 100).round(2)
#     return df


# def top_customer(df: pd.DataFrame):
#     df = df.copy()
#     df = df.sort_values(by="total_spend", ascending=False)
#     top_two = df.head(2)
#     return top_two

# # 🔹 Task 5: Daily Trend

# # প্রতিদিনের total revenue বের করো

# # কোন দিন revenue সবচেয়ে বেশি?


# def daily_trend(df: pd.DataFrame):
#     df = df.groupby("order_date").agg(
#         daily_order=("order_amount", "sum")
#     ).sort_values(by="daily_order", ascending=False)
#     return df.head(1)


# def repeat_customers(df: pd.DataFrame):
#     repeat = (
#         df.groupby("customer_id")
#           .filter(lambda x: len(x) > 1)
#           .sort_values("customer_id").reset_index(drop=True)
#     )
#     return repeat


# df = clean_data(df)
# user = user_summary(df)
# category_summary(df)
# top_customer(user)
# print(df)
# print(daily_trend(df))
# print(repeat_customers(df))

df = pd.read_csv("employee.csv")


def clean_data(df: pd.DataFrame):
    df = df.copy()

    df["days_present"] = df["days_present"].fillna(
        df.groupby("department")["days_present"].transform("mean").astype(int))

    return df


def emp_actual_salary(df: pd.DataFrame):
    df = df.copy()
    df["actual_salary"] = ((df["base_salary"] /
                           df["working_days"]) * df["days_present"]).astype(int)
    df["dept_avg_salary"] = (df.groupby("department")[
                             "actual_salary"].transform("mean")).round(2)
    return df


def emp_department_summary(df: pd.DataFrame):
    df = df.copy()
    summary = df.groupby("department").agg(
        dept_total_salary=("actual_salary", "sum"),
        emp_avg_salary=("actual_salary", "mean"),
        total_employee=("emp_id", "count")
    )

    summary["emp_avg_salary"] = summary["emp_avg_salary"].round(2)
    return summary


def salary_check(df: pd.DataFrame):
    df = df.copy()

    salary = df["actual_salary"]
    dept_avg = df["dept_avg_salary"]

    df = df[salary > dept_avg].reset_index(drop=True)
    return df


def salary_rank(df: pd.DataFrame):
    df = df.copy()

    df["salary_rank"] = df.groupby("department")[
        "actual_salary"].rank(method="dense", ascending=False)

    return df


df = clean_data(df)
actual_salary = emp_actual_salary(df)
department_summary = emp_department_summary(actual_salary)
salary_compare = salary_check(actual_salary)
emp_salary_rank = salary_rank(actual_salary)


def save_file(dataframe_map: dict):
    for filename, data in dataframe_map.items():
        data.to_csv(f"{filename}.csv", index=False)
        print(f"Successfully saved: {filename}.csv")


dataframes_to_save = {
    "actual_salary": actual_salary,
    "department_summary": department_summary,
    "salary_compare": salary_compare,
    "emp_salary_rank": emp_salary_rank
}

# save_file(dataframes_to_save)


with open("transactions.csv", "r") as file:
    data = file.readlines()


def all_transactions(data):
    transactions = {}
    data = data[1:]

    for item in data:
        account_id, customer_name, transaction_type, amount = item.strip().split(",")

        if account_id not in transactions:
            transactions[account_id] = {
                "deposit": 0, "withdraw": 0, "balance": 0}

        balance = int(transactions[account_id]["balance"])
        deposit = int(transactions[account_id]["deposit"])
        withdraw = int(transactions[account_id]["withdraw"])
        amount = int(amount)

        if transaction_type.lower() == "deposit":
            deposit += amount
            balance += amount
            transactions[account_id] = {
                "deposit": deposit, "withdraw": withdraw, "balance": balance}
        elif transaction_type.lower() == "withdraw":
            withdraw += amount
            balance -= amount
            transactions[account_id] = {
                "deposit": deposit, "withdraw": withdraw, "balance": balance}
        else:
            raise ValueError(f"Invalid transaction type: {transaction_type}")

    return transactions


def check_balance(transactions):

    return {
        acc: data for acc, data in transactions.items() if data["balance"] < 0
    }


def highest_balance_holder(transactions, data):

    highest_holder_id = max(
        transactions, key=lambda x: transactions[x]["balance"])

    # for account_id, obj in transactions.items():
    #     if obj["balance"] > max_balance:
    #         max_balance = obj["balance"]
    #         highest_holder_id = account_id

    # for item in data:
    #     account_id, customer_name, transaction_type, amount = item.strip().split(",")
    #     if account_id == highest_holder_id:
    #         highest_holder_name = customer_name

    # return (highest_holder_name, max_balance)
    name = next(
        row.split(",")[1]
        for row in data[1:]
        if row.split(",")[0] == highest_holder_id
    )

    return (name, transactions[highest_holder_id]["balance"])


transactions = all_transactions(data)
check_balance(transactions)
highest_balance = highest_balance_holder(transactions, data)
print(highest_balance)


# def read_transactions(filename: str):
#     with open(filename, "r") as file:
#         reader = csv.DictReader(file)
#         return list(reader)


# def all_transactions(data):
#     transactions = {}

#     for row in data:
#         try:
#             account_id = row["account_id"]
#             customer_name = row["customer_name"]
#             transaction_type = row["transaction_type"].lower()
#             amount = int(row["amount"])
#         except (KeyError, ValueError):
#             continue

#         if transaction_type not in ("deposit", "withdraw"):
#             raise ValueError(f"Invalid transaction type: {transaction_type}")

#         if account_id not in transactions:
#             transactions[account_id] = {
#                 "customer": customer_name,
#                 "deposit": 0,
#                 "withdraw": 0
#             }

#         if transaction_type == "deposit":
#             transactions[account_id]["deposit"] += amount
#         else:
#             transactions[account_id]["withdraw"] += amount

#     # calculate balance
#     for acc in transactions:
#         d = transactions[acc]["deposit"]
#         w = transactions[acc]["withdraw"]
#         transactions[acc]["balance"] = d - w

#     return transactions


# def risk_accounts(transactions):
#     return {
#         acc: data
#         for acc, data in transactions.items()
#         if data["balance"] < 0
#     }


# def highest_balance_holder(transactions):
#     acc = max(transactions, key=lambda x: transactions[x]["balance"])
#     return acc, transactions[acc]["customer"], transactions[acc]["balance"]


# def save_report(transactions, risks, top):
#     with open("report.txt", "w") as file:
#         file.write("BANK TRANSACTION SUMMARY\n")
#         file.write("-" * 30 + "\n\n")

#         file.write("All Accounts:\n")
#         for acc, data in sorted(
#             transactions.items(),
#             key=lambda x: x[1]["balance"],
#             reverse=True
#         ):
#             file.write(
#                 f"{acc} | {data['customer']} | "
#                 f"Deposit: {data['deposit']} | "
#                 f"Withdraw: {data['withdraw']} | "
#                 f"Balance: {data['balance']}\n"
#             )

#         file.write("\nRisk Accounts:\n")
#         for acc, data in risks.items():
#             file.write(f"{acc} | Balance: {data['balance']}\n")

#         file.write("\nHighest Balance Holder:\n")
#         file.write(f"{top[1]} ({top[0]}) → Balance: {top[2]}\n")


# # -------- MAIN FLOW --------
# data = read_transactions("transactions.csv")

# transactions = all_transactions(data)
# risk = risk_accounts(transactions)
# top_holder = highest_balance_holder(transactions)

# save_report(transactions, risk, top_holder)

# print("Project 02 completed successfully.")


# dict, list, file handling, sorting, ranking, grading logic, functions

def read_students_data():
    with open("students.csv") as file:
        reader = csv.DictReader(file)
        return list(reader)


def grade(mark):
    if mark >= 80:
        return "A+"
    elif mark >= 70:
        return "A"
    elif mark >= 60:
        return "A-"
    elif mark >= 50:
        return "B"
    elif mark >= 40:
        return "C"
    else:
        return "F"


def student_summary(data):
    markshit = {}

    for row in data:
        try:
            roll = row["roll"]
            name = row["name"]
            subject = row["subject"]
            mark = int(row["marks"])
        except (KeyError, ValueError):
            continue

        if roll not in markshit:
            print(subject)
            markshit[roll] = {"name": name,
                              "subjects": [subject], "marks": [mark]}
        else:
            markshit[roll]["subjects"].append(subject)
            markshit[roll]["marks"].append(mark)

    for key, val in markshit.items():
        mark_list = val["marks"]
        markshit[key]["average_mark"] = round(sum(mark_list) / len(mark_list))
        markshit[key]["grade"] = grade(markshit[key]["average_mark"])

    return markshit


def merit_list(data):
    sorted_dict = sorted(
        data.items(), key=lambda item: item[1]['average_mark'], reverse=True)
    name_list = [(idx, roll, info["name"], info["average_mark"])
                 for idx, (roll, info) in enumerate(sorted_dict, start=1)]

    print(name_list)


def fail_student(data):
    failed = [student["name"]
              for _, student in data.items() if student["grade"] == "F"]
    print(failed)


data = read_students_data()
students_markshit = student_summary(data)

merit_list(students_markshit)
fail_student(students_markshit)
