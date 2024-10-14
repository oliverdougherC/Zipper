# Zipper for macOS

This project provides a graphical user interface (GUI) for the 7-Zip command-line tool on macOS, built using PyQt6.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have a macOS machine.
* You have installed Python 3.6 or later.
* You have installed pip (Python package installer).

## Installing 7-Zip GUI

To install 7-Zip GUI, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/oliverdougherC/Zipper
   cd Zipper
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

4. Install 7-Zip for macOS using Homebrew:
   ```
   brew install p7zip
   ```

   If you don't have Homebrew installed, you can install it from [brew.sh](https://brew.sh/).

## Using 7-Zip GUI

To use 7-Zip GUI, follow these steps:

1. Ensure you're in the project directory and your virtual environment is activated (if you created one).

2. Run the main script:
   ```
   python main.py
   ```

3. The GUI will open, allowing you to:
   - Select files or directories to compress
   - Choose compression options
   - Extract compressed archives
   - Set passwords for compression/extraction

## Troubleshooting

If you encounter any issues:

1. Ensure 7-Zip is correctly installed and accessible from the command line:
   ```
   7z
   ```
   This should display the 7-Zip help information.

2. Check that all required Python packages are installed:
   ```
   pip list
   ```
   Verify that PyQt6 is in the list.

3. If you're having issues with file permissions, ensure you have read/write access to the directories you're working with.

## Contributing to Zipper

To contribute to Zipper, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## Contact

If you want to contact me, you can reach me at `<tiger.hornet7259@eagereverest.com>`.

## License

This project uses the following license: [MIT](https://opensource.org/licenses/MIT).

