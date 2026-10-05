---
name: greek-school-clozemaster
description: >-
  Builds and extends the Greek School of Glasgow B1 Clozemaster course from
  weekly lesson PowerPoints. Use when the user adds a class pptx, asks for a
  Clozemaster lesson, sentences, phrases, vocabulary, or to update the course
  without repeating words.
---

# Greek School of Glasgow B1 Clozemaster

The course file is `Greek School of Glasgow - B1.tsv` in the class folder:

`C:/Dev/Github/Greek-Language-Obsidian/Greek School of Glasgow - B1/`

Each week's PowerPoint stays in `Lesson N/`. The TSV is the whole course so far. Upload that file to Clozemaster (tab-separated) on the website, in the same account as the phone. The phone app only receives the collection after that upload.

## Course rules

From the source extract all sentences, phrases and useful single words if they make sense on their own (in that order). For each create a test of a single word. Over the whole Clozemaster lesson the same word should not repeat. It should cover all the text in the PowerPoint source.

If the sentence is long, break it up. The purpose is to learn words, not memorise sentences.

- One row tests one word. That word is the cloze, and it must appear in the Greek exactly, as its own word.
- Every word that appears in the Greek is the word to guess once. The same sentence may be used again only with a different cloze. A cloze is never repeated. `Διάλεξε` in two lines is still one word, so it is the cloze on one of them and not on the other. A different form that also appears (`λέξη` and `λέξεις`, `μύτη` and `μύτης`) is guessed once each. Capitalisation does not make a second word.
- A token made only of digits, such as `20` or `30`, is not a word. Leave it in the sentence. Do not make it the cloze. Number words written in Greek, such as `ένα`, `δύο`, `τρεις`, and `πέντε`, are still guessed once each.
- A person's name is not a word to guess. Leave it in the sentence. Do not make it the cloze. `Μαρία` stays in `Η Μαρία έχει ικανότητες.` and is not its own card. When a new name appears, add its casefolded form to `PERSON_NAMES` in `scripts/validate_clozemaster.py` so the checker allows it in the sentence.
- Keep each Greek line to at most 10 words. Break at a clause. Repeat the subject from the same source sentence when a piece would not stand alone. Do not invent facts that are not in the source.
- Order inside a lesson: sentences, then phrases, then single words. Append the next lesson after the previous one in the same order.
- Skip English-only lines (times, email, English aims). They are not Greek words to test.
- A single word is only a row when it was not already the cloze and it makes sense on its own. If the word is already the cloze, do not add another row that is only that word.
- The file matches the Clozemaster course: the same Greek sentence and the same cloze. A sentence is repeated only when the cloze is a new word. Uploading the file again does not change a sentence the course already has. The English on a row translates the Greek that is actually on the row.

## File format

UTF-8, no header, no BOM. Five tab-separated fields:

`Greek`, `English`, `cloze`, empty pronunciation, dictionary note

The note is what Clozemaster can show on the card. It uses English learner-dictionary abbreviations and does not include the lesson label. Leave pronunciation empty.

- Noun: `n. m. sg. ο χαρακτήρας, pl. οι χαρακτήρες`. The article shows the gender. Add the case when the guessed word is not the nominative singular: `· acc. sg.`, `· gen. sg.`, `· gen. pl.`
- Adjective: `adj. καλός, -ή, -ό`. The three forms are masculine, feminine, neuter singular, in that order. The hyphen keeps the stem. Add the form when it is not the masculine singular: `· f. sg.`, `· n. pl.`
- Verb: `v. διαβάζω`. Add the person when the guessed word is not that form: `· 3 sg.`, `· 1 pl.`, `· imp. sg.`, `· imp. pl.`, `· perf.`, `· past`
- Other words: `adv.`, `prep.`, `conj.`, `pron.`, `art.`, `num.`, `part.`, `intj.` Put gender and number on articles and pronouns: `art. f. sg. acc.` A person's name has no note, because it is not a card.

```text
κι εμείς καλύτερα	and we lived even better	καλύτερα		adj. καλός, -ή, -ό
Διάλεξε την κατάλληλη λέξη.	Pick the right word.	λέξη		n. f. sg. η λέξη, pl. οι λέξεις
```

Before saving, run:

```bash
python ~/.cursor/skills/greek-school-clozemaster/scripts/validate_clozemaster.py "<course.tsv>"
```

Fix every reported line and run it again. Leave the file only when it prints `OK`.

## Adding the next lesson

1. Read the existing TSV and collect every cloze. The note is the dictionary line, not a lesson label.
2. Read the new PowerPoint, including text that is only in pictures.
3. Add rows so every new Greek word is the cloze once. Repeat an existing sentence only when the cloze is a new word. Do not repeat a cloze. Do not add a person's name. Add a new name to `PERSON_NAMES` instead.
4. Validate. Do not replace earlier lessons.
