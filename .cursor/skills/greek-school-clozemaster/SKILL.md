---
name: greek-school-clozemaster
description: >-
  Builds and extends the Greek School of Glasgow B1 Clozemaster course from
  weekly lesson PowerPoints. Use when the user adds a class pptx, asks for a
  Clozemaster lesson, sentences, phrases, vocabulary, or to update the course
  without repeating words. Also use when syncing the course to Clozemaster.
  Prefer the Clozemaster MCP tools. If they are not connected, call the site's
  JSON API from the logged-in page, and do not click through the website.
---

# Greek School of Glasgow B1 Clozemaster

The course file is `Greek School of Glasgow - B1.tsv` in the class folder:

`C:/Dev/Github/Greek-Language-Obsidian/Greek School of Glasgow - B1/`

Each week's PowerPoint stays in `Lesson N/`. The TSV is the whole course so far. Sync it with the Clozemaster MCP when that server is connected, in the same account as the phone. The phone app receives the collection after that sync. The MCP repo is `C:/Dev/Github/clozemaster-mcp`.

## Course rules

From the source extract all sentences and phrases. For each create a test of a single word. Over the whole Clozemaster lesson the same word should not repeat. It should cover all the text in the PowerPoint source.

If the sentence is long, break it up. The purpose is to learn words, not memorise sentences.

- One row tests one word. That word is the cloze, and it must appear in the Greek exactly, as its own word.
- Every word that appears in the Greek is the word to guess once. The same sentence may be used again only with a different cloze. A cloze is never repeated. `Διάλεξε` in two lines is still one word, so it is the cloze on one of them and not on the other. A different form that also appears (`λέξη` and `λέξεις`, `μύτη` and `μύτης`) is guessed once each. Capitalisation does not make a second word.
- A token made only of digits, such as `20` or `30`, is not a word. Leave it in the sentence. Do not make it the cloze. Number words written in Greek, such as `ένα`, `δύο`, `τρεις`, and `πέντε`, are still guessed once each.
- A person's name is not a word to guess. Leave it in the sentence. Do not make it the cloze. `Μαρία` stays in `Η Μαρία έχει ικανότητες.` and is not its own card. When a new name appears, add its casefolded form to `PERSON_NAMES` in `scripts/validate_clozemaster.py` so the checker allows it in the sentence.
- Keep each Greek line to at most 10 words. Break at a clause. Repeat the subject from the same source sentence when a piece would not stand alone. Do not invent facts that are not in the source when you split a lesson sentence.
- Order inside a lesson: sentences, then phrases. Append the next lesson after the previous one in the same order.
- Skip English-only lines (times, email, English aims). They are not Greek words to test.
- If the word is already the cloze, do not add another row for it.
- A word with no sentence in the lesson is not left on its own. Write one short sentence that uses that exact form in a common way. The English translates that sentence. Every other word in the sentence is already a cloze. The Greek line must be new, because Clozemaster skips a Greek line the course already has. The sentence is written for the course.
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
3. Add rows so every new Greek word is the cloze once. Repeat an existing sentence only when the cloze is a new word. Do not repeat a cloze. Do not add a person's name. Add a new name to `PERSON_NAMES` instead. If a new word has no sentence in the PowerPoint, write one short sentence for that exact form. Do not leave it as a bare word.
4. Validate. Do not replace earlier lessons.
5. Sync the changed rows with the Clozemaster MCP. If it is not connected, use the API below. Add a Greek line the collection does not already have. To change only the English or the note, update that sentence id. A new Greek line is a new card: add it, then delete the old card. Leave every other card, including its progress.

## Clozemaster MCP

Use the Clozemaster MCP tools for list, add, update, delete, ignore, and play. Add a lesson with the tool that takes many cards. It skips a card when that sentence already hides the same cloze, or when that cloze is already a card. The same sentence is still added when the cloze is new. Find a card by its cloze before updating or deleting it. To change the Greek sentence, use the replace tool: it adds the new sentence, then deletes the old card. The MCP is not tied to one course. When a tool is called with no collection id, it uses the collection this account practiced most recently. For this course, pass collection name `Greek School of Glasgow - B1`, or collection id `119463` if the name is shared. The server keeps its own browser profile on this PC and signs in there. Do not ask for the password, and do not copy the session cookie into the skill or either repo. If a tool says the session has expired, ask the user to run the login tool and sign in in the window it opens.

The tools do not delete a collection and do not reset progress. If the MCP server is not connected, use the API below from a logged-in tab at `https://www.clozemaster.com/l/ell-eng`.

## Clozemaster API

