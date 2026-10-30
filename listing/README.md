# Listing CSV

Save `listing/<collection>.json` as an array of items, or an object with `items`:

```json
{
  "items": [{
    "filename": "outline_box.svg",
    "title": "Educational box outline",
    "description": "Black outline clipart with transparent background.",
    "keywords": ["box", "education", "outline"],
    "ai_assisted": true
  }]
}
```

Run `python3 listing/make_csv.py <collection>` to write `listing/<collection>.csv`.
Columns: filename, title, description, keywords, ai_assisted. CSV uses UTF-8 with
a BOM, standard quoting, and comma-separated keywords with duplicates removed.
The AI disclosure defaults to true; assisted items cannot claim hand-drawn work.
Map these portable columns to the selected marketplace's import fields and set
its required AI disclosure controls according to its current policy. The CSV
does not submit assets or claim compliance with any particular marketplace.
