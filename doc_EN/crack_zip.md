# Detailed Explanation: `crack_zip()` – Code Logic & Mathematical Context

This function is the core of the brute-force attack. It runs in a separate process (CMD window) and handles a specific segment of the total character space. The goal is to systematically test **all possible password combinations** starting with a specific initial character.

---

## Function Signature

```python
def crack_zip(archiv, min_len=1, max_len=10, segment_index=None):
```

| Parameter        | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `archiv`         | Path to the password-protected ZIP file                                     |
| `min_len`        | Minimum password length                                                     |
| `max_len`        | Maximum password length                                                     |
| `segment_index`  | Specifies which part of the character list this process should handle (0–3) |

---

## Character List Segmentation

The global character list `characters` is divided into four equal parts (with `num_processes = 4`).  
Each process only works with password combinations that **start with one of its assigned initial characters**.

```python
range_size = len(characters) // 4
```

Example:  
If the character list contains **64 characters**, then:

```
range_size = 64 // 4 = 16
```

The segments would be:
- Segment 0 → Characters 0–15
- Segment 1 → Characters 16–31
- Segment 2 → Characters 32–47
- Segment 3 → Characters 48–63

The last process may include any remaining characters:

```python
if i == num_processes - 1:
    ende = character_length
```

---

## Goal: Even Distribution Across Processes

```text
┌────────────────────────────┐
│ Character List (64 chars)  │
└────────────────────────────┘
        ↓  ↓  ↓  ↓
   [Seg 0] [Seg 1] ...
   (A-F)   (G-L)   ...
```

---

## Iterating Through Password Lengths

```python
for n in range(min_len, max_len + 1):
    rest_len = n - 1
```

This loop goes through **all desired password lengths** – from `min_len` up to and including `max_len`.

### Example:
```python
min_len = 3
max_len = 5
range(min_len, max_len + 1)  # yields: 3, 4, 5
```

This means:  
The program will try passwords with **3, 4, and 5 characters**.

---

Since the brute-force logic is designed so that **each password starts with a fixed character** (from the assigned segment),  
the **remaining positions** are filled with combinations.

Hence `rest_len` is calculated as:

```python
rest_len = n - 1
```

That means:  
If the desired password length is `n = 4`:

- 1 character is determined by `first_letter` (e.g., 'A')
- The **remaining 3 characters** are formed using combinations via `itertools.product()`

---

### Visualization:

```
Goal: Password length n = 4
                  ▼
        ┌──────┬────────────────────┐
        │  'A' │  ('1', '2', '!')   │
        └──────┴────────────────────┘
          ▲           ▲
   Start character   rest_len = 3
```

Result:
```
'A' + '1' + '2' + '!'  →  'A12!'
```

So we get:
- **Total password length** = `n`
- **Combinations** are generated only for the remaining characters after the first one

---

## Calculating Combinations with `itertools.product`

```python
for kombi in itertools.product(characters, repeat=rest_len):
```

### Mathematical Background: **Cartesian Product**

Given a character set \( C \) with \( |C| \) characters.  
We want all combinations of length \( r \) **with repetition**:

### Formula:

\[
|C|^r
\]

Where:
- \( |C| \): Number of characters in the set
- \( r \): Number of positions to combine (e.g., 3)

---

### Example:

```python
characters = ['a', 'b']
rest_len = 2
```

Result of `itertools.product(characters, repeat=2)`:

```
('a', 'a')
('a', 'b')
('b', 'a')
('b', 'b')
```

 → 2 characters, 2 positions = \( 2^2 = 4 \) combinations

---

## Constructing the Password

```python
password = first_letter + ''.join(kombi)
```

Example:
```python
first_letter = 'A'
kombi = ('1', '2', '!')
password = 'A12!'
```

---

## Verification via 7-Zip

```python
if unzip(archiv, password):
    print("Password cracked!")
    return password
```

If the password is correct (return value 0), the function stops immediately.

---

## Flowchart (Simplified)

```
Start
 │
 │→ Select character segment (segment_index)
 │
 │→ For each password length n:
 │     │
 │     └─ For each starting character:
 │            │
 │            └─ Generate combinations of remaining characters
 │                  │
 │                  └─ Test constructed password with 7z
 │
 └──> Password found? → Yes → return
                        → No → continue
```

---

## Conclusion

- The function generates all possible character set combinations of length `n`
- It’s mathematically predictable and measurable
- It efficiently distributes the workload across processes
- Ideal for demonstrating brute-force logic and combinatorics

---

Documentation written by: Jose Luis Ocana (GitHub: [0xZorro](https://github.com/0xZorro))  
Last updated: April 2025

<div align="center">
  <img src="brand.png" alt="by 0xZorro" width="120"/>
  <br/>
  <sub>© 2025 0xZorro</sub>
</div>

---
