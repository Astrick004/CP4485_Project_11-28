USE summarizer;
INSERT INTO user VALUES
(1, "jsmith", "password01"),
(2, "wbrown", "password02"),
(3, "kblack", "password03");

INSERT INTO summary VALUES
(1, "2023-01-10", "Example 1 of article text", NULL, "Summary text 1", NULL, 1),
(2, "2023-02-05", "Example 2 of article text", NULL, "Summary text 2", NULL, 2),
(3, "2023-03-15", "Example 3 of article text", NULL, "Summary text 3", NULL, 3),
(4, "2023-05-20", "Example 4 of article text", NULL, "Summary text 4", NULL, 1),
(5, "2023-05-20", "Example 5 of article text", NULL, "Summary text 5", NULL, 1),
(6, "2023-09-29", "Example 6 of article text", NULL, "Summary text 6", NULL, 2),
(7, "2023-10-30", "Example 7 of article text", NULL, "Summary text 7", NULL, 1);
