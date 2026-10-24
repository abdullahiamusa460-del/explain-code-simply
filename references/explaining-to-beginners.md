# Explaining Code to Beginners

Read this before writing an explanation. It is the style guide for the
`explain-code-simply` skill.

## What a good explanation must do

When you finish, the reader should be able to answer three questions:

1. What does this code do, in one sentence?
2. What goes in, and what comes out?
3. Where would I change it if I needed something different?

If the reader cannot answer those questions, the explanation is not finished.

## The six parts of an explanation

Use these parts in this order. Keep each part short.

### 1. One-sentence summary

Start with one plain sentence. Name the job, not the language feature.

- Good: "This function reads a text file and returns the average of the numbers
  in it."
- Bad: "This function leverages a list comprehension to aggregate numeric
  input."

If the code does more than one thing, use one sentence for the main job and
list the side jobs after it.

### 2. Inputs and outputs

Show a small table. Include the type, an example value, and what happens when
the value is missing or empty.

| Item | Type | Example | Notes |
| --- | --- | --- | --- |
| `path` | text | `"numbers.txt"` | Must be a file that exists |
| return | number | `12.5` | Returns `0` for an empty file |

Also name side effects: printing, writing a file, changing a global value,
sending a network request, or raising an error.

### 3. Step-by-step walkthrough

Go in the order the computer runs the code.

- Use line numbers from `scripts/code_map.py`.
- Group lines that do one job. Do not narrate every bracket.
- Explain *why* a step exists, not only *what* it does.
- Cover every `return`, `raise`, `throw`, `break`, and `continue`.
- When a call goes to another file or an outside service, say so.

Example:

> Lines 8–10 make an empty list, then loop over each line in the file. The
> `if line.strip()` check skips blank lines, because `int("")` would crash.

### 4. Words decoded

Pick 3 to 6 terms that a beginner may not know. Define each one in one sentence,
then connect it to this code.

> **List comprehension:** A short way to build a new list from a loop. Here it
> turns each line of text into a number.

Do not define every word. Define the words this reader needs for this file.

### 5. One analogy (optional)

Use an analogy only when it makes the code clearer. Say where the analogy stops
being true.

> Think of the function as a kitchen scale: you put food on it, and it gives you
> one number. Unlike a scale, it also skips blank lines.

Skip this part if the code is already concrete.

### 6. Next step

End with one small, safe action:

- a command to run the code,
- one value to change and observe,
- or one question the reader can ask next.

Do not end with a vague "let me know if you have questions."

## Tone rules

- Use short sentences. One idea per sentence.
- Prefer active voice: "The loop adds each number," not "Each number is added."
- Define a term the first time it appears.
- Use the names from the code: `load_numbers`, not "the loader thing."
- Say "I am not sure" when you are not sure. Never guess about behavior.
- Do not use "simply," "just," "obviously," or "of course."
- Do not call code "easy" or "basic." It makes the reader feel behind.
- Do not hide complexity. Name it, then explain it in smaller pieces.

## Good and bad examples

| Bad | Why it is bad | Better |
| --- | --- | --- |
| "This function leverages a closure to memoize results." | Four jargon words, no concrete meaning. | "The inner function remembers the answer from last time. That saved answer is called a cache." |
| "Simply call the API." | "Simply" hides a big step, and "API" is undefined. | "Send a request to the weather service and wait for its answer. That service is the API." |
| "The loop iterates over the collection." | Abstract words, no names from the code. | "The loop visits each student in the `students` list, one at a time." |
| "It returns false on error." | Does not say which error or why. | "If the file is missing, line 14 catches the error and returns `False`." |

## Worked example

Code (`average.py`):

```python
def average(path):
    total = 0
    count = 0
    with open(path) as handle:
        for line in handle:
            if line.strip():
                total += float(line)
                count += 1
    if count == 0:
        return 0
    return total / count
```

Explanation:

**What it does:** This function reads numbers from a file and returns their
average.

**Inputs and outputs:**

| Item | Type | Example | Notes |
| --- | --- | --- | --- |
| `path` | text | `"scores.txt"` | One number per line |
| return | number | `7.5` | Returns `0` if the file has no numbers |

It also opens a file. It does not change the file.

**Step by step:**

1. Lines 2–3 start `total` and `count` at zero. `total` will hold the sum, and
   `count` will hold how many numbers were found.
2. Line 4 opens the file. The `with` block closes it automatically when the
   block ends.
3. Lines 5–9 visit each line. `line.strip()` removes spaces and the newline. If
   the result is empty, the loop skips that line.
4. Lines 8–9 turn the text into a decimal number with `float`, add it to
   `total`, and add one to `count`.
5. Lines 10–11 guard against dividing by zero. An empty file would make `count`
   zero, so the function returns `0` early.
6. Line 12 divides the sum by the count and returns the result.

**Words to know:**

- **`with open(...)`:** opens a file and promises to close it later.
- **`float`:** turns text such as `"3.5"` into a decimal number.
- **Guard clause:** an early check that stops a bad case before the main work.

**Next step:** Run `python3 -c "from average import average; print(average('scores.txt'))"` with a file that has three numbers. Then delete all the numbers and run it again to see the guard clause return `0`.

## Reading the map from `scripts/code_map.py`

The script prints a quick map. Use it like this:

- **Start here:** the first class or function. Explain that before helpers.
- **Definitions:** line numbers for classes and functions. Use these exact
  numbers in the walkthrough.
- **Imports:** outside code the file depends on. Mention them only if they
  affect the reader's understanding.
- **Notes:** `TODO`, `FIXME`, and similar comments. Mention them as unfinished
  work, not as bugs unless the code proves it.
- **Long lines:** lines over 100 characters. They often hide several steps; split
  them into smaller ideas.
- **Counts:** the code, comment, and blank counts are approximate. The line
  numbers are exact.

The script is a helper, not a parser. For unusual syntax, trust the source file.

## Handling different requests

- **"Line by line":** still use the six parts, then add a numbered list with one
  item per small group of lines. Do not explain punctuation.
- **"Like I'm 12":** keep the same facts. Use shorter sentences and more
  concrete examples. Do not remove accuracy.
- **"For an interview":** add the name of the pattern (for example, "a guard
  clause" or "a linear scan") and one trade-off.
- **"Find the bug":** separate what the code does from what it should do. Point
  to the smallest line range that causes the problem.
- **"This file is huge":** explain the map and the main entry point first. Ask
  which function or feature to go through next.

## Accuracy checklist

Before sending, check:

- [ ] Every line number exists and points to the right code.
- [ ] Every return and error path is explained.
- [ ] Side effects are named.
- [ ] Outside calls are described as outside calls, not guessed.
- [ ] No behavior was invented to make the story smoother.
- [ ] The reader has one clear next step.

## Mini glossary

Use these only when the term appears in the code.

- **Argument:** a value you give to a function when you call it.
- **Return:** the value a function sends back.
- **Variable:** a name that holds a value.
- **Loop:** code that repeats for each item or while a condition is true.
- **Condition:** a yes/no check, such as `if count == 0`.
- **Class:** a blueprint that groups data and actions.
- **Object:** one thing made from a class.
- **Import:** loading code from another file or package.
- **Library:** a collection of code someone else wrote.
- **API:** a set of rules for asking another program for something.
- **Callback:** a function passed to another function, to be run later.
- **Async:** work that can wait without blocking everything else.
- **Exception:** an error that interrupts normal flow.
- **Refactor:** change the shape of code without changing what it does.
