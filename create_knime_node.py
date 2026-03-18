#!/usr/bin/env python3
"""
KNIME Node Template Generator

Generates the scaffolding for a KNIME Python node extension.
Run:  python create_knime_node.py

It will prompt you for details and produce a ready-to-use project folder
compatible with the KNIME Python Extension API (knime.extension).

Reference: https://docs.knime.com/latest/pure_python_node_extensions_guide/
"""

import os
import sys
import textwrap

# ── Helpers ──────────────────────────────────────────────────────────────────

NODE_TYPES = {
    "1": ("MANIPULATOR", "A node that manipulates data"),
    "2": ("LEARNER", "A node learning a model"),
    "3": ("PREDICTOR", "A node that predicts using a model"),
    "4": ("SOURCE", "A node producing data"),
    "5": ("SINK", "A node consuming data"),
    "6": ("VISUALIZER", "A node that visualizes data"),
    "7": ("OTHER", "Doesn't fit other categories"),
}

PARAM_TYPES = {
    "string": 'knext.StringParameter("{label}", "{desc}", "{default}")',
    "int": 'knext.IntParameter("{label}", "{desc}", {default})',
    "double": 'knext.DoubleParameter("{label}", "{desc}", {default})',
    "bool": 'knext.BoolParameter("{label}", "{desc}", {default})',
    "column": 'knext.ColumnParameter("{label}", "{desc}", port_index=0)',
    "multicolumn": 'knext.MultiColumnParameter("{label}", "{desc}", port_index=0)',
    "columnfilter": 'knext.ColumnFilterParameter("{label}", "{desc}", port_index=0)',
}


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val if val else default


def ask_int(prompt: str, default: int = 0) -> int:
    val = ask(prompt, str(default))
    try:
        return int(val)
    except ValueError:
        return default


def ask_choice(prompt: str, options: dict) -> str:
    print(prompt)
    for key, (name, desc) in options.items():
        print(f"  {key}) {name} – {desc}")
    return ask("Choice", "1")


def to_class_name(name: str) -> str:
    """Convert a human-readable name to PascalCase class name."""
    return "".join(word.capitalize() for word in name.split())


def to_snake(name: str) -> str:
    """Convert a human-readable name to snake_case."""
    return "_".join(name.lower().split())


# ── Gather user input ───────────────────────────────────────────────────────

def gather_input() -> dict:
    print("=" * 60)
    print("  KNIME Python Node Extension Generator")
    print("=" * 60)
    print()

    cfg = {}

    # Extension metadata
    cfg["ext_id"] = ask("Extension ID (e.g. com.example.myextension)", "com.example.myextension")
    cfg["ext_name"] = ask("Extension display name", "My KNIME Extension")
    cfg["ext_desc"] = ask("Extension description", "A custom KNIME extension")
    cfg["author"] = ask("Author", "Your Name")
    cfg["category_id"] = ask("Node category ID (short, no spaces)", "mycategory")
    cfg["category_name"] = ask("Node category display name", "My Category")

    # Node metadata
    print()
    cfg["node_name"] = ask("Node name", "My Custom Node")
    cfg["node_desc"] = ask("Node description", "Processes input data and produces output data.")
    choice = ask_choice("Node type:", NODE_TYPES)
    cfg["node_type"] = NODE_TYPES.get(choice, NODE_TYPES["1"])[0]

    # Ports
    print()
    cfg["num_input_tables"] = ask_int("Number of input tables", 1)
    cfg["num_output_tables"] = ask_int("Number of output tables", 1)
    cfg["has_view"] = ask("Include an output view? (y/n)", "n").lower().startswith("y")

    # Parameters
    print()
    print("Add dialog parameters (leave name blank to stop):")
    print(f"  Available types: {', '.join(PARAM_TYPES.keys())}")
    params = []
    while True:
        pname = ask("  Parameter name (blank to finish)")
        if not pname:
            break
        ptype = ask("  Type", "string")
        if ptype not in PARAM_TYPES:
            print(f"    Unknown type '{ptype}', defaulting to string")
            ptype = "string"
        pdesc = ask("  Description", f"The {pname} parameter")
        if ptype in ("int", "double"):
            pdefault = ask("  Default value", "0")
        elif ptype == "bool":
            pdefault = ask("  Default value (True/False)", "False")
        elif ptype in ("column", "multicolumn", "columnfilter"):
            pdefault = None
        else:
            pdefault = ask("  Default value", "")
        params.append({"name": pname, "type": ptype, "desc": pdesc, "default": pdefault})
    cfg["params"] = params

    # Output directory
    print()
    cfg["output_dir"] = ask("Output directory", to_snake(cfg["ext_name"]))

    return cfg