The website is the client of a private JSON API. There is no API key. From the logged-in tab, call it with the page's own `$.ajax`, so the session cookie and CSRF token go with the request. `fetch` without that jQuery setup is rejected. Do not click through the site. Do not copy the cookie or the CSRF token into this skill, the repo, or a script. If the tab is logged out, ask the user to sign in. Do not type their password.

These calls were made against a temporary collection named `API Test`, which was then deleted. The B1 course was not changed. The Greek–English pairing id is `4`. A collection answers at both `/api/v1/lp/4/c/{id}` and `/api/v1/lp/ell-eng/c/{slug}`.

The course collection is `Greek School of Glasgow - B1`, id `119463`, slug `greek-school-of-glasgow-b1-b2a0241984`. Its base URL is:

`https://www.clozemaster.com/api/v1/lp/4/c/119463`

A sentence stores the cloze in the Greek with double braces: `Έχουμε {{μάθημα}} στην τάξη.` The other fields are `translation`, `notes`, and `pronunciation` (`null` when empty).

Never `DELETE` the B1 collection URL. Never reset the B1 collection unless the user asks. The language-wide reset is a different URL and is off limits.

### Collection

- `GET /api/v1/lp/4/c?filter=mine` lists your collections.
- `POST /api/v1/lp/4/c` with form field `collection[name]`, or JSON `{"collection": {"name", "description", "play_order", "public", "use_clozes_as_multiple_choice_options"}}`, creates one. `play_order` is `""` for random or `"id"` for added order.
- `GET {base}` returns the collection, including the URLs for the calls below.
- `PATCH {base}` with that same `collection` object updates the name, description, order, public flag, and multiple-choice flag.
- `PUT {base}/uc` with form field `user_collection[dashboard_collection]` sets whether it shows on the dashboard.
- `POST {base}/uc/reset` wipes progress for that collection only. Sentences stay.
- `DELETE {base}` with `$.ajax({method:"delete"})` removes the collection and its sentences. `DELETE {base}/uc` does not remove a collection you created. That call is the one the site uses to drop progress on a shared collection.

### Sentences

List with `GET {base}/ccs` and `context=sentences`, `page`, `per_page`, `query`, `scope=all`. Page until `total` is covered. The id is `id`. The Greek, with braces, is `text`.

Create one card with `POST {base}/ccs` and JSON `{"collection_cloze_sentence": {"text", "translation", "notes", "pronunciation", "alternative_answers": [], "favorited": false, "hint": null, "ignored": false}}`.

Create several with `POST {base}/bulk_collection_cloze_sentences_upserts` and `{"creates_only": true, "updates": [{"id": null, "text", "translation", "notes", "pronunciation"}]}`. If `status` is not `complete`, poll `bulkCollectionClozeSentencesUpsertUrl` until it is.

Change the English or the note of a card that already exists with the same bulk URL and `{"updates": [{"id": <sentence id>, "text", "translation", "notes", "pronunciation"}]}`. Keep `text` the same, including the braces. Poll the same way. This does not create a second card.

A TSV import still skips a Greek line the collection already has, and it does not delete. Use it only for new lines:

1. `POST /api/v1/lp/4/collection-csv-import` as multipart form data. The file field is `file`, named with a `.tsv` ending. The other field is `separator=tab`. No header: Greek, English, cloze, empty pronunciation, note. Poll the returned `url` until `status` is `complete`.
2. Save `result` with the bulk create above, setting each `id` to `null`.

`POST {base}/ccs/delete` with `{"collection_cloze_sentence_id": <id>}` removes one card and that card's progress. Match the card by its full Greek text.

`PUT {base}/ccs/ignore_all` with `collection_cloze_sentence_id` hides a card from play. `GET {base}/play` returns the next cards and leaves ignored cards out.

`PUT` on a single sentence URL is rejected. Use the bulk upsert to change a card.

### Account-level reads

These belong to the whole Greek–English account, not to one collection. Read them if needed. Do not change them while working on this course.

`GET /api/v1/lp/4/review-settings` returns `customSettings`: `alreadyMasteredNextReview`, `defaultMaxReviewsPerCollectionPerDay`, `maxReviewsPerRound`, `nextReviewByLevel`, `nextReviewFuzzEnabled`, `reviewsOrderedBy`.

`GET /api/v1/lp/4/more-stats` and `GET /api/v1/lp/4/daily-stats` return progress charts. `GET /api/v1/lp/ell-eng` is the dashboard payload and includes the URL for each later call.

The dashboard also names stats, sync, download, game settings, daily goal, and streak URLs. A plain `GET` on those URLs returned 404, so do not call them until a response succeeds. The collection answer and spaced-repetition URLs are advertised too, and the posts tried against them returned 404. Play stays on `GET {base}/play`.
