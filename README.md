# logsort
Sort large log files / handles multi-line log entries

When we put a busy services into debug mode, this can create log files that are:
1) enormous
2) out of date-time order (i.e., the loggers may run asynchronously, and dump large clumps of log lines, resulting in a log file where lines are not in datetime order.)

The key difficulty with sorting a *log* file with a simple Linux 'sort' command is: some log entries span multiple lines. The clue that these multiple lines are a single log entry is that the entry begins with a date-time stamp. Here is a sample excerpt of a log file to demonstrate this multi-line nature of some log entries:

```
2017-11-06 21:23:16,769 DEBUG zen.ps: line '   78     0 00:00:00 [migration/14]' -> pid=78 rss=0 cpu=00:00:00 cmdAndArgs=[migration/14]
  events: []
  values: [(({'componentScanValue': 'lo'}, 'ifInOverruns'), 0.0),
2017-11-06 21:23:16,769 DEBUG zen.ps: line '   79     0 00:00:00 [ksoftirqd/14]' -> pid=79 rss=0 cpu=00:00:00 cmdAndArgs=[ksoftirqd/14]
 (({'componentScanValue': 'lo'}, 'ifInErrors'), 0.0),
 (({'componentScanValue': 'lo'}, 'ifInPackets'), 6.0),
 (({'componentScanValue': 'lo'}, 'ifInDropped'), 0.0),
```

This project is designed to provide the tools needed to properly sort a log file that may have multi-line log entries: i.e., we must  keep all non-dated lines with their intended header log line. 

The approach to this problem is as follows:

1) "Mash" the log lines. I.e., combine each multi-line log entry into a single line. Use a unique separator between each line, so that later we can find-and-replace these separators back to newlines.

2) Use GNU sort command to sort the file. (Note: the GNU sort command is designed to do an external-sort-and-merge approach, allowing it to handle VERY large files. There is therefore no need to write any sorting code here, we will just leverage GNU sort.) E.g.,
```
sort inputfile.txt -o sortedfile.txt
```

3) "Unmash" the sorted log file. I.e., split log lines to re-create the original multi-line log entries.