# ── Code generators ─────────────────────────────────────────────────────────

def gen_extension_py(cfg: dict) -> str:
    class_name = to_class_name(cfg["node_name"])
    lines = []

    # Header
    lines.append("import logging")
    lines.append("import knime.extension as knext")
    lines.append("")
    lines.append("LOGGER = logging.getLogger(__name__)")
    lines.append("")
    lines.append("")

    # Category
    lines.append("# ── Category ────────────────────────────────────────────────")
    lines.append("category = knext.category(")
    lines.append(f'    path="/community",')
    lines.append(f'    level_id="{cfg["category_id"]}",')
    lines.append(f'    name="{cfg["category_name"]}",')
    lines.append(f'    description="{cfg["ext_desc"]}",')
    lines.append('    icon="icons/category.png",')
    lines.append(")")
    lines.append("")
    lines.append("")

    # Node decorators
    lines.append("# ── Node ────────────────────────────────────────────────────")
    lines.append("@knext.node(")
    lines.append(f'    name="{cfg["node_name"]}",')
    lines.append(f"    node_type=knext.NodeType.{cfg['node_type']},")
    lines.append('    icon_path="icons/icon.png",')
    lines.append("    category=category,")
    lines.append(")")
    for i in range(cfg["num_input_tables"]):
        label = f"Input Table {i+1}" if cfg["num_input_tables"] > 1 else "Input Table"
        lines.append(f'@knext.input_table(name="{label}", description="Input data")')
    for i in range(cfg["num_output_tables"]):
        label = f"Output Table {i+1}" if cfg["num_output_tables"] > 1 else "Output Table"
        lines.append(f'@knext.output_table(name="{label}", description="Output data")')
    if cfg["has_view"]:
        lines.append('@knext.output_view(name="Output View", description="Visual output")')

    # Class definition
    lines.append(f"class {class_name}(knext.PythonNode):")
    lines.append(f'    """{cfg["node_desc"]}"""')
    lines.append("")

    # Parameters
    if cfg["params"]:
        for p in cfg["params"]:
            attr_name = to_snake(p["name"])
            tmpl = PARAM_TYPES[p["type"]]
            val = tmpl.format(label=p["name"], desc=p["desc"], default=p["default"] or "")
            lines.append(f"    {attr_name} = {val}")
        lines.append("")

    # configure()
    input_args = ", ".join(f"input_schema_{i+1}" for i in range(cfg["num_input_tables"]))
    configure_sig = f"self, configure_context, {input_args}" if input_args else "self, configure_context"
    lines.append(f"    def configure({configure_sig}):")
    lines.append(f'        LOGGER.info("Configuring {cfg["node_name"]}")')

    configure_returns = []
    for i in range(cfg["num_output_tables"]):
        ref = f"input_schema_{i+1}" if i < cfg["num_input_tables"] else "input_schema_1"
        configure_returns.append(ref)
    if cfg["num_output_tables"] == 1:
        lines.append(f"        return {configure_returns[0]}")
    else:
        lines.append(f"        return ({', '.join(configure_returns)})")
    lines.append("")

    # execute()
    exec_args = ", ".join(f"input_table_{i+1}" for i in range(cfg["num_input_tables"]))
    execute_sig = f"self, exec_context, {exec_args}" if exec_args else "self, exec_context"
    lines.append(f"    def execute({execute_sig}):")
    lines.append(f'        LOGGER.info("Executing {cfg["node_name"]}")')

    if cfg["num_input_tables"] >= 1:
        lines.append("        df = input_table_1.to_pandas()")
        lines.append("")
        lines.append("        # ── Your processing logic here ──")
        lines.append("        # Example: df['new_col'] = df['existing_col'] * 2")
        lines.append("")
        lines.append("        output = knext.Table.from_pandas(df)")
    else:
        lines.append("        import pandas as pd")
        lines.append("        df = pd.DataFrame({'result': ['hello']})")
        lines.append("        output = knext.Table.from_pandas(df)")

    if cfg["has_view"]:
        lines.append("")
        lines.append("        # ── Build view ──")
        lines.append("        # import knime.scripting.io as knio")
        lines.append("        # import matplotlib.pyplot as plt")
        lines.append("        # fig, ax = plt.subplots()")
        lines.append("        # ax.plot(df['col'])")
        lines.append("        # view = knio.view_matplotlib(fig)")
        lines.append('        view = knext.view_html("<h1>Hello from the view</h1>")')

    if cfg["num_output_tables"] == 1 and not cfg["has_view"]:
        lines.append("        return output")
    elif cfg["num_output_tables"] == 1 and cfg["has_view"]:
        lines.append("        return output, view")
    elif cfg["num_output_tables"] > 1 and cfg["has_view"]:
        outputs = ", ".join(["output"] * cfg["num_output_tables"])
        lines.append(f"        return ({outputs}, view)")
    else:
        outputs = ", ".join(["output"] * cfg["num_output_tables"])
        lines.append(f"        return ({outputs})")

    lines.append("")
    return "\n".join(lines) + "\n"


