# KNIME Node Maker

A friendly, interactive script that generates ready-to-use [KNIME](https://www.knime.com/) node extension projects — no boilerplate writing required. Answer a few questions, and you get a complete project folder you can open, edit, and load straight into KNIME Analytics Platform.

---

## Table of Contents

1. [What Is This?](#what-is-this)
2. [What Is KNIME?](#what-is-knime)
3. [What Does This Script Actually Do?](#what-does-this-script-actually-do)
4. [Prerequisites](#prerequisites)
5. [How to Run the Script](#how-to-run-the-script)
6. [Walkthrough of the Questions](#walkthrough-of-the-questions)
7. [What Gets Generated](#what-gets-generated)
8. [How to Load Your Node into KNIME](#how-to-load-your-node-into-knime)
9. [Editing Your Node Logic](#editing-your-node-logic)
10. [Full Example: Start to Finish](#full-example-start-to-finish)
11. [Glossary](#glossary)
12. [Troubleshooting](#troubleshooting)
13. [Resources](#resources)

---

## What Is This?

When you want to create a custom node for KNIME, you normally have to set up several files by hand — a Python file with specific decorators and class structures, a YAML metadata file, a dependency file, and so on. It's tedious and easy to get wrong.

This script automates all of that. You run it, answer some plain-English questions about the node you want to build, and it spits out a complete project folder that is ready to develop in.

Think of it like a "new project" wizard, but in your terminal.

---

## What Is KNIME?

[KNIME Analytics Platform](https://www.knime.com/knime-analytics-platform) is a free, open-source tool for building data workflows visually. Instead of writing code from scratch, you drag and drop "nodes" onto a canvas and connect them together — like building blocks for data.

Each node does one job: read a CSV, filter rows, train a model, make a chart, etc. KNIME ships with thousands of built-in nodes, but sometimes you need one that does something specific to your work. That's where custom nodes come in, and that's what this script helps you create.

---

## What Does This Script Actually Do?

`create_knime_node.py` is an interactive command-line tool. When you run it:

1. It asks you a series of questions (node name, what it does, how many inputs/outputs, etc.).
2. It generates a complete project folder containing all the files KNIME needs.
3. You then open the generated Python file, write your actual logic (the interesting part), and load it into KNIME.

The script itself does **not** require KNIME to be installed. It just creates files. You only need KNIME later, when you want to actually use the node.

---

## Prerequisites

You need two things installed on your computer:

### 1. Python (version 3.8 or newer)

Python is the programming language the script is written in. Most Macs and Linux machines already have it. To check, open a terminal and type:

```bash
python3 --version
```

If you see something like `Python 3.11.5`, you're good. If not, download it from [python.org](https://www.python.org/downloads/).

### 2. pixi (for later, when you develop your node)

[pixi](https://pixi.sh) is a package manager that KNIME's Python extension system uses to manage dependencies. You don't need it to *run this script*, but you will need it to *develop and test* the node it generates.

Install pixi:

- **macOS / Linux:**
  ```bash
  curl -fsSL https://pixi.sh/install.sh | sh
  ```
- **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
  ```

After installing, restart your terminal so the `pixi` command becomes available.

---

## How to Run the Script

1. Open a terminal (Terminal on Mac, Command Prompt or PowerShell on Windows, or any terminal on Linux).

2. Navigate to the folder where you downloaded/cloned this repository:
   ```bash
   cd path/to/knime-node-maker
   ```

3. Run the script:
   ```bash
   python3 create_knime_node.py
   ```

4. Answer the questions that appear. Each question shows a default value in square brackets — just press Enter to accept the default, or type your own answer.

5. When it finishes, you'll see a message telling you where your new project folder was created.

---

## Walkthrough of the Questions

Here is every question the script asks, what it means, and what to type.

### Extension metadata

| Question | What it means | Example answer |
|---|---|---|
| **Extension ID** | A unique identifier for your extension, usually in reverse-domain style. | `com.mycompany.texttools` |
| **Extension display name** | The human-readable name shown in KNIME. | `Text Processing Tools` |
| **Extension description** | A short sentence about what your extension does. | `Nodes for cleaning and transforming text data` |
| **Author** | Your name or your team's name. | `Jane Smith` |
| **Node category ID** | A short, no-spaces identifier used internally. | `texttools` |
| **Node category display name** | The name of the folder your node appears in inside KNIME's node repository. | `Text Tools` |

### Node details

| Question | What it means | Example answer |
|---|---|---|
| **Node name** | The name of the node as it appears on the KNIME canvas. | `Remove Stopwords` |
| **Node description** | A sentence explaining what the node does. Users see this in KNIME's node description panel. | `Removes common stopwords from a text column.` |
| **Node type** | What kind of node this is (see table below). Pick a number. | `1` |

#### Node types explained

| # | Type | When to use it |
|---|---|---|
| 1 | **Manipulator** | Your node takes data in, changes it, and passes it out. This is the most common type. |
| 2 | **Learner** | Your node trains a machine-learning model. |
| 3 | **Predictor** | Your node uses a trained model to make predictions. |
| 4 | **Source** | Your node creates or fetches data from somewhere (a file, an API, a database). It has no data input. |
| 5 | **Sink** | Your node saves or sends data somewhere. It has no data output. |
| 6 | **Visualizer** | Your node creates a chart or visual. |
| 7 | **Other** | None of the above fit. |

### Ports (inputs and outputs)

| Question | What it means | Example answer |
|---|---|---|
| **Number of input tables** | How many data tables flow *into* your node. Most nodes have 1. | `1` |
| **Number of output tables** | How many data tables flow *out of* your node. Most nodes have 1. | `1` |
| **Include an output view?** | Should the node produce a visual (chart, HTML, etc.) in addition to table data? | `n` (or `y`) |

### Dialog parameters

These are the settings a user can configure when they double-click your node in KNIME. You can add as many as you want. Press Enter with a blank name to stop adding.

| Question | What it means | Example answer |
|---|---|---|
| **Parameter name** | The label the user sees in the settings dialog. | `Text Column` |
| **Type** | The kind of input control (see table below). | `column` |
| **Description** | Help text shown next to the setting. | `The column containing text to process` |
| **Default value** | The pre-filled value (not asked for column-type parameters). | `hello` |

#### Parameter types explained

| Type | What it creates in the dialog | Good for |
|---|---|---|
| `string` | A text box | Free-form text input |
| `int` | A number spinner (whole numbers) | Counts, thresholds, limits |
| `double` | A number spinner (decimal numbers) | Percentages, weights, tolerances |
| `bool` | A checkbox | On/off toggles |
| `column` | A dropdown listing columns from the input table | Picking a single column to operate on |
| `multicolumn` | A multi-select list of columns | Picking several columns |
| `columnfilter` | A full column filter widget | Advanced include/exclude column selection |

### Output directory

| Question | What it means | Example answer |
|---|---|---|
| **Output directory** | The folder name where the project will be created (relative to where you ran the script). | `my_text_tools` |

---

## What Gets Generated

After answering all the questions, you'll find a new folder with this structure:

```
my_text_tools/
├── icons/
│   └── icon.png              ← Placeholder icon (replace with your own 16×16 PNG)
├── src/
│   └── extension.py          ← The main file — your node's code lives here
├── knime.yml                 ← Tells KNIME about your extension (name, author, etc.)
├── pixi.toml                 ← Lists the Python packages your node needs
├── config.yml                ← Optional debug settings
└── README.md                 ← A small readme for the generated project
```

### What each file does

- **`src/extension.py`** — This is the file you'll edit. It contains your node class with two methods:
  - `configure()` — Tells KNIME what the output table will look like *before* the node runs. Usually you just pass through the input schema.
  - `execute()` — The actual work. This is where you write your data processing logic.

- **`knime.yml`** — Metadata that KNIME reads to register your extension. You generally don't need to touch this after generation.

- **`pixi.toml`** — Dependency management. If your node needs extra Python packages (like `scikit-learn` or `matplotlib`), you add them here.

- **`config.yml`** — Used if you want to debug your node with a debugger. Optional.

- **`icons/icon.png`** — A tiny placeholder image. Replace it with your own 16×16 pixel PNG to give your node a custom icon in KNIME.

---

## How to Load Your Node into KNIME

Once you've generated the project and written your logic:

1. **Install dependencies** — Open a terminal in your generated project folder and run:
   ```bash
   pixi install
   ```
   This creates a Python environment with everything your node needs.

2. **Open KNIME Analytics Platform.**

3. **Register the extension:**
   - Go to **File → Preferences → KNIME → Python**.
   - Under the Python environment settings, point to the `pixi` environment (the `.pixi/envs/default` folder inside your project).
   - Then go to **KNIME → Python → Python Extension Preferences** and add the path to your project folder.

4. **Restart KNIME.** Your node should now appear in the Node Repository under the category you specified.

For the full official walkthrough, see the [KNIME Python Extension Guide](https://docs.knime.com/latest/pure_python_node_extensions_guide/).

---

## Editing Your Node Logic

Open `src/extension.py` in any text editor or IDE. Look for this section inside the `execute` method:

```python
def execute(self, exec_context, input_table_1):
    df = input_table_1.to_pandas()

    # ── Your processing logic here ──
    # Example: df['new_col'] = df['existing_col'] * 2

    output = knext.Table.from_pandas(df)
    return output
```

The variable `df` is a standard [pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) — the most common way to work with tabular data in Python. You can do anything pandas supports: filter rows, add columns, merge tables, run calculations, etc.

When you're done, convert it back with `knext.Table.from_pandas(df)` and return it.

### Accessing your parameters

If you added dialog parameters, you can access their values using `self`:

```python
def execute(self, exec_context, input_table_1):
    df = input_table_1.to_pandas()

    # Access the parameter values the user configured
    threshold = self.threshold
    column_name = self.text_column

    df = df[df[column_name] > threshold]

    return knext.Table.from_pandas(df)
```

### Adding Python dependencies

If your logic needs packages beyond pandas (e.g., `numpy`, `scikit-learn`, `requests`), add them to `pixi.toml`:

```toml
[dependencies]
numpy = "*"
scikit-learn = "*"
```

Then run `pixi install` again.

---

## Full Example: Start to Finish

Let's say you want a node that multiplies a numeric column by a user-specified factor.

### Step 1: Run the script

```
$ python3 create_knime_node.py

============================================================
  KNIME Python Node Extension Generator
============================================================

Extension ID [com.example.myextension]: com.example.multiply
Extension display name [My KNIME Extension]: Multiply Tools
Extension description [A custom KNIME extension]: Nodes for multiplying column values
Author [Your Name]: Jane Smith
Node category ID [mycategory]: multiply
Node category display name [My Category]: Multiply

Node name [My Custom Node]: Column Multiplier
Node description [...]: Multiplies a numeric column by a given factor.
Node type:
  1) MANIPULATOR
  ...
Choice [1]: 1

Number of input tables [1]: 1
Number of output tables [1]: 1
Include an output view? (y/n) [n]: n

Add dialog parameters (leave name blank to stop):
  Parameter name: factor
  Type [string]: double
  Description: The multiplication factor
  Default value [0]: 1.0
  Parameter name:

Output directory [multiply_tools]: multiply_tools
```

### Step 2: Edit the generated `execute` method

Open `multiply_tools/src/extension.py` and change the execute method to:

```python
def execute(self, exec_context, input_table_1):
    df = input_table_1.to_pandas()

    # Multiply all numeric columns by the user-specified factor
    numeric_cols = df.select_dtypes(include='number').columns
    df[numeric_cols] = df[numeric_cols] * self.factor

    return knext.Table.from_pandas(df)
```

### Step 3: Install and load

```bash
cd multiply_tools
pixi install
```

Then register the extension in KNIME as described above. Done — you now have a "Column Multiplier" node in your KNIME node repository.

---

## Glossary

| Term | Meaning |
|---|---|
| **Node** | A single processing block in KNIME. It has inputs, outputs, and a settings dialog. |
| **Extension** | A package of one or more nodes that can be installed into KNIME. |
| **Workflow** | A KNIME project — a canvas of connected nodes that process data step by step. |
| **Port** | A connection point on a node. Input ports receive data; output ports send data. |
| **Table** | The most common data type in KNIME — rows and columns, like a spreadsheet. |
| **Schema** | The structure of a table (column names and their data types) without the actual data. |
| **pandas DataFrame** | A Python object representing a table. The standard way to manipulate data in Python. |
| **pixi** | A package manager that sets up isolated Python environments for your extension. |
| **Decorator** | The `@knext.node(...)`, `@knext.input_table(...)` lines above the class. They tell KNIME how the node is configured. You don't need to understand them deeply — the script writes them for you. |
| **configure()** | A method KNIME calls *before* running the node, to check if the settings make sense and to predict the output structure. |
| **execute()** | A method KNIME calls when the node actually runs. This is where your logic goes. |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `python3: command not found` | Python isn't installed or isn't on your PATH. Install it from [python.org](https://www.python.org/downloads/). |
| `pixi: command not found` | Restart your terminal after installing pixi, or check the [pixi installation guide](https://pixi.sh). |
| The node doesn't appear in KNIME | Make sure you registered the extension path in KNIME's Python Extension Preferences and restarted KNIME. |
| `ModuleNotFoundError` when the node runs | You're missing a Python package. Add it to `pixi.toml` and run `pixi install`. |
| The script crashes with `KeyboardInterrupt` | You pressed Ctrl+C. That's fine — just run it again. |
| I want to add more nodes to the same extension | Add another `@knext.node` class in the same `src/extension.py` file, or create additional `.py` files in the `src/` folder. |

---

## Resources

- [KNIME Python Extension Guide](https://docs.knime.com/latest/pure_python_node_extensions_guide/) — The official tutorial from KNIME
- [KNIME Python API Reference](https://knime-python.readthedocs.io/) — Full API documentation
- [KNIME Python Extension Template (GitHub)](https://github.com/knime/knime-python-extension-template) — KNIME's own starter template
- [pixi Documentation](https://pixi.sh) — Package manager used for dependencies
- [pandas Documentation](https://pandas.pydata.org/docs/) — The data manipulation library used inside nodes
