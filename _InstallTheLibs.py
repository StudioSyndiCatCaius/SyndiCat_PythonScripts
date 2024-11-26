import subprocess
import sys
from typing import List
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import pkg_resources
import threading
import re
from time import sleep

class ProgressTracker:
    def __init__(self, total_packages):
        self.total_packages = total_packages
        self.completed = 0
        self.current_operations = {}
        self.lock = threading.Lock()
        
    def update_progress(self, package: str, status: str) -> None:
        """Update the progress status for a specific package"""
        with self.lock:
            self.current_operations[package] = status
            self._display_progress()
            
    def complete_package(self, package: str) -> None:
        """Mark a package as completed and remove it from current operations"""
        with self.lock:
            self.completed += 1
            if package in self.current_operations:
                del self.current_operations[package]
            self._display_progress()
    
    def _display_progress(self) -> None:
        """Display the current progress of all operations"""
        percentage = (self.completed / self.total_packages) * 100
        
        # Clear previous lines
        sys.stdout.write("\033[K")  # Clear current line
        for _ in range(len(self.current_operations)):
            sys.stdout.write("\033[F")  # Move cursor up
            sys.stdout.write("\033[K")  # Clear line
            
        # Print progress bar
        bar_length = 30
        filled = int(bar_length * percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\rOverall Progress: [{bar}] {percentage:.1f}% ({self.completed}/{self.total_packages})")
        
        # Print current operations
        for pkg, status in self.current_operations.items():
            print(f"  → {pkg}: {status}")
        
        sys.stdout.flush()

def get_package_version(package: str) -> tuple[bool, str]:
    """
    Check if a package is installed and get its version.
    
    Args:
        package: Name of the package to check
        
    Returns:
        Tuple of (is_installed, version_string)
    """
    try:
        version = pkg_resources.get_distribution(package).version
        return True, version
    except pkg_resources.DistributionNotFound:
        return False, ""

def install_or_update_package(package: str, progress_tracker: ProgressTracker) -> tuple[str, bool, str]:
    """
    Install a package if not present, or update it if already installed.
    
    Args:
        package: Name of the package to install/update
        progress_tracker: ProgressTracker instance for monitoring progress
        
    Returns:
        Tuple of (package_name, success_status, message)
    """
    installed, current_version = get_package_version(package)
    
    try:
        if installed:
            progress_tracker.update_progress(package, "Checking for updates...")
            # Try to upgrade the package
            process = subprocess.Popen(
                [sys.executable, "-m", "pip", "install", "--upgrade", package],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Monitor the upgrade process
            while True:
                output = process.stdout.readline()
                if output:
                    progress_tracker.update_progress(package, output.strip())
                if process.poll() is not None:
                    break
            
            # Check if version changed after upgrade
            _, new_version = get_package_version(package)
            
            if process.returncode == 0:
                message = (f"Updated from {current_version} to {new_version}" 
                          if new_version != current_version 
                          else f"Already up to date (version {current_version})")
                progress_tracker.complete_package(package)
                return package, True, message
            else:
                error = process.stderr.read().strip()
                progress_tracker.complete_package(package)
                return package, False, f"Update failed: {error}"
        else:
            progress_tracker.update_progress(package, "Starting installation...")
            # Package not installed, perform fresh install
            process = subprocess.Popen(
                [sys.executable, "-m", "pip", "install", package],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Monitor the installation process
            while True:
                output = process.stdout.readline()
                if output:
                    progress_tracker.update_progress(package, output.strip())
                if process.poll() is not None:
                    break
            
            if process.returncode == 0:
                _, installed_version = get_package_version(package)
                progress_tracker.complete_package(package)
                return package, True, f"Newly installed (version {installed_version})"
            else:
                error = process.stderr.read().strip()
                progress_tracker.complete_package(package)
                return package, False, error.strip()
                
    except Exception as e:
        progress_tracker.complete_package(package)
        return package, False, str(e)

def batch_install(packages: List[str], max_workers: int = 4) -> None:
    """
    Install/update multiple packages in parallel using ThreadPoolExecutor.
    
    Args:
        packages: List of package names to install/update
        max_workers: Maximum number of concurrent operations
    """
    print(f"\nStarting batch installation/update at {datetime.now().strftime('%H:%M:%S')}")
    print(f"Packages to process: {', '.join(packages)}\n")
    
    progress_tracker = ProgressTracker(len(packages))
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(install_or_update_package, package, progress_tracker)
            for package in packages
        ]
        results = [future.result() for future in futures]
    
    # Print final results
    success_count = 0
    print("\nFinal Results:")
    print("-" * 60)
    
    for package, success, message in results:
        status = "✓" if success else "✗"
        success_count += int(success)
        print(f"{status} {package}: {message}")
    
    print("-" * 60)
    print(f"Successfully processed {success_count}/{len(packages)} packages")

if __name__ == "__main__":
    # You can either pass packages as command line arguments
    # or modify this list directly
    packages_to_install = sys.argv[1:] if len(sys.argv) > 1 else [        
        "requests",
        "pandas",
        "numpy",
        "glob",
        "pyperclip",
        "PIL"
    ]
    
    batch_install(packages_to_install)