def gen_knime_yml(cfg: dict) -> str:
    return textwrap.dedent(f"""\
        id: {cfg['ext_id']}
        name: {cfg['ext_name']}
        author: {cfg['author']}
        description: {cfg['ext_desc']}
        src: src
    """)


def gen_config_yml(_cfg: dict) -> str:
    return textwrap.dedent("""\
        # Debug / development configuration for KNIME
        # Point this to your KNIME Analytics Platform installation
        # knime_executable: /path/to/knime

        # Uncomment to enable debug mode
        # debug: true
        # debug_port: 5678
    """)


def gen_pixi_toml(cfg: dict) -> str:
    return textwrap.dedent(f"""\
        [project]
        name = "{to_snake(cfg['ext_name'])}"
        version = "0.1.0"
        description = "{cfg['ext_desc']}"
        channels = ["conda-forge", "knime"]
        platforms = ["osx-arm64", "osx-64", "linux-64", "win-64"]

        [dependencies]
        python = ">=3.11,<3.13"
        knime-extension = "*"
        knime-python-base = "*"
        pandas = ">=2.0"

        # Add your dependencies below
        # numpy = "*"
        # scikit-learn = "*"
        # matplotlib = "*"
        # plotly = "*"
    """)


def gen_readme(cfg: dict) -> str:
    return textwrap.dedent(f"""\
        # {cfg['ext_name']}

        {cfg['ext_desc']}

        ## Development

        1. Install [pixi](https://pixi.sh) if you haven't already.
        2. Run `pixi install` in this directory to set up the Python environment.
        3. Open the project in VS Code and select the `.pixi/envs/default` Python interpreter.
        4. In KNIME Analytics Platform, go to **Preferences → KNIME → Python** and
           point to the pixi environment, then add this folder as a local extension.

        ## Project Structure

        ```
        ├── icons/
        │   └── icon.png
        ├── src/
        │   └── extension.py      ← node implementation
        ├── knime.yml              ← extension metadata
        ├── pixi.toml              ← Python dependencies
        ├── config.yml             ← debug configuration
        └── README.md
        ```

        ## Reference

        - [KNIME Python Extension Guide](https://docs.knime.com/latest/pure_python_node_extensions_guide/)
        - [KNIME Python API Docs](https://knime-python.readthedocs.io/)
    """)


# ── SVG icon placeholder (16x16) ────────────────────────────────────────────

PLACEHOLDER_ICON = (
    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10'
    b'\x08\x02\x00\x00\x00\x90\x91h6\x00\x00\x00\x1eIDATx\x9cc\xfc\xcf\x80'
    b'\x1c0\xa1\xc8\x30\xa0\x06\x8c\x1a0j\xc0\xa8\x01\xa3\x06\x0c\x1e\x03'
    b'\x00\x05\xd8\x00\x11\xc4\x1e\x1e\xf0\x00\x00\x00\x00IEND\xaeB`\x82'
)


# ── Write files ─────────────────────────────────────────────────────────────

def write_project(cfg: dict):
    base = cfg["output_dir"]
    dirs = [
        base,
        os.path.join(base, "src"),
        os.path.join(base, "icons"),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    files = {
        os.path.join(base, "src", "extension.py"): gen_extension_py(cfg),
        os.path.join(base, "knime.yml"): gen_knime_yml(cfg),
        os.path.join(base, "config.yml"): gen_config_yml(cfg),
        os.path.join(base, "pixi.toml"): gen_pixi_toml(cfg),
        os.path.join(base, "README.md"): gen_readme(cfg),
    }

    for path, content in files.items():
        with open(path, "w") as f:
            f.write(content)

    icon_path = os.path.join(base, "icons", "icon.png")
    if not os.path.exists(icon_path):
        with open(icon_path, "wb") as f:
            f.write(PLACEHOLDER_ICON)

    print()
    print("=" * 60)
    print(f"  Project created in: {base}/")
    print("=" * 60)
    print()
    print("Next steps:")
    print(f"  1. cd {base}")
    print(f"  2. pixi install")
    print(f"  3. Edit src/extension.py with your logic")
    print(f"  4. Add the extension to KNIME Analytics Platform")
    print()


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        cfg = gather_input()
        write_project(cfg)
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(1)
