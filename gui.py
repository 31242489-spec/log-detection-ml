import tkinter as tk
import requests

# API URL
API_URL = "https://log-detection-ml-1.onrender.com/predict"

def predict():
    try:
        data = {
            "features": [
                int(ip_entry.get()),
                int(status_entry.get()),
                int(request_entry.get()),
                int(bytes_entry.get())
            ]
        }

        response = requests.post(API_URL, json=data)
        result = response.json()

        if result["prediction"] == 1:
            result_label.config(text="Malicious Activity", fg="red")
        else:
            result_label.config(text="Normal Activity", fg="green")

    except Exception as e:
        result_label.config(text="Error")

# Window
root = tk.Tk()
root.title("Log Detection GUI")

# Inputs
tk.Label(root, text="IP").grid(row=0, column=0)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1)

tk.Label(root, text="Status Code").grid(row=1, column=0)
status_entry = tk.Entry(root)
status_entry.grid(row=1, column=1)

tk.Label(root, text="Requests").grid(row=2, column=0)
request_entry = tk.Entry(root)
request_entry.grid(row=2, column=1)

tk.Label(root, text="Bytes").grid(row=3, column=0)
bytes_entry = tk.Entry(root)
bytes_entry.grid(row=3, column=1)

# Button
tk.Button(root, text="Predict", command=predict).grid(row=4, column=0, columnspan=2)

# Result
result_label = tk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2)

root.mainloop()
