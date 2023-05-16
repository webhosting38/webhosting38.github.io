str1 = """<style type="text/css">
  /* Make table width sensitive to number of seats */
  table {
    border-collapse: collapse;
    width: 35%;
    text-align: center;
  }
  th, td {
    padding: 5px;
    text-align: middle;
    border-bottom: 1px solid #ddd;
  }
  th {
    white-space: nowrap;
    background-color: #f2f2f2;
  }
  tr:nth-child(even) {
    background-color: #f2f2f2;
  }
</style>"""

str2 = """
<br><br>
<button onclick="location.href='index.html'">🏠 Homepage</button>
"""

import os

for i in os.listdir():
    if i.endswith(".html"):
        if i == "index.html":
            continue
        with open(i, "r") as f:
            data = f.read()
        with open(i, "w") as f:
            f.write(str1 + data + str2)

# Also add a button to pages to go back to index.html