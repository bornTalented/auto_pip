# 👉 Install Python packages via pip and automatically append them (with version numbers)
# to requirements.txt if not already listed.

import os
import sys
import subprocess
from typing import List

# import pkg_resources
from importlib.metadata import version, PackageNotFoundError


def get_case_message(case: int):
    case_actions = {
        1: "Package is installed and already listed in requirements.txt: Do nothing.",
        2: "Package is installed but not in requirements.txt: Add to requirements.txt.",
        3: "Package is installed with a different version: Install requested version and append to requirements.txt (keep history).",
        4: "Package is not installed and not in requirements.txt: Install it and add to requirements.txt.",
    }
    # Get the case message from the existing function
    case_message = case_actions.get(case)
    if case_message:
        return f"Case{case}: {case_message}\nAction: "
    return "Invalid case\n"


def install_and_append(packages: List[str]):
    """
    Install Python packages using pip and ensure pinned versions 
    are recorded in requirements.txt, handling version mismatches, preserving version history.

    Handles the following cases:
    Case 1: Package is installed and already listed in requirements.txt -> Do nothing
    Case 2: Package is installed but not in requirements.txt -> Add to requirements.txt
    Case 3: Package is installed with a different version -> Install requested version and append new entry in requirements.txt (keep history)
    Case 4: Package is not installed and not in requirements.txt -> Install it and add to requirements.txt

    Parameters
    ----------
    packages : list of str
        List of package specifications (e.g., ["requests", "numpy==1.25.0"]).

    Raises
    ------
    subprocess.CalledProcessError
        If pip installation fails for any package.
    pkg_resources.DistributionNotFound
        If a package cannot be found after installation (rare case).
    """

    # Step 1: Load existing requirements (as set of lines)
    req_file = os.path.join(os.getcwd(), "requirements.txt")
    print(f"Loading requirements.txt from {req_file}")
    existing_lines = []
    try:
        with open(req_file, "r") as f:
            existing_lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        pass

    existing_set = set(existing_lines)  # for quick lookup

    for pkg in packages:
        # Extract package name and version (if specified)
        if "==" in pkg:
            pkg_name, pkg_version = pkg.split("==")
            pkg_name = pkg_name.strip()
            requested_version = pkg_version.strip()
        else:
            pkg_name = pkg.strip()
            requested_version = None

        installed_version = None
        # try:
        #     dist = pkg_resources.get_distribution(pkg_name)
        #     installed_version = dist.version
        # except pkg_resources.DistributionNotFound:
        #     installed_version = None

        # Check installed version using importlib.metadata
        try:
            installed_version = version(pkg_name)
        except PackageNotFoundError:
            installed_version = None

        # -------- Handle Cases --------
        if installed_version:
            if requested_version:
                if f"{pkg_name}=={requested_version}" in existing_set:
                    print(f"ℹ️ {get_case_message(1)}{pkg_name}=={requested_version} already installed and listed.")
                elif installed_version == requested_version:
                    # Installed version matches request, but may not be in requirements.txt
                    if f"{pkg_name}=={installed_version}" not in existing_set:
                        with open(req_file, "a") as f:
                            f.write(f"{pkg_name}=={installed_version}\n")
                        print(f"✅ {get_case_message(2)}Added {pkg_name}=={installed_version} to requirements.txt")
                    else:
                        print(f"ℹ️ {get_case_message(1)}{pkg_name}=={installed_version} already tracked.")
                else:
                    # Different version installed → upgrade/downgrade & append trace
                    print(f"⚠️ {get_case_message(3)}{pkg_name} installed ({installed_version}) but different version required ({requested_version}). Updating...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", f"{pkg_name}=={requested_version}"])
                    with open(req_file, "a") as f:
                        f.write(f"{pkg_name}=={requested_version}\n")
                    print(f"✅ {get_case_message(3)}Appended {pkg_name}=={requested_version} to requirements.txt (history preserved).")
            else:
                # No version requested → just ensure installed version is recorded
                entry = f"{pkg_name}=={installed_version}"
                if entry not in existing_set:
                    with open(req_file, "a") as f:
                        f.write(entry + "\n")
                    print(f"✅ {get_case_message(2)}Added {entry} to requirements.txt")
                else:
                    print(f"ℹ️ {get_case_message(1)}{entry} already installed and listed.")
        else:
            # Case 4: Not installed at all
            install_target = pkg if not requested_version else f"{pkg_name}=={requested_version}"
            print(f"⬇️ {get_case_message(4)}Installing {install_target} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", install_target])

            # dist = pkg_resources.get_distribution(pkg_name)
            # entry = f"{dist.project_name}=={dist.version}"

            installed_version = version(pkg_name)
            entry = f"{pkg_name}=={installed_version}"

            if entry not in existing_set:
                with open(req_file, "a") as f:
                    f.write(entry + "\n")
                print(f"✅ {get_case_message(4)}Added {entry} to requirements.txt")


# def install_and_append(packages):
    
#     # Step 1: Install all packages
#     subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
#     # Example: python -m pip install <package1> <package2> ...

#     # Step 2: Load current requirements
#     req_file = os.path.join(os.getcwd(), "requirements.txt")
#     existing_pkgs = set()
#     try:
#         with open(req_file, "r") as f:
#             existing_pkgs = set(line.strip() for line in f if line.strip())
#     except FileNotFoundError:
#         pass

#     # Step 3: Append new entries
#     new_entries = []
#     for pkg in packages:
#         try:
#             dist = pkg_resources.get_distribution(pkg)
#             versioned = f"{dist.project_name}=={dist.version}"
#             if versioned not in existing_pkgs:
#                 new_entries.append(versioned)
#             else:
#                 print(f"ℹ️ Already present: {versioned}")
#         except pkg_resources.DistributionNotFound:
#             print(f"❌ Package not found: {pkg}")

#     if new_entries:
#         with open(req_file, "a") as f:
#             for line in new_entries:
#                 f.write(line + "\n")
#                 print(f"✅ Added: {line}")
#     else:
#         print("✅ All packages already present.")


if __name__ == "__main__":
    # Checks if at least one package is passed via CLI.
    if len(sys.argv) < 2:
        print("Usage: python pip_install_and_append.py <package1> <package2> ...")
        sys.exit(1)
    # Calls the function with the list of packages.
    install_and_append(sys.argv[1:])
