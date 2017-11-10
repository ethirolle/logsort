# logsort
Sort large log files / handles multi-line log entries

When putting bucy services into debug mode, we can create log files that are:
1) enormous
2) not well-sorted

I.e., the loggers may run asynchronously, and dump large clumps of log lines, resulting in a log file where lines are not in datetime order.

The key difficulty with sorting this file with a simple Linux 'sort' command is: some log entries span multiple lines. The clue that these multiple lines are a single log entry is that the entry begins with a date-time stamp.

This project is designed to provide the tools needed to sort a log file that may hae multi-line log entries. The approach is:

1) "Mash" the log lines. I.e., combine multi-line log entries into a single line. We add a unique separator, so that later we can find-and-replace these separators back to newlines.

2) Use GNU sort command to sort the file.

3) "Unmash" the sorted log file. I.e., split log lines to re-create the original multi-line log entries.

Note: the GNU sort command is designed to do an external-sort-and-merge approach, allowing it to handle VERY large files. There is therefore no need to write any sorting code here, we will just leverage GNU sort.
