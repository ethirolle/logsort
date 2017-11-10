# logsort
Sort large log files / handles multi-line log entries

When we put a busy services into debug mode, this can create log files that are:
1) enormous
2) out of date-time order (i.e., the loggers may run asynchronously, and dump large clumps of log lines, resulting in a log file where lines are not in datetime order.)

The key difficulty with sorting a *log* file with a simple Linux 'sort' command is: some log entries span multiple lines. The clue that these multiple lines are a single log entry is that the entry begins with a date-time stamp. Here is a sample excerpt of a log file to demonstrate this multi-line nature of some log entries:

```
2017-11-08 20:40:27,467 DEBUG zen.command.parsers.diskstats: Parser class: <class 'ZenPacks.zenoss.LinuxMonitor.parsers.linux.diskstats.BlockParser'>, Scanner: (?P<component>253\s+5\s+\S+\s)(?P<readsCompleted>\d+\s)(?P<readsMerged>\d+\s)(?P<sectorsRead>\d+\s)(?P<msReading>\d+\s)(?P<writesCompleted>\d+\s)(?P<writesMerged>\d+\s)(?P<sectorsWritten>\d+\s)(?P<msWriting>\d+\s)(?P<ioInProgress>\d+\s)(?P<msDoingIO>\d+\s)(?P<msDoingIOWeighted>\d+)
2017-11-08 20:40:27,468 DEBUG zen.command.parsers.diskstats: Parsed metrics: [(({'componentScanValue': 'disk-fileserver-share--snap1',
  'hdFilterRegex': '^[hs]d[a-z]\\d+$|c\\d+t\\d+d\\d+s\\d+$|^cciss\\/c\\dd\\dp\\d$|^dm\\-\\d$',
  'major_minor': '253:5'},
 'writesMerged'), 0.0), (({'componentScanValue': 'disk-fileserver-share--snap1',
  'hdFilterRegex': '^[hs]d[a-z]\\d+$|c\\d+t\\d+d\\d+s\\d+$|^cciss\\/c\\dd\\dp\\d$|^dm\\-\\d$',
  'major_minor': '253:5'},
 'writesCompleted'), 0.0), (({'componentScanValue': 'disk-fileserver-share--snap1',
  'hdFilterRegex': '^[hs]d[a-z]\\d+$|c\\d+t\\d+d\\d+s\\d+$|^cciss\\/c\\dd\\dp\\d$|^dm\\-\\d$',
  'major_minor': '253:5'},
 'sectorsWritten'), 0.0), (({'componentScanValue': 'disk-fileserver-share--snap1',
  'hdFilterRegex': '^[hs]d[a-z]\\d+$|c\\d+t\\d+d\\d+s\\d+$|^cciss\\/c\\dd\\dp\\d$|^dm\\-\\d$',
  'major_minor': '253:5'},
 'sectorsRead'), 46067848.0), (({'componentScanValue': 'disk-fileserver-share--snap1',
  'hdFilterRegex': '^[hs]d[a-z]\\d+$|c\\d+t\\d+d\\d+s\\d+$|^cciss\\/c\\dd\\dp\\d$|^dm\\-\\d$',
  'major_minor': '253:5'},
 'msWriting'), 0.0), (({'componentScanValue': 'disk-fileserver-share--snap1',
  'hdFilterRegex': '^[hs]d[a-z]\\d+$|c\\d+t\\d+d\\d+s\\d+$|^cciss\\/c\\dd\\dp\\d$|^dm\\-\\d$',
  'major_minor': '253:5'},
 'readsCompleted'), 5758481.0), (({'componentScanValue': 'disk-fileserver-share--snap1',
  'hdFilterRegex': '^[hs]d[a-z]\\d+$|c\\d+t\\d+d\\d+s\\d+$|^cciss\\/c\\dd\\dp\\d$|^dm\\-\\d$',
  'major_minor': '253:5'},
 'msDoingIO'), 2292957.0), (({'componentScanValue': 'disk-fileserver-share--snap1',
  'hdFilterRegex': '^[hs]d[a-z]\\d+$|c\\d+t\\d+d\\d+s\\d+$|^cciss\\/c\\dd\\dp\\d$|^dm\\-\\d$',
  'major_minor': '253:5'},
 'msReading'), 3258340.0), (({'componentScanValue': 'disk-fileserver-share--snap1',
  'hdFilterRegex': '^[hs]d[a-z]\\d+$|c\\d+t\\d+d\\d+s\\d+$|^cciss\\/c\\dd\\dp\\d$|^dm\\-\\d$',
  'major_minor': '253:5'},
 'msDoingIOWeighted'), 3258466.0), (({'componentScanValue': 'disk-fileserver-share--snap1',
  'hdFilterRegex': '^[hs]d[a-z]\\d+$|c\\d+t\\d+d\\d+s\\d+$|^cciss\\/c\\dd\\dp\\d$|^dm\\-\\d$',
  'major_minor': '253:5'},
 'ioInProgress'), 0.0), (({'componentScanValue': 'disk-fileserver-share--snap1',
  'hdFilterRegex': '^[hs]d[a-z]\\d+$|c\\d+t\\d+d\\d+s\\d+$|^cciss\\/c\\dd\\dp\\d$|^dm\\-\\d$',
  'major_minor': '253:5'},
 'readsMerged'), 0.0)]
2017-11-08 20:40:27,472 DEBUG zen.command.parsers.diskstats: Parser class: <class 'ZenPacks.zenoss.LinuxMonitor.parsers.linux.diskstats.BlockParser'>, Scanner: (?P<component>253\s+1\s+\S+\s)(?P<readsCompleted>\d+\s)(?P<readsMerged>\d+\s)(?P<sectorsRead>\d+\s)(?P<msReading>\d+\s)(?P<writesCompleted>\d+\s)(?P<writesMerged>\d+\s)(?P<sectorsWritten>\d+\s)(?P<msWriting>\d+\s)(?P<ioInProgress>\d+\s)(?P<msDoingIO>\d+\s)(?P<msDoingIOWeighted>\d+)
```

This project is designed to provide the tools needed to properly sort a log file that may have multi-line log entries: i.e., we must  keep all non-dated lines with their intended header log line. 

The approach to this problem is as follows:

1) "Mash" the log lines. I.e., combine each multi-line log entry into a single line. Use a unique separator between each line, so that later we can find-and-replace these separators back to newlines.

2) Use GNU sort command to sort the file. (Note: the GNU sort command is designed to do an external-sort-and-merge approach, allowing it to handle VERY large files. There is therefore no need to write any sorting code here, we will just leverage GNU sort.)

3) "Unmash" the sorted log file. I.e., split log lines to re-create the original multi-line log entries.
