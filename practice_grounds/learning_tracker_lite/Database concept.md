# Database Concept

---
**Content**
What will be stored in the DB:
Simplified version of the final logged DB

- Automatic ID generation for every added entry
- What did i learn (subject)
- New skills learned (key learnings 1 sentence)
- Notes (what was done)
- Time spent learning
- Difficulties 1-10 (10 the most difficult, 1 easy)
- timestamp of entry created

**Functionality**
How should the user be able to interact with the DB:

- Add new entry
- Delete entry
- edit entry (full, not only 1 single parameter)
- display entries filtered by subject (for now only one filter maybe more functionality later)

**Table concept**

 | ID | Subject | Key Learnings | Notes | Time spend | Difficulty | datetime|
|----|---------|---------------|-------|------------|------------|---------|
|Automatic(int)|string|string|string|float(eg 1.5 in hours)| int (limited 1-10)| Automatic


**Planning The API**
Pydantic model for a single new entry:
