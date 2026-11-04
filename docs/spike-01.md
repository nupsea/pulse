## Learnings



| Query | Result |
| --- | --- |
| Volume | Avg: 79.39 vehicles per poll |
| Freshness | Not able to determine (Refer spike.py notebook) |
| Lag | median_diff : 23 sec, p95_lag : 44 sec |
| Duplicates | dupe percentage: 3.98 |
| Shared Trip % | 13% (Appears low) |


Surprised:
1. Shared trip percentage is so low.
2. No null data as such
3. It takes a lot of time to analyse .. How can I get better and faster.

Open Questions:
- How do you determine freshness?
-  How does one prove correctness. What if things go wrong..?
-  How to handle null data.. and with different fields, I assume its different.
-  What is a general analytical process adopted by experienced data professionals to see value inside data?