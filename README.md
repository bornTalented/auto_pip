# 📦 Python Project Package Installer & `requirements.txt` Auto-Updater

This repository provides a utility script to simplify installing Python packages **per project** and **automatically update** that project's `requirements.txt` file. It also includes optional shell function setup to streamline the workflow.

---

## 🚀 Features

* Install Python packages into a specific project.
* Automatically update the appropriate `requirements.txt`.
* Shell function for convenient usage from any project folder.

---

## 📁 Project Structure

Ensure your directory is organized as follows:

```
MyProject/
├── Project1/
│   ├── requirements.txt
│   └── (other files)
├── Project2/
│   ├── requirements.txt
│   └── (other files)
├── Project3/
│   ├── requirements.txt
│   └── (other files)
└── pip_install_and_append.py   # Script for installing packages and updating requirements
```

---

## 🛠️ Usage Instructions

### 1. Navigate to the Target Project Directory

Example (for `Project1`):

```bash
cd /users/ABC/MyProject/Project1
```

### 2. Run the Script

Install a package and update the current project's `requirements.txt`:

```bash
python ../pip_install_and_append.py <package_name>
```

Example:

```bash
python ../pip_install_and_append.py numpy
```

This will:

* Install `numpy` in the current environment.
* Append it to `requirements.txt` inside `Project1`.

---

## ⚙️ Optional: Create a Shell Function (`pipa`) for Simplicity

You can create a shell function called `pipa` to run the script more easily from any project directory.

### Step 1: Check Your Shell

```bash
echo $SHELL
```

- If the output is `/bin/zsh`, you’re using **zsh**.
- If the output is `/bin/bash`, you’re using **bash**.

### Step 2: Add the Alias

#### For `zsh`:

```bash
nano ~/.zshrc
```

#### For `bash`:

```bash
nano ~/.bash_profile
# or
nano ~/.bashrc
```

#### Add the alias at the end of the file:

   ```bash
   alias pipa='python3 ../pip_install_and_append.py'
   ```

> To make the `alias pipa` command look for `pip_install_and_append.py` in the **current**, **parent**, and **grandparent** directories (in that order), you'll need to write a small shell script or use inline shell logic to check each location.

#### Add the following function instead of Alias:

```bash
unalias pipa 2>/dev/null

pipa() {
  script_name="pip_install_and_append.py"

  if [ -f "./$script_name" ]; then
    python3 "./$script_name" "$@"
  elif [ -f "../$script_name" ]; then
    python3 "../$script_name" "$@"
  elif [ -f "../../$script_name" ]; then
    python3 "../../$script_name" "$@"
  else
    echo "Error: $script_name not found in current, parent, or grandparent directory."
    return 1
  fi
}
```

Save and exit (for `nano` users):
   - Press `CTRL + X` to exit.
   - Press `Y` to confirm saving.
   - Press `Enter` to confirm the filename.
### Step 3: Apply the Changes

```bash
source ~/.zshrc         # For zsh
source ~/.bash_profile  # For bash
# or
source ~/.bashrc
```

---

## ✅ Example Usage

After setting up the alias, you can now run the following command inside any project folder (e.g., `Project1`, `Project2`):

```bash
cd /users/ABC/MyProject/Project1
pipa numpy
```

This will install the package `numpy` and update the `requirements.txt` file for the current project. You can also specify a specific version or pass multiple packages to be installed, like this:

```bash
pipa numpy==1.21.0 pandas requests
```

This will install:

* `numpy` version `1.21.0`
* `pandas`
* `requests`

And automatically update `requirements.txt` with the respective versions.

---

## 💡 Optional: Use a Virtual Environment

Before using the script, you can create and activate a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

> ⚠️ **Note**: If you encounter this error:
>
> `ModuleNotFoundError: No module named 'pkg_resources'`
> Run:
>
> ```bash
> pip install --upgrade setuptools
> ```

---

## 🧰 Troubleshooting

* **Script Not Found**: Make sure `pip_install_and_append.py` exists in a parent directory.
* **Permission Denied**: Ensure you have write access to the project folder and `requirements.txt`.
* **Wrong Directory**: Always navigate to the target project before running the script.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---
