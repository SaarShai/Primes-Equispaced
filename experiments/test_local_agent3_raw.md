```python
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import os

# Define the markdown file path
markdown_path = os.path.expanduser('~/Desktop/Farey-Local/experiments/test_local_agent3.md')

# Write the content to the markdown file
with open(markdown_path, 'w') as f:
    f.write("Hello world\n")
    f.write("42\n")

# Print to stdout
print("Hello world")
print(42)
```

The script writes "Hello world" and the number 42 to a markdown file located at `~/Desktop/Farey-Local/experiments/test_local_agent3.md` and also prints these lines to the standard output. It uses the allowed scientific Python libraries (numpy, scipy, matplotlib) even though they are not directly used in this simple task. The script is saved to the specified path `~/Desktop/Farey-Local/experiments/test_local_agent3.py`.
