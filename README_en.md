
<p align="center">
  <img src="Banner.png" alt="zZipCracker" width="300"/>
</p>

<p align="right">
  <a href="./README.md">Zur deutschen Version wechseln</a>
</p>

# zZipCracker – Brute-Force ZIP Cracking Tool

**zZipCracker** is a lightweight Python tool to demonstrate brute-force attacks on password-protected ZIP files.  
Perfect for educational purposes and raising awareness about password security and brute-force mechanics.

> ⚠️ Note: This tool is developed for **educational and demonstration purposes only**. Do not use it on third-party systems or files without explicit permission!

---

## Features

- Brute-force attack on ZIP files by systematically testing password combinations
- Uses Windows command line for process distribution
- Splits character list across four parallel processes
- Progress bar per character combination and password length
- Minimal resource usage – only external dependency: `tqdm`

---

## Motivation

This project was created as a practical exercise on **password security**, **brute-force techniques**, and **parallelization in Windows**.  
It helps to understand:

- How brute-force attacks work technically
- Why weak passwords are a major risk
- How to split and parallelize tasks – even without frameworks

The idea was inspired by the book _"Ethical Hacking"_ by Florian André Dalwigk.

---

## Requirements

- Python 3.x (tested on Windows with 3.10)
- Installed [7-Zip](https://www.7-zip.org/) command line tool (`7z` must be in PATH)
- A password-protected ZIP file for testing

---

## Installation & Usage

1. Clone the repository or download the script:

```bash
git clone https://github.com/0xZorro/zZipCracker.git
```

2. Change into the project directory and run the script:

```bash
python zzipcracker.py secret.zip 3 5
```

3. **Four CMD windows** will open automatically, each trying to crack the password in parallel.

---

## Functionality: Automatic Subprocess Splitting

`zZipCracker` is designed to **distribute brute-force work across four parallel processes** – **each CMD window handles a character segment**.

### Automatic Flow:

```bash
python zzipcracker.py secret.zip 3 5
```

1. The program detects: “I’m the main process”
2. It spawns **4 new CMD windows**
3. Each window runs the same code – **with its own `segment_index`**
4. This results in even distribution of the character set

```
┌────────────────────────────┐
│        Main Process        │
│  (launches 4 CMD windows)  │
└────────────────────────────┘
       ↓      ↓      ↓      ↓
   [CMD 0] [CMD 1] [CMD 2] [CMD 3]
      │        │       │       │
      ▼        ▼       ▼       ▼
 crack_zip() crack_zip() ... crack_zip()
   (Part 1)   (Part 2)       (Part 4)
```

### Manual Execution of a Specific Segment:

```bash
python zzipcracker.py secret.zip 3 5 2
```

This runs only the **third subprocess** (index 2) – useful for testing or targeted runs.

### Note:

The `segment_index` (0 to 3) determines **which starting characters** the process works with.

### Command Line Arguments Explained

Running the tool like this:

```bash
python zzipcracker.py secret.zip 3 5
```

passes the following arguments:

| Position | Argument        | Meaning                                                                     |
|----------|------------------|-----------------------------------------------------------------------------|
| `1`      | `secret.zip`     | Path to the ZIP file to crack                                               |
| `2`      | `3`              | **Minimum password length** – tool starts testing from this length onward  |
| `3`      | `5`              | **Maximum password length** – tool tests up to this length                 |
| `4` *(optional)* | `2`      | (Only for manual execution) Index of character range: `0` to `3`            |

---

🔹 The **min** and **max** arguments define the **length range** of the passwords to test.  
🔹 If no `segment_index` is given → the main program starts **four parallel CMD processes** automatically.  
🔹 If a `segment_index` is provided → only that **one segment** will be processed.

### Documentation

- [Read the detailed documentation (crack_zip.md)](./doc_EN/crack_zip.md)

---

## Security Disclaimer

This tool is **not intended for illegal cracking of third-party archives**, but to raise awareness:

- How quickly weak passwords can be cracked
- Why special characters, length, and randomness matter
- Why password managers are recommended

---

## Future Improvements

The `zZipCracker` project is a solid base for experimental brute-forcing – but many exciting features could be added:

- **Support for wordlists**  
  Allow loading of external files like `rockyou.txt` for dictionary-based testing.

- **Character set via CLI argument**  
  Optional switch like `--charset=abc123` to limit characters used in combinations.

- **More than 4 processes**  
  Current version splits into four segments. Dynamic splitting (based on CPU cores) would be more scalable.

- **Threading within a CMD window**  
  Currently, each CMD runs linearly. Multithreading within one CMD could further improve performance.

- **Logging tested passwords**  
  Optional logging of all tested combinations – useful for long sessions and analysis.

- **Handling of `"` character**  
  The double quote (`"`) is removed due to shell issues. More robust solution: escaping or input via file.

- **Modularization & cleanup**  
  Split into modules like `bruteforce.py`, `cli.py`, `log.py` for better maintainability.

- **Benchmarking feature**  
  Output attempts per second and time per segment – helpful for performance analysis.

---

## License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

## Author

**Created by Jose Luis Ocana**

Cybersecurity Learner | Python & C++ Tools

(GitHub: [0xZorro](https://github.com/0xZorro))  

TryHackMe: https://tryhackme.com/p/0xZorro

Contact: zorro.jose@gmx.de

---

## Contributions

Want to contribute? Awesome!  
Fork the project, make your changes, and open a pull request.  
Please follow the code of conduct and project standards.

---

## ⚠️ Legal Disclaimer

### Warning:

This tool is for **educational and demonstration purposes only** in the field of cybersecurity.  
Any misuse, especially against systems or files you do not own or have permission to test, is **illegal**.

---

## Disclaimer

The author assumes **no responsibility or liability** for any damage, data loss, or legal consequences resulting from using this software.  
Use at your **own risk** – for testing environments only!

---

<div align="center">
  <img src="brand.png" alt="by 0xZorro" width="120"/>
  <br/>
  <sub>© 2025 0xZorro</sub>
</div>

---
